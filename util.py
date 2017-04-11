import re
from user import User

def get_user(message, pos, bots=True):
    args = message.content.split(" ")
    target = None
    i = 0
    while pos >= 0:
        target = re.findall(r'<@(.+)>', args[i])
        i = i + 1
        if len(target) > 0:
            pos = pos - 1
        elif len(args) <= i:
            return None


    member = None
    for m in message.mentions:
        if m.id == target[0] and (bots or not m.bot):
            member = m
            break

    if member is None:
        return None

    return User.find(member.id, member.name)
