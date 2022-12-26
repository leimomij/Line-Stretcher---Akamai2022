#!/home/student1/miniconda3/envs/LLC/bin/python
#
#this program initializes the line length stretcher using the ADAM module 5056SO 

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from VVMsubs import vvmInit, VVM_MEAS
#from unittest import main
#import VVM
#import VVMsubs
#

# Some definitions
hostname = '128.171.166.181'
port = 502
UNIT = 0x1
WR = 0
CS = 1
A0 = 2
DB0 = 4

def fst_init(client):

    #W/R change from 0-1-0-1
    client.write_coils(WR, 0, unit=UNIT)
    client.write_coils(WR, 1, unit=UNIT)
    client.write_coils(WR, 0, unit=UNIT)
    client.write_coils(WR, 1, unit=UNIT)

    #DB0-DB11 from 0-1-0
    client.write_coils(DB0, [0]*12, unit=UNIT)
    client.write_coils(DB0, [1]*12, unit=UNIT)
    client.write_coils(DB0, [0]*12, unit=UNIT)

    #A0,A1 from 0-1-0
    client.write_coils(A0, [0]*2, unit=UNIT)
    client.write_coils(A0, [1]*2, unit=UNIT)
    client.write_coils(A0, [0]*2, unit=UNIT)

    #CS from 0-1-0-1
    client.write_coils(CS, 0, unit=UNIT)
    client.write_coils(CS, 1, unit=UNIT)
    client.write_coils(CS, 0, unit=UNIT)
    client.write_coils(CS, 1, unit=UNIT)


# client=ModbusClient(hostname,port)
# client.connect()
# fst_init(client)
# client.close()



ip ="128.171.166.190"
sockGPIB = vvmInit(ip)
phase, ba, apow, bpow = VVM_MEAS(sockGPIB)

print(phase,ba,apow,bpow)