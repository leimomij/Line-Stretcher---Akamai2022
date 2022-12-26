#!/home/corr/miniconda3/envs/LLC/bin/python
#
import os
import os.path
import array
import time
import datetime
import socket
import numpy
import subprocess
import glob, os, sys
import shutil
import sys, traceback

# Special characters to be escaped
LF   = 0x0A
CR   = 0x0D
ESC  = 0x1B
PLUS = 0x2B

def vvmInit(ip):
    try:

        # Open TCP connect to port 1234 of GPIB-ETHERNET
        sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        print('GPIB Socket Created')

        sockGPIB.settimeout(1.0)
        sockGPIB.connect((ip, 1234))

        print('Socket connected to GPIB device')

        # Set mode as CONTROLLER
        sockGPIB.send("++mode 1\n".encode())

        print('set mode as controller')

        # Set HP33120A address
        #sockGPIB.send("++addr " + addr + "\n")

        #	print 'set gpib address'

        # Turn off read-after-write to avoid "Query Unterminated" errors
        sockGPIB.send("++auto 0\n".encode())

        # Read timeout is 500 msec
        sockGPIB.send("++read_tmo_ms 500\n".encode())

        # Do not append CR or LF to GPIB data
        sockGPIB.send("++eos 3\n".encode())

        # Assert EOI with last byte to indicate end of data
        sockGPIB.send("++eoi 1\n".encode())

        cmd = "*CLS\n"
        print(cmd)
        sockGPIB.send(cmd.encode())
        time.sleep(1.0)
        CheckError(sockGPIB)

        cmd = "*IDN?\n"
        print(cmd)
        sockGPIB.send(cmd.encode())
        sockGPIB.send("++read eoi\n".encode())
        time.sleep(1.0)

        try:
            s = sockGPIB.recv(4096)
        except socket.timeout:
            s = ""

        print(s)

        cmd = "*RST\n"
        print(cmd)
        sockGPIB.send(cmd.encode())
        time.sleep(1.0)
        CheckError(sockGPIB)

        cmd = "AVER:COUN 0\n"
        print(cmd)
        sockGPIB.send(cmd.encode())
        time.sleep(1.0)
        CheckError(sockGPIB)

        cmd = "SYST:FORM ASCII\n"
        print(cmd)
        sockGPIB.send(cmd.encode())
        time.sleep(1.0)
        CheckError(sockGPIB)

        # cmd = "DISP:STAT OFF"
        # print cmd
        # sockGPIB.send(cmd + "\n")
        # time.sleep(1.0)
        # CheckError(sockGPIB)
    except socket.error as e:
        print(e)

    return sockGPIB

#==============================================================================
def IsSpecial(data):
    return data in (LF, CR, ESC, PLUS)


#==============================================================================
def CheckError(sockGPIB):
    sockGPIB.send("SYST:ERR?\n".encode())
    sockGPIB.send("++read eoi\n".encode())

    s = None

    try:
        s = sockGPIB.recv(4096)
    except socket.timeout:
        s = ""

    print(s)
#=====================================================================================

def vvmReadVal(param,sockGPIB):
    cmd = "SENSE "+str(param)+"\n"
    sockGPIB.send(cmd.encode())
    cmd = "MEAS? "+str(param) + "\n"
    # print cmd
    sockGPIB.send(cmd.encode())
    sockGPIB.send("++read eoi\n".encode())
    # time.sleep(0.5)
    # CheckError(sockGPIB)

    try:
        paramval = sockGPIB.recv(8192).decode().rstrip('\r\n')
    except socket.timeout:
        paramval = ""
    time.sleep(0.01)
    return paramval

# Starting measurements on VVM

def VVM_MEAS(sockGPIB):
    sockGPIB.send("FORM POL\n".encode())
    phase = vvmReadVal("PHASE",sockGPIB)

    sockGPIB.send("FORM LOG\n".encode())
    ba = vvmReadVal("BA",sockGPIB)
    apow = vvmReadVal("APOW",sockGPIB)
    bpow = vvmReadVal("BPOW",sockGPIB)

    return phase, ba, apow, bpow

def main():
    try:
        ip="128.171.166.190"
        tottime=int(sys.argv[1])
        sockGPIB = vvmInit(ip)

        timenow=datetime.datetime.utcnow().strftime("%d%m%y_%H%M%S")
        outfilename="data/"+"Phase" + "_"  + timenow + '.txt'
        timecount=0

        for i in range(tottime):
            phase, ba, apow, bpow = VVM_MEAS(sockGPIB)
            timeWritetoFile=datetime.datetime.utcnow().strftime("%Y/%m/%d_%H:%M:%S")
            currtime = time.time()
            with open(outfilename,"a") as outfile:
                outfile.write('%30s %15.6f %20s %20s %20s %20s\n' % (timeWritetoFile, currtime, phase, ba, apow, bpow))

            timecount=timecount+1
            time.sleep(0.76)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        sockGPIB.close()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

#==============================================================================
if __name__ == '__main__':
    main()
