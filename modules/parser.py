#from modules.decoder import Decoder
from datetime import date
import mailbox
import email
import os
import shutil

class Parser:
    # initialize an instance of Maildir
    def __init__(self, dir_from, dir_dest):
        self.dir = dir_from
        self.dir_dest = dir_dest
        self.mbox = mailbox.Maildir(self.dir, factory=None)
        
        #!!! if delete == true, the program will clear the inbox after parsing as intended
        #!!! false delete is only for testing purpose
        self.delete = False
    
    def parse_all(self):
        # directory to store emails without HEX keys
        self.dir_others_folder = os.path.join(self.dir_dest, 'OTHERS')

        # directory to store emails with Data to be parsed to SQL
        self.dir_date_folder = os.path.join(self.dir_dest, 'DATA', str(date.today()))
        to_remove_data = []
        to_remove_others = []
        hex_key_collection = []

        # parse all emails
        for key, msg in self.mbox.iteritems():
            #msg.set_subdir('cur') # move email to 'cur' subdir
            # find HEX
            body = self.get_body(msg)
            lines = body.splitlines()
            #print(msg['Date'])

            is_DATA = False
            for line in lines:
                if 'HEX:' in line:
                    # exit search
                    is_DATA = True
                    break
            if is_DATA:
                # it is DATA
                to_remove_data.append(key)
                # look for the actual HEX key
                hex_key = self.extract_HEX(line)
                temp_dict = {
                    'Key':  hex_key,
                    'From': msg['From'],
                    'Date': msg['Date']
                    }
                hex_key_collection.append(temp_dict)
            else:
                to_remove_others.append(key)
                    
        
        #print(to_remove_data)
        #print(to_remove_others)
            
        # move all files to destination folder
        for key in to_remove_data:
            dir_source = os.path.join(self.dir, 'new', key)
            dir_destination = os.path.join(self.dir_date_folder, key)
            #print(dir_source)
            #print(dir_destination)
            if not os.path.exists(self.dir_date_folder):
                os.makedirs(self.dir_date_folder)
            shutil.copyfile(dir_source, dir_destination)
            if self.delete: self.mbox.remove(key)

        for key in to_remove_others:
            dir_source = os.path.join(self.dir, 'new', key)
            dir_destination = os.path.join(self.dir_others_folder, key)
            #print(self.dir_others_folder)
            if not os.path.exists(self.dir_others_folder):
                os.makedirs(self.dir_others_folder)
            shutil.copyfile(dir_source, dir_destination)
            if self.delete: self.mbox.remove(key)
        
        return hex_key_collection
    
    def get_body(self, message): #getting plain text 'email body'
        body = None
        if message.is_multipart():
            for part in message.walk():
                if part.is_multipart():
                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            body = subpart.get_payload(decode=True)
                elif part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
        elif message.get_content_type() == 'text/plain':
            body = message.get_payload(decode=True)
        return body.decode()

    def extract_HEX(self, line):
        temp = line.split(':')
        for item in temp:
            if item != 'HEX':
                return item
        
    def get_message(self, dur):
        pass


    # for dir testing purpose only 
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