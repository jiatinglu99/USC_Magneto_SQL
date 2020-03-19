import os 
import sys
from modules.decoder import *
from modules.parser import *

######## Choose one of the following 
# dir = '/home/usc-magneto/Maildir' # dir on Magneto VM
dir_from = os.path.join(os.getcwd(), 'sample', 'Maildir') # dir on test environment

######## This is the folder where all past emails are stored
dir_dest = os.path.join(os.getcwd(), 'History')

class Manager:
    # initialize an instance of Maildir
    def __init__(self, dir_from, dir_dest):
        self.dir = dir_from
        self.dir_dest = dir_dest
        self.parser = Parser(dir_from, dir_dest)
        self.dec = Decoder()

    def run(self):
        self.keys = self.parser.parse_all()


    def process_data(self, hex_key):
        decoded = self.dec.decodeBeacon(hex_key,0)
        print(decoded)#self.dec.getPrintableBeacon(decoded))

if __name__ == "__main__":
    manager = Manager(dir_from, dir_dest)
    manager.run()