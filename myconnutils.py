import pymysql.cursors


# Function return a connection.
def getConnection():
    # You can change the connection arguments.

    connection = pymysql.connect(host="108.170.60.18", port=3306, user="sistagua_root",
                                    charset='utf8',
                                    password="Sistagua2020*", db="sistagua_bd",
                                    cursorclass=pymysql.cursors.DictCursor
                                )

    # connection = pymysql.connect(
    #     host="localhost", port=3306, user="root",
    #     charset='utf8',
    #     password="", db="sistagua_bd",
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    return connection