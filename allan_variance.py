#!/home/student1/miniconda3/envs/LLC/bin/python

#this program reads in txt files of data from the VVM and creates
#an Allan Variance analysis (graph)

import allantools  #use allantools  
import matplotlib.pyplot as plot #use matplotlib
import pandas
import numpy

#going to want to do an Allan Variance on the raw phase data 
#without line stretcher, and then one with my algorithm controling
#line stretcher for same amount of time


path = "/home/corr/LLC_Akamai_2022/data/Phase_with_lineStretcher_280722_012703.csv"
#path = "/home/corr/LLC_Akamai_2022/GLT_phasestability_runs/2019-08-27 Phase Stability Run/GLT2hoursRealFR.xlsx"
#path = "/home/corr/LLC_Akamai_2022/GLT_phasestability_runs/2019-08-27 Phase Stability Run/PhaseMonitor_270819_215541.xlsx"
yaxis = "Phase"
xaxis = "Elapsed"
#"Elapsed"
#for phase: "Phase vs Time for GLT 8/27/2019"
#for Allan Variance: "Allan Deviation analysis for VVM data 7/8/22"
Allantitle = "Allan Deviation analysis for GLT data 8/27/19"
Phasetitle = "Phase v Time for GLT data 8/27/19"



def allan_plot(path, yaxis, xaxis, title):
    #Gdata = pandas.read_excel("/home/corr/LLC_Akamai_2022/GLT_phasestability_runs/2019-08-27 Phase Stability Run/PhaseMonitor_270819_215541.xlsx")
    Gdata=  pandas.read_csv(path)
    phase = list(Gdata[yaxis])
    phase.pop(0)
    time = list(Gdata[xaxis])
    time.pop(0)
    
    #convert phase error to time delay
    #math = phase error * pi/180 * 1/frequency = time delay
    phase_delay = []
    for i in range(len(phase)):
        phase_delay.append(phase[i]*((numpy.pi)/180.0)*1.0/(15.75*10**9)) #gives array of time delay in seconds

    #this is allentools function to create allan deviation
    (tau_out, adev, adeverr, n) = allantools.adev(phase_delay, rate=1.0, data_type="phase", taus=None)

    #avar = numpy.square(adev)
    print(adev)
    logavar = numpy.log10(adev)
    print(logavar)
    logtauout = numpy.log10(tau_out)
    print(logtauout)

    plot.figure(figsize=(10,10))
    plot.style.use('seaborn')
    plot.scatter(logtauout,logavar,marker=".",s=200,edgecolors="black",c="red")
    plot.title(title)
    plot.xlabel("log of time increments in seconds(tau)")
    plot.ylabel("log of variation in phase delay (sec/sec)")
    plot.show()
    


def phase_v_time(path, yaxis, xaxis, title): #function to plot phase v time, pass in the path that takes you to the data file
    #var = pandas.read_excel("PhaseMonitor_270819_215541.xlsx")
    
    #var = pandas.read_excel("/home/corr/LLC_Akamai_2022/GLT_phasestability_runs/2019-08-27 Phase Stability Run/PhaseMonitor_270819_215541.xlsx")
    var = pandas.read_csv(path)
    print(var)

    phase = list(var[yaxis])
    phase.pop(0)
    #mag = list(var["Mag"])
    #mag.pop(0)
    time = list(var[xaxis])
    time.pop(0)

    plot.figure(figsize=(10,10))
    plot.style.use('seaborn')
    plot.scatter(time,phase,marker=".",s=100,edgecolors="black",c="red")
    plot.title(title)
    plot.ylabel("Phase (degrees)")
    plot.xlabel("Time (seconds)")
    plot.show()


    

print("done")

#phase_v_time(path, yaxis, xaxis, Phasetitle)
allan_plot(path,yaxis,xaxis,Allantitle )