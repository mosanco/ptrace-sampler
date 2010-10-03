#!/usr/bin/python

import sys
import time

from sample_reader import parseFile


outFd = None

def handleEvent (e):
    #print e

    outFd.write("# event at %s\n" % ( time.strftime('%c', time.localtime(e[0]) ) ) )

    # NumSamples
    for f in e[1]:
        if f[3] is not None:
            outFd.write("fl=%s\n" % f[3])
            outFd.write("fn=%s\n" % f[2])
            outFd.write("%d %d 0\n" % (f[4], 1))
            break

    # NumIncSamples
    outFd.write("# NumIncSamples\n")
    for f in e[1]:
        if f[3] is not None:
            outFd.write("fl=%s\n" % f[3])
            outFd.write("fn=%s\n" % f[2])
            outFd.write("%d 0 %d\n" % (f[4], 1))

    # function calls
    outFd.write("# function calls\n")
    currFrame = 1
    for f in e[1][1:]:
        if f[3] is not None:
            prevFrame = e[1][ currFrame-1 ]
            
            if prevFrame[4] is not None:
                outFd.write("fl=%s\n" % f[3])
                outFd.write("fn=%s\n" % f[2])
                outFd.write("cfl=%s\n" % prevFrame[3])
                outFd.write("cfn=%s\n" % prevFrame[2])
                outFd.write("calls=1 %d\n" % prevFrame[4])
                outFd.write("%d 1 0\n" % f[4])
                
            
            #outFd.write("%d 0 %d\n" % (f[4], 1))
        currFrame += 1

    outFd.write("\n")

    #sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <sample data file>" % sys.argv[0]
        sys.exit(1)

    sampleFile = sys.argv[1]

    outFd = open("calltree.%s" % sampleFile, "w")

    outFd.write("# callgrind output file, generated by '%s'\n" % sys.argv)
    outFd.write("events: NumSamples NumIncSamples\n")
    outFd.write("\n")

    parseFile(sampleFile, handleEvent)
