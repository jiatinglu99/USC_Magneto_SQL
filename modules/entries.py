# This program turns decoded beacon packets into standardized data entry for SQL Server
# -*- coding: utf-8 -*-

PrimaryEntry = [
    ['Time',            'TIME'],
    ['SERCMag(x)',     ''],
    ['SERCMag(y)',     ''],
    ['SERCMag(z)',     ''],
    ['OmegaMag1(x)',   ''],
    ['OmegaMag1(y)',   ''],
    ['OmegaMag1(z)',   ''],
    ['Roll',            ''],
    ['Pitch',           ''],
    ['Yaw',             ''],
    ['Source',          '']
]

SecondaryEntry = [
    ['Time',                'TIME'],
    ['Gyro_1_Temp',         ''],
    ['Gyro_2_Temp',         ''],
    ['Gyro_3_Temp',         ''],
    ['V_DBB_Main_Cell',     ''],
    ['V_DBB_Daughterboard', ''],
    ['I_DBB_Main_Cell',     ''],
    ['I_DBB_Daughterboard', ''],
    ['Sun_Sensor_Temp',     ''],
    ['Solar_Panel_1_V',     ''],
    ['Solar_Panel_2_V',     ''],
    ['Solar_Panel_3_V',     ''],
    ['Solar_Panel_4_V',     ''],
    ['Solar_Panel_5_V',     ''],
    ['Solar_Panel_1_I',     ''],
    ['Solar_Panel_2_I',     ''],
    ['Solar_Panel_3_I',     ''],
    ['Solar_Panel_4_I',     ''],
    ['Solar_Panel_5_I',     ''],
    ['I_Pycube_3.3V',       ''],
    ['I_Pycube_5V',         ''],
    ['Battery_Bus',         ''],
    ['Battery_Current_Direction',''],
    ['Solar_Panel_T_Panel_1',''],
    ['Solar_Panel_T_Panel_2',''],
    ['Solar_Panel_T_Panel_3',''],
    ['Solar_Panel_T_Panel_4',''],
    ['Solar_Panel_T_Panel_5',''],
    ['T_DBB_Main_Cell',     ''],
    ['T_DBB_Daughterboard', ''],
    ['Reboot_Counter',      ''],
    ['Solar_Panel_1_I_H8',  ''],
    ['Solar_Panel_2_I_H8',  ''],
    ['Solar_Panel_3_I_H8',  ''],
    ['Solar_Panel_4_I_H8',  ''],
    ['Solar_Panel_5_I_H8',  ''],
    ['T_DBB_Main_Cell_H8',  ''],
    ['T_DBB_Daughterboard_H8',''],
    ['Source',              '']
]

primary_entry_rule = [
    # Packet Type 0
   [#Line       Mins Prior 
    [5,         0],
    [14,        5],
    [23,        11],
    [32,        16]
   ],
    # Packet Type 1
   [#Line       Mins Prior 
    [5,         23],
    [14,        28],
    [23,        33],
    [32,        37]
   ]
]

secondary_entry_rule = [
    # Packet Type 0
    #Line       Mins Prior 
    [41,        35],
    # Packet Type 1
    [41,        36],
    # Packet Type 2
    [5,         0]
]

# input packet time and change it to *mins prior
def get_time(curr, prior):
    temp = curr.split(':')
    tlist = []
    for t in temp:
        tlist.append(int(t))
    day, hour, minute = tlist
    minute -= prior
    while minute < 0:
        minute += 60
        hour -= 1
        if hour < 0:
            hour += 24
            day -= 1
            if day < 0: # way out of range
                day, hour, minute = 0, 0, 0
                break
    return str(day)+':'+str(hour)+':'+str(minute)
        
    

# returns a list of primary data entries
def get_primary_data(packet, source):
    packet_type = packet[2][1]
    curr_time = packet[4][1]
    answer_list = []
    if packet_type == 0 or packet_type == 1: # Beacon 1/2
        for rule in primary_entry_rule[packet_type]:
            starting_index = rule[0]
            modified_time = get_time(curr_time, rule[1])
            # FILL ENTRY
            new_entry = [modified_time]
            for i in range(9):
                new_entry.append(str(packet[starting_index+i][1]))
            new_entry.append(source)
            answer_list.append(new_entry)
    elif packet_type == 2: # Beacon 3
        pass # beacon3 does not contain primary data
    #print(answer_list)
    return answer_list

def get_secondary_data(packet, source):
    packet_type = packet[2][1]
    curr_time = packet[4][1]
    answer = []
    starting_index = secondary_entry_rule[packet_type][0]
    modified_time = get_time(curr_time, secondary_entry_rule[packet_type][1])
    answer.append(modified_time)
    if packet_type == 0: # Beacon 1
        for i in range(11):
            answer.append(str(packet[starting_index+i][1]))
        for i in range(26):
            answer.append('NULL')
    elif packet_type == 1: # Beacon 2
        for i in range(11):
            answer.append('NULL')
        for i in range(11):
            answer.append(str(packet[starting_index+i][1]))
        for i in range(15):
            answer.append('NULL')
    elif packet_type == 2: # Beacon 3
        for i in range(37):
            answer.append(str(packet[starting_index+i][1]))
    answer.append(source)
    return answer