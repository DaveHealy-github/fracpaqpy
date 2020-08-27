#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:31:26 2020

fracpaq.py

import library for generic functions 

@author: davidhealy
"""

import numpy as np 
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

def getNodes(fn):
    '''
    Parameters:
        fn - filename of ASCII tab-delimited text file of nodes 
             in x,y format, one fracture trace per line 
    Returns:
        list of node x-coordinates, grouped by trace 
        list of node y-coordinates, grouped by trace  
    '''    
    NodeList = [] 
    print('Reading file %s' % fn)
    
    #   open a node file 
    with open(fn, 'r') as reader:
        
        #  define list of node coordinates
        nodexlist = [] 
        nodeylist = [] 
    
        #  Read and print the entire file line by line
        i = 0 
        for line in reader:
            
    #        print('\n', line, end='')
            
            #  define numpy array of nodes on this trace
            pointarray = np.array 
            #   one line is one trace, variable number of nodes 
            pointarray = [float(x) for x in line.split()]
            
            #   how many nodes?
            nNodesThisTrace = int(len(pointarray)/2)
            
            if nNodesThisTrace >= 2:
                
                #   lists of x and y coords for this trace 
                xcoord = [] 
                ycoord = [] 
                
                #   for each node (i.e. pair of x,y coordinates)
                for n in range(0, len(pointarray)-1, 2):
                    
                    #   get coords of this node 
                    xcoord.append(pointarray[n])
                    ycoord.append(pointarray[n+1])
                    
                nodexlist.append(xcoord)
                nodeylist.append(ycoord) 
    
            #   increment the line (trace) counter 
            i = i + 1 
    
    NodeList = nodexlist, nodeylist
    
    nNodes = int(sum(len(x) for x in nodexlist)) 
    print('Read %5d nodes' % nNodes)
    
    return NodeList 

def getSegAngles(xlist, ylist):
    '''
    Parameters:
        xlist - list of x coordinates, grouped by trace 
        ylist - list of y coordinates, grouped by trace 
    Returns:
        list of angles - one per segment 
    '''
    anglelist = [] 
    
    for n in range(0, len(xlist)):
        
        xcoord = xlist[n]
        ycoord = ylist[n]
        
        #   get segment angles 
        for s in range(1, len(xcoord)):

            #   NB: change in X/change in Y, because strike angle is measured from Y-axis
            segangle = np.arctan2((xcoord[s]-xcoord[s-1]), (ycoord[s]-ycoord[s-1])) * 180 / np.pi
            if segangle < 0:
                segangle = segangle + 180 
            if segangle >= 179.5:
                segangle = 0.0 
            anglelist.append(segangle) 
        
    return anglelist 

def getSegLengths(xlist, ylist):
    '''
    Parameters:
        xlist - list of x coordinates, grouped by trace 
        ylist - list of y coordinates, grouped by trace 
    Returns:
        list of lengths - one per segment 
    '''
    lengthlist = [] 
    
    for n in range(0, len(xlist)):
        
        xcoord = xlist[n]
        ycoord = ylist[n]
        
        #   get segment lengths 
        for s in range(1, len(xcoord)):
                
            lengthlist.append(np.sqrt((xcoord[s]-xcoord[s-1])**2 + (ycoord[s]-ycoord[s-1])**2))
                    
    return lengthlist

def getTraceLengths(xlist, ylist):
    '''
    Parameters:
        xlist - list of x coordinates, grouped by trace 
        ylist - list of y coordinates, grouped by trace 
    Returns:
        list of lengths - one per segment 
    '''
    lengthlist = [] 
    
    for n in range(0, len(xlist)):
        
        xcoord = xlist[n]
        ycoord = ylist[n]
        
        lengthlist.append(np.sqrt((xcoord[-1]-xcoord[0])**2 + (ycoord[-1]-ycoord[0])**2))
                    
    return lengthlist

def getPlotLimits(nodelist):
      
    N = len(nodelist) 
    xmin = ymin = +9e38 
    xmax = ymax = -9e38 
    
    for i in range(0, N):
        if nodelist[i][0] < xmin:
            xmin = nodelist[i][0] 
        if nodelist[i][1] < ymin:
            ymin = nodelist[i][1] 
        if nodelist[i][0] > xmax:
            xmax = nodelist[i][0] 
        if nodelist[i][1] > ymax:
            ymax = nodelist[i][1] 

    return xmin, xmax, ymin, ymax 

def rose(azimuths, z=None, ax=None, bins=30, bidirectional=False, 
         color_by=np.mean, color=None, eqarea=False, **kwargs):
    '''
    Create a "rose" diagram (a.k.a. circular histogram).  

    Parameters:
    -----------
        azimuths: sequence of numbers
            The observed azimuths in degrees.
        z: sequence of numbers (optional)
            A second, co-located variable to color the plotted rectangles by.
        ax: a matplotlib Axes (optional)
            The axes to plot on. Defaults to the current axes.
        bins: int or sequence of numbers (optional)
            The number of bins or a sequence of bin edges to use.
        bidirectional: boolean (optional)
            Whether or not to treat the observed azimuths as bi-directional
            measurements (i.e. if True, 0 and 180 are identical).
        color_by: function or string (optional)
            A function to reduce the binned z values with. Alternately, if the
            string "count" is passed in, the displayed bars will be colored by
            their y-value (the number of azimuths measurements in that bin).
        color: colour string - added by D Healy, Jul 2020 
        eqarea: boolean for equal area projection - added by D Healy, Jul 2020 
        Additional keyword arguments are passed on to PatchCollection.

    Returns:
    --------
        A matplotlib PatchCollection
        
    Author:
    -------
    Joe Kington 2013 
        taken from https://stackoverflow.com/questions/16264837/how-does-one-add-a-colorbar-to-a-polar-plot-rose-diagram
    '''
    azimuths = np.asanyarray(azimuths)
    if color_by == 'count':
        z = np.ones_like(azimuths)
        color_by = np.sum
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = 'b'    
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.radians(90))
    if bidirectional:
        other = azimuths + 180
        azimuths = np.concatenate([azimuths, other])
        if z is not None:
            z = np.concatenate([z, z])
    # Convert to 0-360, in case negative or >360 azimuths are passed in.
    azimuths[azimuths > 360] -= 360
    azimuths[azimuths < 0] += 360
    counts, edges = np.histogram(azimuths, range=[0, 360], bins=bins)
    if eqarea:
        print('Hello') 
    if z is not None:
        idx = np.digitize(azimuths, edges)
        z = np.array([color_by(z[idx == i]) for i in range(1, idx.max() + 1)])
        z = np.ma.masked_invalid(z)
    edges = np.radians(edges)
    coll = colored_bar(edges[:-1], counts, z=z, width=np.diff(edges), 
                       ax=ax, color=color, **kwargs)
    return coll

def colored_bar(left, height, z=None, width=0.8, bottom=0, ax=None, color='b', **kwargs):
    '''
    A bar plot colored by a scalar sequence.
    
    Author:
    -------
    Joe Kington 2013 
        taken from https://stackoverflow.com/questions/16264837/how-does-one-add-a-colorbar-to-a-polar-plot-rose-diagram
    '''
    if ax is None:
        ax = plt.gca()
    width = itertools.cycle(np.atleast_1d(width))
    bottom = itertools.cycle(np.atleast_1d(bottom))
    rects = []
    for x, y, h, w in zip(left, bottom, height, width):
        rects.append(Rectangle((x,y), w, h))
    coll = PatchCollection(rects, array=z, **kwargs)
    coll.set_color(color)
    ax.add_collection(coll)
    # ax.autoscale()
    return coll
