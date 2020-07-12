import mysql.connector

# module that manages connection with SQL Database
class Connector:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        #self.cnx = mysql.connector.connect(user='root', password='M@riaDb4Spac3',
        #                      host=self.host, database=self.database)
        #self.cursor = self.cnx.cursor()

    def create_table(self, name, keys):
        cmd = 'CREATE TABLE ' + name + ' (\n'
        for i in range(len(keys)):
            cmd += '\t' + keys[i][0] + ' ' + keys[i][1]
            if keys[i][0] == 'Time':
                cmd += ' NOT NULL PRIMARY KEY'
            if i == len(keys)-1:# last item 
                cmd += '\n'
            else:
                cmd += ',\n'
        cmd += ');'
        print(cmd)
        #self.cursor.execute(cmd)
        

    def add_to_sql(self, name, keys, entries):
        #cmd = 'INSERT 
        #ON DUPLICATE KEY UPDATE '
        pass

    def __del__(self):
        #self.cnx.close()
        pass