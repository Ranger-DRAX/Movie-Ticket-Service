import MySQLdb


connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db='movie_ticket' )#---server---name-----


cursor = connection.cursor()


cursor.execute("SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'movie_ticket' ")


result = cursor.fetchone()[0]


if result:
    print("Database exists ")
else:
    print("Database does not exist")



cursor.close()
connection.close()
