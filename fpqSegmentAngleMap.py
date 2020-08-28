#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:36:36 2020

fpqSegmentAngleMap

plots a map of segments, colour coded by strike, from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    grid, on/off 

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import matplotlib.collections as mc 
import sys 
import cmocean as cmo 
import numpy as np 

#   defaults 
CM2INCHES = 0.3937 
bGrid = False 
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
    sys.exit('Usage: python3 fpqSegmentAngleMap.py -I<inputfilename>')

#   get the x,y nodes & calculate angles from the file data
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
segangle = fpq.getSegAngles(xnodelist, ynodelist)

#   get the cmocean 'phase' colour map - this is cyclic, good for strikes/azimuths 
start = 0.0 
stop = 1.0 
number_of_lines = 180 
cm_subsection = np.linspace(start, stop, number_of_lines) 
colours = [ cmo.cm.phase(x) for x in cm_subsection ]

#   get segment coordinates & colours (based on strike) into a line collection  
nTraces = int(len(xnodelist))
nSegs = int(len(segangle)) 
segments = []
segcolours = np.zeros([nSegs, 4])
segcount = 0 
for t in range(0, nTraces): 
    nSegsThis = len(xnodelist[t])
    for s in range(1, nSegsThis):
        segments.append([(xnodelist[t][s-1], ynodelist[t][s-1]), 
                         (xnodelist[t][s], ynodelist[t][s])]) 
        segcolours[segcount] = colours[int(segangle[segcount])] 
        segcount += 1 
sc = mc.LineCollection(segments, colors=segcolours, linewidths=1, cmap=cmo.cm.phase)

#   get plot limits 
xmin, xmax, ymin, ymax = fpq.getPlotLimits(xnodelist, ynodelist) 
 
#   plot the map 
fig, ax = plt.subplots(figsize=(xSize,ySize))
p = ax.add_collection(sc)
plt.xlabel('X, pixels')
plt.ylabel('Y, pixels')
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax) 
plt.gca().set_aspect('equal')
plt.grid(bGrid)
p.set_clim(0, 180)
plt.colorbar(sc, label='Segment strike, degrees', 
                 orientation='horizontal', 
                 fraction=0.04)
plt.title('Segment angle map, n=%i' % nSegs)
plt.savefig("fpqSegmentAngleMap.png", dpi=600)

print('Plotted %5d segments & angles' % nSegs)