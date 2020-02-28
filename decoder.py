import numpy as np
# from gnuradio import gr
# import pmt
import sys
import struct
import binascii
import os.path
import scipy
import time
from datetime import datetime
import os, errno

# ---------------- AX.25 BEACON PACKET STRUCTURE---------------------------------------------------#

#	--			FLAG:	  		01111110...
#	 0			ADDRESS:  		19 Bytes		(ASCII)
#	19			CONTROL:  		3  Bytes		(2 Bytes | 00000011 - Frame Type: UI, PF=0)
#	22			PID:	  		1  Bytes		(11110000 - No layer 3 protocol implimented)
#	23			INFO:---- 		X  Bytes		(ASCII)
#	23+X		FCS:	|  		2  Bytes		(not yet dealt with...)
#	--	F		LAG:	|  		01111110...
#						|
#						|
#						'---------------INFO STRUCTURE-------------------------------------------------------------------#
#
#								0		HEADER:			12 Bytes		(ASCII)
#								12		LENGHT:			4  Bytes		(Length of TYPE + PAGE ADDRESS + DATA Sections)
#								16		TYPE:			2  Bytes		(Beacon 1 = 60, Beacon 7 = 66)
#								18		PAGE ADDRESS:	2  Bytes		(
#								20		DATA:			X  Bytes		(Returned from decoder functions)
#								20+X	CRC:			2  Bytes		(


import struct

# Column 1: Variable Name
# Column 2: Type of stage 1 decdoding (numerical or meaning). For exmaple, from hex to int, or from hex to time.
# Column 3: Type of stage 2 (meaning or none) decoding. For example, from int to reboot cause, or from time to time (no change)

# Both stage 1 and stage 2 decoding can be omitted. A '0' is used in this case.


#		Column 1						Column 2	Column 3
# MAGNETO BEACONS
BeaconStructures = [
    #Beacon 1

  [
    #Header
    # C
    ['Title',                           'Ti',        '0'],
    ['Length',                          'H',         '0'],
    ['Packet type',                     'B',         '0'],
    ['Page_Address',                    'No',        '0'],
    ['Time',                            't',         '0'],
    ['SERCMagC (x)',                    'H',         'Conv1'],
    ['SERCMagC (y)',                    'H',         'Conv1'],
    ['SERCMagC (z)',                    'H',         'Conv1'],
    ['OmegaMag1C (x)',                  'H',         'Conv1'],
    ['OmegaMag1C (y)',                  'H',         'Conv1'],
    ['OmegaMag1C (z)',                  'H',         'Conv1'],
    ['RollC',                           'H',         '0'],
    ['PitchC',                          'H',         '0'],
    ['YawC',                            'H',         '0'],
    #figure out header

    #H1: 5 mins prior
    ['SERCMagH1 (x)',                    'H',         'Conv1'],
    ['SERCMagH1 (y)',                    'H',         'Conv1'],
    ['SERCMagH1 (z)',                    'H',         'Conv1'],
    ['OmegaMag2H1 (x)',                  'H',         'Conv1'],
    ['OmegaMag2H1 (y)',                  'H',         'Conv1'],
    ['OmegaMag2H1 (z)',                  'H',         'Conv1'],
    ['RollH1',                           'H',         '0'],
    ['PitchH1',                          'H',         '0'],
    ['YawH1',                            'H',         '0'],
    #H2: 11 mins prior
    ['SERCMagH2 (x)',                    'H',         'Conv1'],
    ['SERCMagH2 (y)',                    'H',         'Conv1'],
    ['SERCMagH2 (z)',                    'H',         'Conv1'],
    ['OmegaMag1H2 (x)',                  'H',         'Conv1'],
    ['OmegaMag1H2 (y)',                  'H',         'Conv1'],
    ['OmegaMag1H2 (z)',                  'H',         'Conv1'],
    ['RollH2',                           'H',         '0'],
    ['PitchH2',                          'H',         '0'],
    ['YawH2',                            'H',         '0'],
    #H3: 16 mins prior
    ['SERCMagH3 (x)',                    'H',         'Conv1'],
    ['SERCMagH3 (y)',                    'H',         'Conv1'],
    ['SERCMagH3 (z)',                    'H',         'Conv1'],
    ['OmegaMag2H3 (x)',                  'H',         'Conv1'],
    ['OmegaMag2H3 (y)',                  'H',         'Conv1'],
    ['OmegaMag2H3 (z)',                  'H',         'Conv1'],
    ['RollH3',                           'H',         '0'],
    ['PitchH3',                          'H',         '0'],
    ['YawH3',                            'H',         '0'],
    #H3B: 35 mins prior
    ['Gyro 1 Temp H3B',                  'H',         'Conv2'],
    ['Gyro 2 Temp H3B',                  'H',         'Conv2'],
    ['Gyro 3 Temp H3B',                  'H',         'Conv2'],
    ['V DBB Main Cell H3B',              'H',         'Conv1'],
    ['V DBB Daughterboard H3B',          'H',         'Conv1'],
    ['I DBB Main Cell H3B',              'H',         'Conv2'],
    ['I DBB Daughterboard H3B',          'H',         'Conv2'],
    ['Sun Sensor Temp H3B',              'H',         'Conv2'],
    ['Solar Panel 1 V H3B',              'H',         'Conv1'],
    ['Solar Panel 2 V H3B',              'H',         'Conv1'],
    ['Solar Panel 3 V H3B',              'H',         'Conv1'],
    ['Check Sum',                        'No',         '0'],
  ],

# Beacon 2
    #H4: 23 mins prior
  [
    ['Title',                            'Ti', '0'],
    ['Length',                           'H', '0'],
    ['Packet type',                      'B', '0'],
    ['Page_Address',                     'No', '0'],
    ['Time',                             't', '0'],
    ['SERCMagH4 (x)',                    'H',         'Conv1'],
    ['SERCMagH4 (y)',                    'H',         'Conv1'],
    ['SERCMagH4 (z)',                    'H',         'Conv1'],
    ['OmegaMag1H4 (x)',                  'H',         'Conv1'],
    ['OmegaMag1H4 (y)',                  'H',         'Conv1'],
    ['OmegaMag1H4 (z)',                  'H',         'Conv1'],
    ['RollH4',                           'H',         '0'],
    ['PitchH4',                          'H',         '0'],
    ['YawH4',                            'H',         '0'],
    #figure out header

    #H5: 28 mins prior
    ['SERCMagH5 (x)',                    'H',         'Conv1'],
    ['SERCMagH5 (y)',                    'H',         'Conv1'],
    ['SERCMagH5 (z)',                    'H',         'Conv1'],
    ['OmegaMag2H5 (x)',                  'H',         'Conv1'],
    ['OmegaMag2H5 (y)',                  'H',         'Conv1'],
    ['OmegaMag2H5 (z)',                  'H',         'Conv1'],
    ['RollH5',                           'H',         '0'],
    ['PitchH5',                          'H',         '0'],
    ['YawH5',                            'H',         '0'],
    #H6: 33 mins prior
    ['SERCMagH6 (x)',                    'H',         'Conv1'],
    ['SERCMagH6 (y)',                    'H',         'Conv1'],
    ['SERCMagH6 (z)',                    'H',         'Conv1'],
    ['OmegaMag1H6 (x)',                  'H',         'Conv1'],
    ['OmegaMag1H6 (y)',                  'H',         'Conv1'],
    ['OmegaMag1H6 (z)',                  'H',         'Conv1'],
    ['RollH6',                           'H',         '0'],
    ['PitchH6',                          'H',         '0'],
    ['YawH6',                            'H',         '0'],
    #H7: 37 mins prior
    ['SERCMagH7 (x)',                    'H',         'Conv1'],
    ['SERCMagH7 (y)',                    'H',         'Conv1'],
    ['SERCMagH7 (z)',                    'H',         'Conv1'],
    ['OmegaMag2H7 (x)',                  'H',         'Conv1'],
    ['OmegaMag2H7 (y)',                  'H',         'Conv1'],
    ['OmegaMag2H7 (z)',                  'H',         'Conv1'],
    ['RollH7',                           'H',         '0'],
    ['PitchH7',                          'H',         '0'],
    ['YawH7',                            'H',         '0'],
    #H7B: 36 mins prior
    ['Solar Panel 4 V H7B',              'H',         'Conv2'],
    ['Solar Panel 5 V H7B',              'H',         'Conv2'],
    ['Solar Panel 1 I H7B',              'H',         'Conv2'],
    ['Solar Panel 2 I H7B',              'H',         'Conv2'],
    ['Solar Panel 3 I H7B',              'H',         'Conv2'],
    ['Solar Panel 4 I H7B',              'H',         'Conv2'],
    ['Solar Panel 5 I H7B',              'H',         'Conv2'],
    ['I Pycube 3.3V H7B',                'H',         'Conv2'],
    ['I Pycube 5V H7B',                  'H',         'Conv2'],
    ['Battery Bus H7B',                  'H',         'Conv2'],
    ['Battery Current Direction H7B',    'H',         '0'],
    ['Check Sum',                        'No',        '0'],
  ],

# Beacon 3
  [
    ['Title', 'Ti', '0'],
    ['Length', 'H', '0'],
    ['Packet type', 'B', '0'],
    ['Page_Address', 'No', '0'],
    ['Time', 't', '0'],
    ['Gyro 1 Temp',                      'H',         'Conv2'],
    ['Gyro 2 Temp',                      'H',         'Conv2'],
    ['Gyro 3 Temp',                      'H',         'Conv2'],
    ['V DBB Main Cell',                  'H',         'Conv1'],
    ['V DBB Daughterboard',              'H',         'Conv1'],
    ['I DBB Main Cell',                  'H',         'Conv2'],
    ['I DBB Daughterboard',              'H',         'Conv2'],
    ['Sun Sensor Temp',                  'H',         'Conv2'],
    ['Solar Panel 1 V',                  'H',         'Conv1'],
    ['Solar Panel 2 V',                  'H',         'Conv1'],
    ['Solar Panel 3 V',                  'H',         'Conv1'],
    ['Solar Panel 4 V',                  'H',         'Conv1'],
    ['Solar Panel 5 V',                  'H',         'Conv1'],
    ['Solar Panel 1 I',                  'H',         'Conv2'],
    ['Solar Panel 2 I',                  'H',         'Conv2'],
    ['Solar Panel 3 I',                  'H',         'Conv2'],
    ['Solar Panel 4 I',                  'H',         'Conv2'],
    ['Solar Panel 5 I',                  'H',         'Conv2'],
    ['I Pycube 3.3V',                    'H',         'Conv2'],
    ['I Pycube 5V',                      'H',         'Conv2'],
    ['Battery Bus',                      'H',         'Conv2'],
    ['Battery Current Direction',        'H',         '0'],
    ['Solar Panel T Panel 1',            'H',         'Conv2'],
    ['Solar Panel T Panel 2',            'H',         'Conv2'],
    ['Solar Panel T Panel 3',            'H',         'Conv2'],
    ['Solar Panel T Panel 4',            'H',         'Conv2'],
    ['Solar Panel T Panel 5',            'H',         'Conv2'],
    ['T DBB Main Cell',                  'H',         'Conv2'],
    ['T DBB Daughterboard',              'H',         'Conv2'],
    ['Reboot Counter',                   'H',         '0'],
    #H8
    ['Solar Panel 1 I H8', 'H', 'Conv2'],
    ['Solar Panel 2 I H8', 'H', 'Conv2'],
    ['Solar Panel 3 I H8', 'H', 'Conv2'],
    ['Solar Panel 4 I H8', 'H', 'Conv2'],
    ['Solar Panel 5 I H8', 'H', 'Conv2'],
    ['T DBB Main Cell H8', 'H', 'Conv2'],
    ['T DBB Daughterboard H8', 'H', 'Conv2'],
    ['Check Sum', 'No', '0'],
  ],
]



# Decoding type lengths, in bytes (real bytes, not ASCII hex bytes)
decodeLengths = {
'f': 2,
'H': 2,
'r': 2,
't': 3,
'B': 1,
'0': 0,
'Ti':7,
'No':2,
}

def getDecodeLength(elementType):
    try:
        decodeLength = decodeLengths[elementType]
    except:
        decodeLength = int(elementType)
    return decodeLength


def decodeElement(element, elementType):
    switcher = {
        'ch': decodeChar,
        'f': decodeNum,
        'H': decodeNum,
        'B': decodeNum,
        'r': decodeReboot,
        't': decodeTime,
        '0': decodeNone,
        'z': decodeNone,
        'Ti': decodeChar,
        'L': decodeNum,
        'No': decodeNone,
        'Conv1': decodeConvert1,
        'Conv2': decodeConvert2,
    }
    decoder = switcher.get(elementType, decodeNone)
    return decoder(element, elementType)

def decodeChar(element, elementType):
    return element.decode("hex")

def decodeNum(element, elementType):
    ident = '<' + elementType  # changed to little endian '<' from big endian '>' (RR, 04/03/2019)
    return struct.unpack(ident, element.decode('hex'))[0]


def decodeNumBig(element, elementType):
    ident = '>' + elementType  # allows decoding of big endian data
    return struct.unpack(ident, element.decode('hex'))[0]

def decodeReboot(rebootReason_num, elementType):
    switcher = {
        0: "RESTART_POWER_UP",
        1: "RESTART_BROWNOUT",
        4: "RESTART_WATCHDOG",
        6: "RESTART_SOFTWARE",
        7: "RESTART_MCLR",
        14: "RESTART_ILLEGAL_OP",
        15: "RESTART_TRAP_CONFLICT",
    }
    return switcher.get(rebootReason_num)

def getReebootReason(reebootReason_num):
    switcher = {
        0: "RESTART_POWER_UP",
        1: "RESTART_BROWNOUT",
        4: "RESTART_WATCHDOG",
        6: "RESTART_SOFTWARE",
        7: "RESTART_MCLR",
        14: "RESTART_ILLEGAL_OP",
        15: "RESTART_TRAP_CONFLICT",
    }
    return switcher.get(reebootReason_num)

def decodeConvert1(element,elementType):

    return float(element)/100

def decodeConvert2(element,elementType):
    return float(element)/10

def decodeTime(element, elementType):
    return str(decodeNum(element[0:2], 'B')) + ':' + str(decodeNum(element[2:4], 'B')) \
           + ':' + str(decodeNum(element[4:6], 'B'))

def decodeNone(element, elementType):
    return element

# What are those missions called?


def decodeBeacon(packet, type_):
    # Switch-Case statement for beacon decoders
    # self.add_to_debug('Beacon type', str(type_))
    print("Type: {}".format(type_))
    # Beacons types are 1 - 7 inc.
    # They are sent as 60 - 66 inc.
    type_ -=0
    if type_ < 0 or type_ > 3:
        print("Invalid Beacon Type!")
    else:
        # if type_ <=4: packet = packet[12:] # Hack to skip the extra 12 characters that the lower PPM adds to it's beacon packets (Removed by RR - Fixed on Satellite End 04/05/2019)
        print("Beacon {} identified.".format(type_))
        BeaconStructure = BeaconStructures[type_ ]
        len_BeaconStructure = len(BeaconStructure)

        expectedPacketLength = 0
        packetLength = len(packet)
        for i in range(len_BeaconStructure):
            expectedPacketLength += getDecodeLength(BeaconStructure[i][1]) * 2
        print('Packet Length to Decode: {}'.format(packetLength))
        print('Expected packet Length: {}'.format(expectedPacketLength))
        if expectedPacketLength != packetLength:
            print('Packet Length not as expected.')

        DecodedElements = [[0 for i in range(2)] for j in range(len_BeaconStructure)]
        p = 0
        for i in range(len_BeaconStructure):  # Iterate through telemetry elements
            DecodedElements[i][0] = BeaconStructure[i][0]
            elementType = BeaconStructure[i][1]
            val_len = getDecodeLength(elementType) * 2
            DecodedElements[i][1] = decodeElement(packet[p:p + val_len], elementType)
            elementType = BeaconStructure[i][2]
            DecodedElements[i][1] = decodeElement(DecodedElements[i][1], elementType)
            '''
            try:
                DecodedElements[i][1] = decodeElement(packet[p:p + val_len], elementType)
                elementType = BeaconStructure[i][2]
                DecodedElements[i][1] = decodeElement(DecodedElements[i][1], elementType)
            except:
                print("Error decoding element {} of beacon {}.".format(i, type_))
                DecodedElements[i][1] = "Error!"
            '''
            p += val_len
    return DecodedElements


def getPrintableBeacon(DecodedElements):
    printable = ''
    type_ = DecodedElements[1]
    max_len = 0
    for i in range(len(DecodedElements)):
        max_len = max(max_len, len(DecodedElements[i][0]))
    for i in range(len(DecodedElements)):
        spaces = ' ' + '.' * (max_len - len(DecodedElements[i][0]) + 2) + ' '
        printable += '{}:{}{}\n'.format(
            str(DecodedElements[i][0]),
            spaces,
            str(DecodedElements[i][1]))
    return printable


def getDisplayableBeacon(DecodedElements):
    displayable = ''
    type_ = DecodedElements[1]
    max_len = 0
    for i in range(len(DecodedElements)):
        spaces = '\n    '
        displayable += '{}:{}{}\n'.format(
            str(DecodedElements[i][0]),
            spaces,
            str(DecodedElements[i][1]))
    return displayable

f = open("B0EncodedSample.txt", "r")
EncodedElements=f.readline()

decoded = decodeBeacon(EncodedElements,0)
print(getPrintableBeacon(decoded))
