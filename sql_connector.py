import mysql.connector
from mysql.connector import errorcode
from config import config

connection = mysql.connector.connect(**config['db'], host='127.0.0.1')

def setup():
    TABLES = {}
    TABLES['users'] = [
        "`id` int(11) NOT NULL AUTO_INCREMENT",
        "`discord_id` varchar(20) NOT NULL", # the api id
        "`name` varchar(20) NOT NULL", # 0 = regular, 1 = admin
        "`rank` int(11) NOT NULL DEFAULT '0'", # 0 = regular, 1 = admin
        "PRIMARY KEY (`id`)"
    ]
    cursor = connection.cursor()
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
