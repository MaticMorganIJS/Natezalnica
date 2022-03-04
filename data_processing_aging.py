# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 15:18:16 2022

@author: Matic
"""


import os
import matplotlib.pyplot as plt


def ExtractForces(file, force_type):
    upper_forces = []
    lower_forces = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 0):
                upper_forces.append(float(line.split('\t')[0]))
            else:
                lower_forces.append(float(line.split('\t')[0]))
    
    if (force_type == 'upper'):
        return upper_forces
    else:
        return lower_forces


def ExtractTimes(file, time_type):
    upper_times = []
    lower_times = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 0):
                upper_times.append(float(line.split('\t')[1]))
            else:
                lower_times.append(float(line.split('\t')[1]))
    
    if (time_type == 'upper'):
        return upper_times
    else:
        return lower_times
    
def ExtractLengths(file, length_type):
    upper_lengths = []
    lower_lengths = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 0):
                upper_lengths.append(float(line.split('\t')[2]))
            else:
                lower_lengths.append(float(line.split('\t')[2]))
    
    if (length_type == 'upper'):
        return upper_lengths
    else:
        return lower_lengths


def IsBroken(file):
    upper_forces = ExtractForces(file, 'upper')
    lower_forces = ExtractForces(file, 'lower')
    lower_forces_avg = sum(lower_forces) / len(lower_forces)
    broken = False
    for u in upper_forces:
        if (abs(u - lower_forces_avg) < 1000):
            broken = True
            
    return broken

def ExtractGoodForces(file):
    if IsBroken(file):
        upper_forces = ExtractForces(file, 'upper')
        lower_forces = ExtractForces(file, 'lower')
        lower_forces_avg = sum(lower_forces) / len(lower_forces)
        while (abs(upper_forces[-1] - lower_forces_avg) < 1000):
            upper_forces.pop(-1)
        
        return upper_forces
            
            
            
 # functions that calculate certain values

 # strain value coresponding to the %, area in mm^2, returns value in GPa
def CalculateYoungModulus(file, strain, area):
    moduli = []
    forces = ExtractForces(file, 'upper')
    for force in forces:
        moduli.append( (0.001 * force) / ( area * strain ) )
    
    return moduli

 # functions that draw the specified graphs
def draw_forces(force_type):
    if (force_type == 'upper'):
        fig, ax = plt.subplots()
        ax.set_title('Upper force')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Upper force [ mg ]')
        plt.scatter(range(len(all_upper_forces)), all_upper_forces, s=1)
    
    else:
        fig, ax = plt.subplots()
        ax.set_title('Lower force')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Lower force [ mg ]')
        plt.scatter(range(len(all_lower_lengths)), all_lower_forces, s=1)
 
    
def draw_lengths(length_type):
    if (length_type == 'upper'):
        fig, ax = plt.subplots()
        ax.set_title('Upper lengths')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Upper length [ mm ]')
        plt.scatter(range(len(all_upper_lengths)), all_upper_lengths, s=1)
    
    else:
        fig, ax = plt.subplots()
        ax.set_title('Lower lengths')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('lower length [ mm ]')
        plt.scatter(range(len(all_lower_lengths)), all_lower_lengths, s=1)


def draw_young_modulus():
    fig, ax = plt.subplots()
    ax.set_title('Young\'s modulus with respect to the number of repetitions')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Young\'s modulus [ GPa ]')
    plt.scatter(range(len(all_moduli)), all_moduli, s=1)

if __name__ == "__main__":
    
    all_upper_forces = []
    all_lower_forces = []
    all_upper_lengths = []
    all_lower_lengths = []
    all_moduli = []
    
     # adding up measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\aging\meritve_aging\measurements_to_be_processed\aging'):
        file = open(entry.path)
        vsebina = file.readlines()
            
        try:
            all_upper_forces += ExtractForces(file, 'upper')
            all_lower_forces += ExtractForces(file, 'lower')
            all_moduli += CalculateYoungModulus(file, 30, 1.6)
            file.close()
        except:
            print(f"File {file} couldn't be processed.")
            file.close()
        finally:
            file.close()
            
            
     # drawing all the graphs
    draw_forces('upper')
    draw_forces('lower')
    
    draw_young_modulus()
