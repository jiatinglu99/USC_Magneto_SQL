#from modules.decoder import Decoder
from datetime import date
import mailbox
import email
import os
import shutil

######## Choose one of the following 
# dir = '/home/usc-magneto/Maildir' # dir on Magneto VM
dir = os.path.join(os.getcwd(), 'sample', 'Maildir') # dir on test environment

class Parser:
    # initialize an instance of Maildir
    def __init__(self, dir):
        self.dir = dir
        self.mbox = mailbox.Maildir(self.dir)
    
    def parse_all(self):
        # directory to store emails without HEX keys
        self.dir_others_folder = os.path.join(dir, 'OTHERS')

        # directory to store emails with Data to be parsed to SQL
        self.dir_date_folder = os.path.join(dir, 'DATA', str(date.today()))
        to_remove_data = []
        to_remove_others = []

        # parse all emails
        for key, msg in self.mbox.iteritems():
            msg.set_subdir('cur') # move email to 'cur' subdir
            print(msg.get_info())
            #print(type(msg))
            to_remove_data.append(key)

        # move all files to destination folder
        for key in to_remove_data:
            dir_file = os.path.join(dir, 'new', key)
            remove_file()
    
    def copy_and_remove_message(source, destination):
        #dest = shutil.copyfile(source, destination)
        pass
        

    def get_HEX_from_message(self, msg):
        pass

    def get_message(self, dur):
        pass






if __name__ == "__main__":
    parser = Parser(dir)
    parser.parse_all()

    # for dir testing purpose
    """
    for dirname, subdirs, files in os.walk(dir):
        print(dirname)
        print('\tDirectories:', subdirs)
    for name in files:
        fullname = os.path.join(dirname, name)
        print()
        print('***', fullname)
        print(open(fullname).read())
        print('*' * 20)

    for key, msg in mbox.iteritems():
        print(key)
        print(msg.get_info())
    """