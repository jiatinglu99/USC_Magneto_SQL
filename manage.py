import os 
import sys
from modules.parser import *
from modules.decoder import *
import modules.entries as Standard
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

######## True if running for the first time
create_database = True
create_table = True

class Manager:
    # initialize an instance of Maildir
    def __init__(self, dir_from, dir_dest):
        self.dir = dir_from
        self.dir_dest = dir_dest
        self.parser = Parser(dir_from, dir_dest)
        self.decoder = Decoder()
        self.connector = Connector(host, database)

    def run(self):
        # for storing data entries to be pushed into database later
        to_be_added_Primary = list()
        to_be_added_Secondary = list()

        self.key_dict_collection = self.parser.parse_all()
        #print(self.key_dict_collection)
        print('Parsed ' + str(len(self.key_dict_collection)) + ' Key(s) in Total')
        used_keys = set() # to avoid repetition with keys
        for key_dict in self.key_dict_collection:
            print('    Parsed Key from ' + key_dict['From'] + ' at ' + key_dict['Date'])
            key = key_dict['Key']
            if key in used_keys:
                print("        Key Repeated! Pass...")
                continue
            used_keys.add(key)

            # Decode Key and Add to to_be_added_...
            decoded = self.get_decoded(key)
            print('        Beacon Type '+str(decoded[2][1])+' identified.')
            #print(get_primary_data(decoded, key_dict['From'])
            for entry in Standard.get_primary_data(decoded, key_dict['From']):
                to_be_added_Primary.append(entry)
            to_be_added_Secondary.append(Standard.get_secondary_data(decoded, key_dict['From']))
            #print(to_be_added_Secondary)

        # Combine and eliminate repetition
        #print(to_be_added_Primary)
        print('########### PRIMARY ##########')
        to_be_added_Primary = self.get_fixed_list(to_be_added_Primary)
        print('########## SECONDARY #########')
        to_be_added_Secondary = self.get_fixed_list(to_be_added_Secondary)
        #print(to_be_added_Primary)

        # add to SQL Server
        if create_database:
            pass
        if create_table:
            self.connector.create_table('Primary', Standard.PrimaryEntry)
            self.connector.create_table('Secondary', Standard.SecondaryEntry)
        #self.connector.add_to_sql(key_dict)

    def get_decoded(self, hex_key):
        decoded = self.decoder.decodeBeacon(hex_key,0)
        #print(decoded)
        #print(self.decoder.getPrintableBeacon(decoded))
        return decoded

    # combine and eliminate repetition within data entry list
    def get_fixed_list(self, entries):
        #print('####### FIXING_ENTRIES #######')
        print('    ' + str(len(entries)) + ' entries detected.')
        if len(entries) == 0: return entries
        # sort the list based on time
        entries.sort(key = lambda x:x[0])
        # add all to a new list
        fixed_entries = []
        first_time = True
        for entry in entries:
            # check if the entry time is already in fixed entries
            if first_time:
                fixed_entries.append(entry)
                first_time = False
            else:
                t = entry[0]
                repeated = False
                for existing_entry in fixed_entries:
                    if t == existing_entry[0]:
                        # repetition occurs, merge
                        repeated = True
                        for m in range (1, len(existing_entry)):
                            if existing_entry[m] == 'NULL':
                                existing_entry[m] = entry[m]
                        break # ignore following
                if not repeated:
                    fixed_entries.append(entry)
        print('    ' + str(len(fixed_entries)) + ' entries after merge.')
        #print('############ DONE ############')
        return fixed_entries


if __name__ == "__main__":
    manager = Manager(dir_from, dir_dest)
    manager.run()