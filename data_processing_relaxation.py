# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:04:07 2022

@author: Matic
"""

import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


# exponential function
def exponentialFunction(x, m, t, b):
    return m * np.exp(-t * x) + b


# function that extracts consecutive forces which are measured every 0.1 seconds
def ExtractForces(file, force_type):
    forces = []
    for line in vsebina:
        forces.append(float(line.split('\t')[0]))
    
    if (force_type == 'all'):
        return forces
    
    elif (force_type == 'upper'):
        upper_forces = []
        for idx, val in enumerate(forces):
            if (idx < (len(forces) / 2) + 10):
                upper_forces.append(val)
        
        # cutting away the initial rising forces
        while (upper_forces[0] < upper_forces[1]):
            upper_forces.pop(0)
        # cutting away the latter falling forces
        while (upper_forces[-1] < upper_forces[-2]):
            upper_forces.pop(-1)
            
        return upper_forces
        
    elif (force_type == 'lower'):
        lower_forces = []
        for idx, val in enumerate(forces):
            if (idx > (len(forces) / 2)):
                lower_forces.append(val)
        # cutting away the initial falling forces
        while (lower_forces[0] > lower_forces[1]):
            lower_forces.pop(0)
        
        return lower_forces


# function that draw the specified graph
def DrawForces(force_type):
    
    if (force_type == 'all'):
        
        fig, ax = plt.subplots()
        ax.set_title('Force with respect to time')
        plt.xlabel('Time [ 0.1 s ]')
        plt.ylabel('Force [ mg ]')
        plt.scatter(range(len(ExtractForces(file, 'all'))), ExtractForces(file, 'all'), s=1)
    else:
        
        fig, ax = plt.subplots()
        ax.set_title('Forces during relaxation with respect to time')
        plt.xlabel('Time [ 0.1 s ]')
        plt.ylabel('Force [ mg ]')
        
        ys = ExtractForces(file, force_type)
        xs = range(len(ys))
        # perform the fit
        p0 = (2000, .1, 50) # start with values near those we expect
        params, cv = curve_fit(exponentialFunction, xs, ys, p0)
        m, t, b = params
                
        # plot the results
        plt.scatter(xs, ys, s=1, label="data")
        plt.plot(xs, exponentialFunction(xs, m, t, b), '--', label="fitted", color = 'r')
        plt.legend()
        
        # calculate and print out the parameters
        sampleRate = 20_000 # Hz
        tauSec = (1 / t) / sampleRate
        print(f"Y = {m} * e^(-{t} * x) + {b}")
        print(f"Tau = {tauSec * 1e6} µs")

       

if __name__ == "__main__":
    
    
    # processing measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\aging\meritve_aging\measurements_to_be_processed'):
        file = open(entry.path)
        vsebina = file.readlines()
        
        DrawForces('all')
        DrawForces('upper')
        DrawForces('lower')
      
        
        file.close()        
