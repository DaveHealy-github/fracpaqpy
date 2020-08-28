#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:43:14 2020

fpqSegmentAngleRose.py 

plots a rose plot of segment angles, from an input file of x,y nodes 

input:
    -I<filename>, name of ascii text file of x,y nodes 
    
options:
    -Wn, width of bins (degrees) 
    -E, equal area plot (rather than linear)
    -C, colour for rose petals 

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import sys 
import numpy as np 

#   defaults 
CM2INCHES = 0.3937 
DEG2RAD = np.pi / 180.0 
bGrid = False 
bEqualArea = False 
nBinWidth = 10  
sColour = 'C0' 
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
    if "-C" in sArg: 
        sColour = sArg[2:] 
    #   number of bins 
    if "-W" in sArg:
        nBinWidth = int(sArg[2:])
        
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqSegmentAngleRose.py -I<inputfilename>')

#   get nodes and calculate angles from nodes 
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
segangle = fpq.getSegAngles(xnodelist, ynodelist)
nSegs = len(segangle)

#   bin the data and find maximum per bin 
nBins = int(round(360/nBinWidth))
segangleDoubled = np.zeros(len(segangle))
segangleDoubled = np.copy(segangle)
segangleDoubled = np.concatenate([segangleDoubled, segangleDoubled+180.0])
n, b = plt.histogram(segangleDoubled, nBins)
nMax = max(n) 

#   plot the segment angle distribution 
plt.figure(figsize=(xSize, ySize))
plt.subplot(111, projection='polar')
coll = fpq.rose(segangle, bins=nBins, 
                bidirectional=True, eqarea=False, 
                color=sColour)
plt.xticks(np.radians(range(0, 360, 45)), 
           ['0', '45', '90', '135', '180', '215', '270', '315'])
plt.rgrids(range(0, int(round(nMax*1.1)), int(round((nMax*1.1)/5))), angle=330)
plt.ylim(0, int(round(nMax*1.1)))
plt.title('Segment strikes, n=%i' % nSegs)
plt.savefig("fpqSegmentAngleRose1.png", dpi=600)

segangle2 = np.asanyarray(segangle)
plt.figure(figsize=(xSize, ySize))
plt.subplot(111, projection='polar')
ax = plt.gca()
fpq.rose_plot(ax, -segangleDoubled*DEG2RAD, offset=90*DEG2RAD, bins=nBins, start_zero=False)
ax.invert_xaxis()
#plt.ylim(0, int(round(np.sqrt(nMax)*1.1)))
plt.title('Segment strikes, n=%i' % nSegs)
plt.savefig("fpqSegmentAngleRose2.png", dpi=600)

print('Plotted %5d segments & angles' % nSegs)