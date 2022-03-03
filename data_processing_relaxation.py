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
        if line[0] == '#':
            continue
        else:
            forces.append(float(line.split('\t')[0]))
    
    if (force_type == 'all'):
        return forces
    
    elif (force_type == 'upper'):
        upper_forces = []
        for idx, val in enumerate(forces):
            if (idx < (len(forces) / 2)):
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
        xs = np.linspace( 0, len(ExtractForces(file, 'all')) / 10, num=len(ExtractForces(file, 'all')) )
        plt.scatter(xs, ExtractForces(file, 'all'), s=1)
    
    else:
        fig, ax = plt.subplots()
        ax.set_title('Forces during relaxation with respect to time')
        plt.xlabel('Time [ s ]')
        plt.ylabel('Force [ mg ]')
        
        ys = ExtractForces(file, force_type)
        xs = np.linspace( 0, len(ExtractForces(file, force_type)) / 10, num=len(ExtractForces(file, force_type)) )
        p0 = (2000, .1, 50)
        params, cv = curve_fit(exponentialFunction, xs, ys, p0)
        m, t, b = params
                
         # plot the results
        plt.scatter(xs, ys, s=1, label="data")
        plt.plot(xs, exponentialFunction(xs, m, t, b), '--', label="fitted", color = 'r')
        plt.legend()
        
         # calculate and print out the parameters
        tau = 1 / t
        print(f" Tau_{force_type} = {tau} s")
        
        return tau
       


if __name__ == "__main__":
    
    all_upper_taus = []
    all_lower_taus = []
    
     # processing measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\aging\meritve_aging\measurements_to_be_processed'):
        file = open(entry.path)
        vsebina = file.readlines()
        
        try:
            DrawForces('all')
            all_upper_taus.append(DrawForces('upper'))
            all_lower_taus.append(DrawForces('lower'))
        except:
            print(f"File {file} couldn't be processed.")
            file.close()
        finally:        
            file.close()
            
        average_upper_tau = sum(all_upper_taus) / len(all_upper_taus)
        average_lower_tau = sum(all_lower_taus) / len(all_lower_taus)
        
    print(average_upper_tau)
    print(average_lower_tau)
