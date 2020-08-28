#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:45:19 2020

fpqSlipTendencyMap.py 

plots a map of segments, colour coded by slip tendency, from an input file of x,y nodes
and parameters for sigma1, sigma2, and theta (angle of sigma1 from Y-axis)

input:
    name of ascii text file of x,y nodes 
    
options:
    grid, on/off 
    sigma1, stress
    sigma2, stress
    theta, angle of sigma1 w.r.t. y-axis in degrees

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
DEG2RAD = np.pi / 180.0 
bGrid = False 
fSigma1 = 100.0 
fSigma2 = 50.0 
fTheta = 0.0 
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
    #   sigma1 stress 
    if "-S1" in sArg:
        fSigma1 = float(sArg[3:])
    #   sigma2 stress 
    if "-S2" in sArg:
        fSigma2 = float(sArg[3:])
    #   theta, in degrees  
    if "-T" in sArg:
        fTheta = float(sArg[2:])

#   filename is mandatory         
if not bFilename:
    sys.exit('Usage: python3 fpqSlipTendency.py -I<inputfilename>')

#   get the x,y nodes & calculate angles from the file data
nodelist = fpq.getNodes(fn)
xnodelist = nodelist[0] 
ynodelist = nodelist[1]
segangle = fpq.getSegAngles(xnodelist, ynodelist)

#   get the cmocean 'thermal' colour map, scaled from 0-100% 
start = 0.0 
stop = 1.0 
number_of_lines = 101 
cm_subsection = np.linspace(start, stop, number_of_lines) 
colours = [ cmo.cm.thermal(x) for x in cm_subsection ]

#   slip tendency 
#   calculate max. possible slip tendency for these stresses 
nAlpha = np.arange(1, 180, 1)
Tsmax = max(((fSigma1 - fSigma2) * np.sin(nAlpha * DEG2RAD) * np.cos(nAlpha * DEG2RAD))  
           / (fSigma1 * np.cos(nAlpha * DEG2RAD)**2.0 + fSigma2 * np.sin(nAlpha * DEG2RAD)**2.0))  

#   get segment coordinates & colours (based on normalised slip tendency) into a line collection  
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
        
        poleAngle = segangle[segcount] + 90 - fTheta  

        sn = fSigma1 * np.cos(poleAngle * DEG2RAD)**2 + fSigma2 * np.sin(poleAngle * DEG2RAD)**2 
        tau = (fSigma1 - fSigma2) * np.sin(poleAngle * DEG2RAD) * np.cos(poleAngle * DEG2RAD) 
        
        Ts = abs(tau / sn)
        TsNorm = Ts / Tsmax 
        iTs = int(round(TsNorm * 100))
        
        segcolours[segcount] = colours[iTs] 
        segcount += 1
        
sc = mc.LineCollection(segments, colors=segcolours, linewidths=1, cmap=cmo.cm.thermal)

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
plt.colorbar(sc, label='Normalised slip tendency', 
                 orientation='horizontal', 
                 fraction=0.04)
p.set_clim(0, 1)
plt.title('Slip tendency map, n=%i' % nSegs)
plt.savefig("fpqSlipTendencyMap.png", dpi=600)

print('Plotted %5d segments' % nSegs)