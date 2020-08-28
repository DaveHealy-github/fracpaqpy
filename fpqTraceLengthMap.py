#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:56:22 2020

fpqTraceLengthMap

plots a map of traces, colour coded by length, from an input file of x,y nodes 

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
tracelengths = fpq.getTraceLengths(xnodelist, ynodelist)

#   get the cmocean 'haline' colour map, sized to the maximum segment length  
start = 0.0 
stop = 1.0 
number_of_lines = int(max(tracelengths))+1
cm_subsection = np.linspace(start, stop, number_of_lines) 
colours = [ cmo.cm.haline(x) for x in cm_subsection ]

#   trace coordinates and colours (based on length) into a line collection  
nTraces = int(len(xnodelist))
traces = []
tracecolours = []
tracecount = 0 
segcount = 0 
#   so we draw the segments, but colour code according to trace length; hence two loops 
for t in range(0, nTraces): 
    nSegsThis = len(xnodelist[t])
    for s in range(1, nSegsThis):
        traces.append([(xnodelist[t][s-1], ynodelist[t][s-1]), 
                       (xnodelist[t][s], ynodelist[t][s])]) 
        tracecolours.append(colours[int(tracelengths[tracecount])])
        segcount += 1 
    tracecount += 1 
sc = mc.LineCollection(traces, colors=tracecolours, 
                       linewidths=1, cmap=cmo.cm.haline, norm=colors.PowerNorm(gamma=0.5))

#   get plot limits 
xmin, xmax, ymin, ymax = fpq.getPlotLimits(xnodelist, ynodelist) 
 
#   plot the traces 
fig, ax = plt.subplots(figsize=(xSize,ySize))
p = ax.add_collection(sc)
ax.set_xlabel('X, pixels')
ax.set_ylabel('Y, pixels')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax) 
ax.grid(bGrid)
ax.set_aspect('equal', adjustable='box')
plt.colorbar(sc, label='Trace length, pixels', 
                  orientation='horizontal', 
                  fraction=0.04)
p.set_clim(0, number_of_lines)
plt.title('Trace length map, n=%i' % nTraces)
plt.savefig("fpqTraceLengthMap.png", dpi=600)

print('Plotted %5d traces & lengths' % nTraces)