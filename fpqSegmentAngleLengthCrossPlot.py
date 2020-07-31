#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:14:40 2020

fpqSegmentAngleLengthCrossPlot.py

plots a histogram of segment angles, from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    -G, grid on   

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
        
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqSegmentAngleLengthCrossPlot.py -I<inputfilename>')

#   alternative method 
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
segangle = fpq.getSegAngles(xnodelist, ynodelist)
seglengths = fpq.getSegLengths(xnodelist, ynodelist)
nSegs = len(segangle)

#   plot the segment length distribution 
fig, ax = plt.subplots(figsize=(xSize,ySize))
plt.plot(segangle, seglengths, 'o')
plt.xlabel('Segment angle, degrees')
plt.ylabel('Segment length, pixels')
plt.xlim(0, 180)
plt.ylim(0, max(seglengths)*1.05)
plt.grid(bGrid)
plt.title('Segment angles versus lengths, n=%i' % nSegs)
plt.savefig("fpqSegmentAngleLengthCrossPlot.png", dpi=600)

print('Plotted %5d segments, angles & lengths' % nSegs)