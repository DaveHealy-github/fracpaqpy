#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:12:03 2020

fpqSegmentLengthLogLog.py

log-log plot of segment lengths, from an input file of x,y nodes 

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
bGrid = True 
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
    sys.exit('Usage: python3 fpqSegmentLengthLogLog.py -I<inputfilename>')

#   get nodes and lengths 
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
seglengths = fpq.getSegLengths(xnodelist, ynodelist)
nTraces = len(seglengths)
incSegLength = (max(seglengths)-min(seglengths))/nBins
segBins = np.arange(min(seglengths), 
                      max(seglengths)+2*incSegLength, 
                      incSegLength)
nlog, binlog = plt.histogram(seglengths, bins=segBins)

#   plot the segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
plt.loglog(binlog[0:-1], nlog, 'o')
plt.xlabel('Trace length, pixels')
plt.ylabel('Count')
plt.xlim(min(seglengths)*.95, max(seglengths)*1.05)
plt.grid(True, which='both')
plt.title('Segment length distribution, n=%i' % nTraces)
plt.savefig("fpqSegmentLengthLogLogDensity.png", dpi=600)

segBins = np.arange(min(seglengths), 
                      max(seglengths)+2*incSegLength, 
                      1)
nlog, binlog = plt.histogram(seglengths, bins=segBins)
cumsum = np.cumsum(nlog)
#   plot the cumulative segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
plt.loglog(binlog[0:-1], max(cumsum)-cumsum, 'o')
plt.xlabel('Trace length, pixels')
plt.ylabel('Count')
plt.xlim(min(seglengths)*.9, max(seglengths)*1.1)
plt.grid(True, which='both')
plt.title('Segment length cumulative distribution, n=%i' % nTraces)
plt.savefig("fpqSegmentLengthLogLogCumulative.png", dpi=600)

print('Plotted %5d segments & lengths' % nTraces)
