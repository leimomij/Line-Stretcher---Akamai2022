#!/home/corr/miniconda3/envs/LLC/bin/python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from VVMsubs import vvmInit, VVM_MEAS

import time

#this program will load data to the adam to control the line stretcher
#it will do this by intaking a decimal number (0-4095)
#converting it to a 12 bit binary number
#reversing it, and sending it to the ADAM

#do I need all this?
hostname = '128.171.166.181'
port = 502
UNIT = 0x1
WR = 0
CS = 1
A0 = 2
A1 = 3
DB0 = 4
DB1 = 5
DB2 = 6
DB3 = 7
DB4 = 8
DB5 = 9
DB6 = 10
DB7 = 11
DB8 = 12
DB9 = 13
DB10 = 14
DB11 = 15

decimal = 0
channel = 1


def send_to_adam(decimal, channel):
    #this function converts the decimal number passed in to a 
    #12 bit binary number
    #decimal should be a decimal number from 0-4095

    #convert decimal to 12 bit binary here
    binary = (bin(decimal)[2:])
    
    #turn binary int into array
    binary_array = list(map(int, str(binary)))

    #flip it around
    flipped = binary_array[::-1]

    #turn into 12 bit number
    for i in range(12-len(flipped)):
        flipped.append(0)

    #call all functions to load data per the manual
    load_data_mode()
    time.sleep(0.1)
    load_data(flipped)
    select_channel(channel)
    chip_select()

    time.sleep(0.1)
    client.write_coils(WR, [1], unit=UNIT)
    time.sleep(0.1)
   


#create a function for each step in the manual a,b,c,d

def load_data_mode():
    #step a: change W/R from 1(default) to 0(load data mode)
    time.sleep(0.1)
    client.write_coils(WR, [0], unit=UNIT)
    time.sleep(0.1)

def load_data(flipped):
    #takes in 12 bit binary number and loads it to DB0-DB11

    #step b: load data to DB0-DB11
    
    ports = [DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7, DB8, DB9, DB10, DB11]
    
    # for i in range(12):
    #     if flipped[i] == 0:
    #         client.write_coils(ports[i], [0], unit=UNIT)
    #     else:
    #         client.write_coils(ports[i], [1], unit=UNIT)
    time.sleep(0.1)
    client.write_coils(DB0,flipped,unit=UNIT)
    time.sleep(0.1)


def select_channel(channel):
    #takes in channel number and sets A0 and A1 accordingly

    #step c: set A1, A0 to select output channel
    # channel  A1   A0
    #    1      0    0
    #    2      0    1
    #    3      1    0
    #    4      1    1
    
    if (channel == 1):
        client.write_coils(A0, [0,0], unit=UNIT)
        time.sleep(0.1)
    if (channel == 2):
        client.write_coils(A0, [1,0], unit=UNIT)
        time.sleep(0.1)
    if (channel == 3):
        client.write_coils(A0, [0,1], unit=UNIT)
        time.sleep(0.1)
    if (channel == 4):
        client.write_coils(A0, [1,1], unit=UNIT)
        time.sleep(0.1)

def chip_select():
    #step d: change C/S (chip select) from 1(default) to 0(select chip)
    #and back to 1 again. 

    client.write_coils(CS, [0], unit=UNIT)
    time.sleep(0.1)
    client.write_coils(CS, [1], unit=UNIT)
    time.sleep(0.1)




client=ModbusClient(hostname,port)
time.sleep(0.1)
client.connect()  
time.sleep(0.1)
send_to_adam(decimal,channel)
time.sleep(0.1)
client.close()

#write_holding_registers(channel, 16bit)
#channel 0 1 2 3 
#16 bit- could only do half of this, since output is 10V and ls can only take 5V


