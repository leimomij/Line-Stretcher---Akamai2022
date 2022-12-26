#!/home/corr/miniconda3/envs/LLC/bin/python
#
import time
import datetime
import sys, traceback
from VVMsubs import vvmInit, VVM_MEAS

def main():
    try:
        ip="128.171.166.190"
        tottime=int(sys.argv[1])
        sockGPIB = vvmInit(ip)

        timenow=datetime.datetime.utcnow().strftime("%d%m%y_%H%M%S")
        #outfilename="data/"+"Phase" + "_"  + timenow + '.txt'
        outfilename="data/"+"Phase" + "_"  + timenow + '.csv'

        with open("7_18_22VVMdata","a") as outfile:
            outfile.write("%s\n" % (outfilename))

        timecount=0

        print("Writing data to: ",outfilename)
        for i in range(tottime):
            phase, ba, apow, bpow = VVM_MEAS(sockGPIB)
            timeWritetoFile=datetime.datetime.utcnow().strftime("%Y/%m/%d_%H:%M:%S")
            currtime = time.time()
            with open(outfilename,"a") as outfile:
                #outfile.write('%30s %15.6f %20s %20s %20s %20s\n' % (timeWritetoFile, currtime, phase, ba, apow, bpow))
                outfile.write('%s,%f,%s,%s,%s,%s\n' % (timeWritetoFile, currtime, phase, ba, apow, bpow))

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
