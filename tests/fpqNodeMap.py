#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:29:18 2020

fpqNodeMap

plots a map of nodes from an input file of x,y nodes 

input:
    name of ascii text file of x,y nodes 
    
options:
    colour of nodes 
    grid, on/off 

@author: davidhealy
"""

import fracpaq as fpq 
import matplotlib.pylab as plt 
import sys 

#   defaults 
sColour = 'C0' 
bGrid = False 
 
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
#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqNodeMap.py -I<inputfilename>')

#   get the x,y nodes from the file 
nodes = fpq.getNodes(fn)
nodexlist = nodes[0] 
nodeylist = nodes[1] 

#   get some stats 
nNodes = int(sum(len(x) for x in nodexlist)) 
#   get plot limits 
xmin, xmax, ymin, ymax = fpq.getPlotLimits(nodexlist, nodeylist) 

#   plot the traces 
plt.figure(figsize=(6,6))
for node in range(0, len(nodexlist)):
    plt.plot(nodexlist[node], nodeylist[node], sColour+'o')         
plt.xlabel('X, pixels')
plt.ylabel('Y, pixels')
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax) 
plt.gca().set_aspect('equal')
plt.grid(bGrid)
plt.title('Node map, n=%i' % nNodes)
plt.savefig("fpqNodeMap.png", dpi=300)

print('Plotted %5i nodes' % nNodes)