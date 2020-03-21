import mysql.connector


class Connector:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.cnx = mysql.connector.connect(user='root', password='M@riaDb4Spac3',
                              host=self.host, database=self.database)
        self.cursor = self.cnx.cursor()

    def add_to_sql(self, key_dict):
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in key_dict.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in key_dict.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('mytable', columns, values)
        print(columns)

    def __del__(self):
        self.cnx.close()