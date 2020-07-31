#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:51:00 2020

fpqTraceMap

plots a map of traces from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    colour of traces 
    show nodes, yes/no
    grid, on/off 
    
@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import sys 

#   defaults 
sColour = 'b' 
bGrid = True 
bNode = False
 
#   process command line arguments; filename is mandatory 
bFilename = False 
for sArg in sys.argv[1:]:   
    #   input data file 
    if "-I" in sArg:
        fn = sArg[2:]
        bFilename = True 
    #   line colour for traces   
    if "-C" in sArg:
        sColour = sArg[2:]
    #   grid on 
    if "-G" in sArg: 
        bGrid = True 
    #   nodes on     
    if "-N" in sArg:
        bNode = True 
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqTraceMap.py -I<inputfilename>')

#   get the x,y nodes from the file 
nodes = fpq.getNodes(fn)
nodexlist = nodes[0] 
nodeylist = nodes[1] 

#   get some stats 
nTraces = int(len(nodexlist)) 
nNodes = int(sum(len(x) for x in nodexlist)) 
#   get plot limits 
nodelist = nodexlist.copy()
nodelist.extend(nodeylist.copy())
xmin, xmax, ymin, ymax = fpq.getPlotLimits(nodelist) 

#   plot the traces 
plt.figure(figsize=(6,6))
for node in range(0, len(nodexlist)):
    plt.plot(nodexlist[node], nodeylist[node], sColour) 
    if bNode:
        plt.plot(nodexlist[node], nodeylist[node], sColour+'o')         
plt.xlabel('X, pixels')
plt.ylabel('Y, pixels')
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax) 
plt.gca().set_aspect('equal')
plt.grid(bGrid)
plt.title('Trace map, n=%i' % nTraces)
plt.savefig("fpqTraceMap.png", dpi=300)

print('Plotted %5d traces' % nTraces)