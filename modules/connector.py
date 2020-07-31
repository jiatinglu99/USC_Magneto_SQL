import mysql.connector

# module that manages connection with SQL Database
class Connector:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.cnx = mysql.connector.connect(user='root', password='M@riaDb4Spac3',
                              host=self.host, database=self.database)
        self.cursor = self.cnx.cursor()

    def check_table_exist(self, name):
        cmd = "SHOW TABLES LIKE " + "'" + name + "'"
        self.cursor.execute(cmd)
        result = self.cursor.fetchone()
        if result: 
            return True
        else: 
            return False

    def create_table(self, name, keys):
        if self.check_table_exist(name):
            print('Table ' + name + ' already exists, proceed...')
            return
        cmd = 'CREATE TABLE ' + name + ' (\n'
        for i in range(len(keys)):
            cmd += '\t' + keys[i][0] + ' ' + keys[i][1]
            if keys[i][0] == 'Time':
                cmd += ' NOT NULL'
            #if i == len(keys)-1:# last item 
            #    cmd += '\n'
            #else:
            cmd += ',\n'
        cmd += '\tCONSTRAINT time_pk PRIMARY KEY (Time)\n'
        cmd += ');'
        print(cmd)
        self.cursor.execute(cmd)
        print('Table ' + name + ' created successfully...')
        

    def add_to_sql(self, name, keys, entries):
        #cmd = 'INSERT 
        #ON DUPLICATE KEY UPDATE '
        pass

    def __del__(self):
        #self.cnx.close()
        pass