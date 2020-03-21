import os 
import sys
from modules.decoder import *
from modules.parser import *
from modules.connector import *

######## Choose one of the following 
#dir = '/home/usc-magneto/Maildir' # dir on Magneto VM
dir_from = os.path.join(os.getcwd(), 'sample', 'Maildir') # dir on test environment

# This is the folder where all past emails are stored
dir_dest = os.path.join(os.getcwd(), 'History')

######## Choose one of the following 
#host = 'localhost'
host = 'magneto.isi.edu'
 
######## Choose one of the following 
#database = 'magneto'
database = 'testing'

class Manager:
    # initialize an instance of Maildir
    def __init__(self, dir_from, dir_dest):
        self.dir = dir_from
        self.dir_dest = dir_dest
        self.parser = Parser(dir_from, dir_dest)
        self.decoder = Decoder()
        self.connector = Connector(host, database)

    def run(self):
        self.key_dict_collection = self.parser.parse_all()
        print(self.key_dict_collection)
        for key_dict in self.key_dict_collection:
            key = key_dict['Key']
            del key_dict['Key']
            decoded = self.get_decoded(key)
            key_dict.update(decoded)
            # add to SQL Server
            self.connector.add_to_sql(key_dict)

    def get_decoded(self, hex_key):
        decoded = self.decoder.decodeBeacon(hex_key,0)
        return decoded
        #print(decoded)
        #print(self.dec.getPrintableBeacon(decoded))

if __name__ == "__main__":
    manager = Manager(dir_from, dir_dest)
    manager.run()