#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:51:24 2020

fpqTraceLengthLogLog

log-log plot of trace lengths, from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    -Bn, number of bins  

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import sys 
import numpy as np 

#   defaults 
CM2INCHES = 0.3937 
bGrid = False 
nBins = 20  
xSize = 15.0 * CM2INCHES 
ySize = 15.0 * CM2INCHES   

#   process command line arguments; filename is mandatory 
bFilename = False 
for sArg in sys.argv[1:]:   
    #   input data file 
    if "-I" in sArg:
        fn = sArg[2:]
        bFilename = True 
    #   number of bins 
    if "-B" in sArg:
        nBins = int(sArg[2:])
        
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqTraceLengthLogLog.py -I<inputfilename>')

#   get nodes and lengths 
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
tracelengths = fpq.getTraceLengths(xnodelist, ynodelist)
nTraces = len(tracelengths)
incTraceLength = (max(tracelengths)-min(tracelengths))/nBins
traceBins = np.arange(min(tracelengths), 
                      max(tracelengths)+2*incTraceLength, 
                      incTraceLength)
nlog, binlog = plt.histogram(tracelengths, bins=traceBins)

#   plot the segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
plt.loglog(binlog[0:-1], nlog, 'o')
plt.xlabel('Trace length, pixels')
plt.ylabel('Count')
plt.xlim(min(tracelengths)*.9, max(tracelengths)*1.1)
plt.grid(True, which='both')
plt.title('Trace length density distribution, n=%i' % nTraces)
plt.savefig("fpqTraceLengthLogLogDensity.png", dpi=600)

traceBins = np.arange(min(tracelengths), 
                      max(tracelengths)+2*incTraceLength, 
                      1)
nlog, binlog = plt.histogram(tracelengths, bins=traceBins)
cumsum = np.cumsum(nlog)
#   plot the cumulative segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
plt.loglog(binlog[0:-1], max(cumsum)-cumsum, 'o')
plt.xlabel('Trace length, pixels')
plt.ylabel('Count')
plt.xlim(min(tracelengths)*.9, max(tracelengths)*1.1)
plt.grid(True, which='both')
plt.title('Trace length cumulative distribution, n=%i' % nTraces)
plt.savefig("fpqTraceLengthLogLogCumulative.png", dpi=600)


print('Plotted %5d traces & lengths' % nTraces)
