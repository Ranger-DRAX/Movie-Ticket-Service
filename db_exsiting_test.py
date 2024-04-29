import MySQLdb


connection = MySQLdb.connect(host="hosting_server",
                             user="user",
                             passwd="password",
                             db='server_name' )


cursor = connection.cursor()


cursor.execute("SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'server_name' ")


result = cursor.fetchone()[0]


if result:
    print("Database exists ")
else:
    print("Database does not exist")



cursor.close()
connection.close()
