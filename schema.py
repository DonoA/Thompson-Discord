import mysql.connector
from mysql.connector import errorcode

def setup(cnx):
    TABLES = {}
    TABLES['users'] = [
        "`id` int(11) NOT NULL AUTO_INCREMENT",
        "`discord_id` int(11) NOT NULL", # the api id
        "`rank` int(11) NOT NULL DEFAULT '0'", # 0 = regular, 1 = admin
        "`chat_mode` int(11) NOT NULL DEFAULT '0'", # 0 = regular, 1 = command (all chat are commands)
        "PRIMARY KEY (`id`)"
    ]
    cursor = cnx.cursor()
    for name, fields in TABLES.items():
        query = "CREATE TABLE `thompson`.`{}` (".format(name)
        for col in fields:
            query=query+"{},".format(col)
        query = "{}) ENGINE = InnoDB;".format(query[:-1])
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
