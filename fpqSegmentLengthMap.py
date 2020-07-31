#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:28:47 2020

fpqSegmentLengthMap

plots a map of segments, colour coded by length, from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    grid, on/off 

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import matplotlib.collections as mc 
import matplotlib.colors as colors
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
    sys.exit('Usage: python3 fpqSegmentLengthMap.py -I<inputfilename>')

#   get the x,y nodes & calculate angles from the file data
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
seglengths = fpq.getSegLengths(xnodelist, ynodelist)

#   get the cmocean 'haline' colour map, sized to the maximum segment length  
start = 0.0 
stop = 1.0 
number_of_lines = int(max(seglengths))+1
cm_subsection = np.linspace(start, stop, number_of_lines) 
colours = [ cmo.cm.haline(x) for x in cm_subsection ]

#   segment coordinates and colours (based on length) into a line collection  
nTraces = int(len(xnodelist))
nSegs = int(len(seglengths)) 
segments = []
segcolours = np.zeros([nSegs, 4])
segcount = 0 
for t in range(0, nTraces): 
    nSegsThis = len(xnodelist[t])
    for s in range(1, nSegsThis):
        segments.append([(xnodelist[t][s-1], ynodelist[t][s-1]), 
                         (xnodelist[t][s], ynodelist[t][s])]) 
        segcolours[segcount] = colours[int(seglengths[segcount])] 
        segcount += 1 
sc = mc.LineCollection(segments, colors=segcolours, 
                       linewidths=1, cmap=cmo.cm.haline, norm=colors.PowerNorm(gamma=0.5))

#   get plot limits 
nodelist = xnodelist 
nodelist.extend(ynodelist)
xmin, xmax, ymin, ymax = fpq.getPlotLimits(nodelist) 
 
#   plot the map 
fig, ax = plt.subplots(figsize=(xSize,ySize))
p = ax.add_collection(sc)
plt.xlabel('X, pixels')
plt.ylabel('Y, pixels')
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax) 
plt.gca().set_aspect('equal')
plt.grid(bGrid)
plt.colorbar(sc, label='Segment length, pixels', 
                 orientation='horizontal', 
                 fraction=0.04)
p.set_clim(0, number_of_lines)
plt.title('Segment length map, n=%i' % nSegs)
plt.savefig("fpqSegmentLengthMap.png", dpi=600)

print('Plotted %5d segments & lengths' % nSegs)