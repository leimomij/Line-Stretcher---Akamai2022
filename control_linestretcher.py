#!/home/corr/miniconda3/envs/LLC/bin/python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from VVMsubs import vvmInit, VVM_MEAS
from load_adamdata import send_to_adam


#this is the main control program for the line stretcher (algorithm)
ip ="128.171.166.190"
sockGPIB = vvmInit(ip)

#initialize line stretcher to set point (8190):
send_to_adam(4095, 1)
send_to_adam(4095, 2)
send_to_adam(0, 3)
send_to_adam(0, 4)

dt = 5 #cycle time of the PID controller in seconds

def main():

    #we want the phase to stay at or near "zero" so we can check 
    #between readings if the phase has drifted, and if yes, inch 
    #it up or down toward zero

    #we do this by sending the current phase readings through a software PID controller
    #the output of this we send to the line stretcher

    #loop
    #read in current phase value
    #check if less than or greater than zero
        #if less, increment up
        #if greater, increment down

        #do this by passing a decimal number to load_adamdata.py
        #must also select channel and pass to load_adamdata.py
        #the channels are 1,2,3 or 4
        #each channel can be controlled individually
        #but we really have 0-16380 amount of precsion

    #while loop: (or for loop for 6 hrs)

    preverror = 0
    It = 0
    for i in range(dt): #not sure about this timing

        phase, ba, apow, bpow = VVM_MEAS(sockGPIB) #read in data from the VVM
        print(phase,ba,apow,bpow)  

        p = float(phase) #convert the scientfic notation to float
        print(p)

        #should have line stretcher zeroed at 50% stretch

        #convert phase value to linestretcher decimal (PV = process value)
        PV = phase_to_decimal(p)
        print(PV)
       
    #PID controller

        SP = 8190 #the setpoint for the line stretcher
        Kp = 1   #the proportional gain
        Ki = 0  #the integral gain
        Kd = 0   #the derivative gain
        
        error = SP-PV
        #print(error)

        P = Kp*error
        It = It + error*Ki*dt
        D = Kd*(preverror-error)/dt

        preverror = error

        output = P + It + D #the output is how much the value needs to be corrected from the PV to reach SP
        print("the output of PID is " + str(output))

        if output <= -16380 or output >= 16380:
            adjust = PV
        else: 
            adjust = PV + output 
        print("the corrected amount is " + str(adjust))

    if adjust <= 0:
        send_to_adam(0, 1)
        send_to_adam(0, 2)
        send_to_adam(0, 3)
        send_to_adam(0, 4)
    
    if adjust >= 16380: #should it be 16383? 4096*4-1 (for the 0th place)
        send_to_adam(4095, 1)
        send_to_adam(4095, 2)
        send_to_adam(4095, 3)
        send_to_adam(4095, 4)

    if adjust <= 4095:
        send_to_adam(adjust, 1)
    if 4095 < adjust <= 8190:
        send_to_adam(4095, 1)
        send_to_adam(adjust-4095, 2)
    if 8190 < adjust <= 12285:
        send_to_adam(4095, 1)
        send_to_adam(4095, 2)
        send_to_adam(adjust-8190, 3)
    if 12285 < adjust < 16380:
        send_to_adam(4095, 1)
        send_to_adam(4095, 2)
        send_to_adam(4095, 3)
        send_to_adam(adjust-12285, 4)

        

       
    
def phase_to_decimal(phase):
    #phase setpoint = 0, range = +/- 180 degrees. Convert this into units for the PID and line stretcher

    #0-16380 - set point = 8190
    #-180-180 - set point = 0

    #math for converting phase to line stretcher decimal
    if phase == 0:
        decimal = 8190
    if phase < 0:
        decimal = 8190 - phase*(-45.5)
    if phase > 0:
        decimal = 8190 + phase*(45.5)

    return decimal


main()

#test out find out how much ls unit corresponds to phase (could be more than 360 deg)