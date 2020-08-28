#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:51:24 2020

fpqTraceLengthHist

plots a histogram of trace lengths, from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    -Bn, number of bins  

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import sys 

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
    #   grid on 
    if "-G" in sArg: 
        bGrid = True 
    #   number of bins 
    if "-B" in sArg:
        nBins = int(sArg[2:])
        
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqTraceLengthHist.py -I<inputfilename>')

#   get nodes and lengths 
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
tracelengths = fpq.getTraceLengths(xnodelist, ynodelist)
nTraces = len(tracelengths)

#   plot the segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
n, b, p = ax.hist(tracelengths, nBins)
ax.set_ylim(0, max(n)*1.05)
ax.set_xlabel('Trace length, pixels')
ax.set_ylabel('Count')
ax.set_xlim(0, max(tracelengths))
ax.grid(bGrid)
ax2 = ax.twinx()
ax2.set_ylim(0, (max(n)*1.05/nTraces)*100)
ax2.set_ylabel('Frequency, %')
plt.title('Trace length distribution, n=%i' % nTraces)
plt.savefig("fpqTraceLengthHist.png", dpi=600)

print('Plotted %5d traces & lengths' % nTraces)
