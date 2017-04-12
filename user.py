from sql_connector import connection
import time, json

cache = {}

ranks=[
    "Default",
    "User",
    "Admin"
]

class User:
    def find(d_id, name=''):
        if d_id in cache:
            cache[d_id]._from_cache = True
            return cache[d_id]
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `users` WHERE `discord_id` = {} LIMIT 1;".format(d_id))
            user = cursor.fetchone()
            cursor.close()
            if user is not None:
                user = User(user[1], user[2], s_id=user[0], rank=user[3])
                cache[d_id] = user
                return user
            else:
                user = User(d_id, name, new=True)
                cache[d_id] = user
                return user

    def __init__(self, d_id, name, s_id='', rank=0, new=False):
        self._id = s_id
        self.discord_id = d_id
        self.rank = rank
        self.name = name
        self._dirty = False
        self._new = new
        self._from_cache = False
        if new:
            self.commit()

    def promote(self, new_rank):
        if len(ranks) <= new_rank:
            return False
        self.rank = new_rank
        self._dirty = True
        self.commit()
        return True

    def demote(self, new_rank):
        if new_rank < 0:
            return False
        self.rank = new_rank
        self._dirty = True
        self.commit()
        return True

    def rank_name(self):
        return ranks[self.rank]

    def has_perm(self, cmd):
        return ('rank' in cmd and cmd['rank'] <= self.rank) or 'rank' not in cmd

    def commit(self):
        if self._new:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO `users` (`discord_id`, `name`, `rank`) VALUES (%s, %s, %s);", (self.discord_id, self.name, self.rank))
            connection.commit()
            self._new = False
            cursor.close()
        elif self._dirty:
            cursor = connection.cursor()
            cursor.execute("UPDATE `users` SET `discord_id`= %s, `name` = %s, `rank` = %s WHERE id = %s;", (self.discord_id, self.name, self.rank, self._id))
            connection.commit()
            self._dirty = False
            cursor.close()

    def purge(self):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM `users` WHERE id=%s", (self._id))
        cursor.close()

    def hash(self):
        attrs = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]
        s = {}
        for attr in attrs:
            s[attr] = getattr(self,attr)
        return s

def purge_cache():
    global cache
    cache = {}
