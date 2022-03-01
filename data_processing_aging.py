# -*- coding: utf-8 -*-
"""
Created on Mon Feb  21 10:13:02 2022

@author: Matic
"""

import os
import matplotlib.pyplot as plt


# returns the additional relaxation time of consecutive repetitions in seconds as a list of floats
def extract_additional_relaxations(file):
    additional_relaxations = []
    i = 0
    while (i < len(vsebina)):
        line_temp = vsebina[i+2]
        line_temp = line_temp.replace('\n', '')
        additional_relaxations.append(float(line_temp))
        i += 4
    
    return additional_relaxations


# returns either the upper or the lower forces of consecutive repetitions in miligrams as a list of floats
# force_type is either 'upper' or 'lower'.
def extract_forces(file, force_type):
    upper_forces = []
    lower_forces = []
    i = 0
    while(i < len(vsebina)):
        upper_forces.append(float(vsebina[i+1].split()[0]))
        lower_forces.append(float(vsebina[i+3].split()[0]))
        i += 4
    
    if (force_type == 'upper'):
        return upper_forces
    else:
        return lower_forces


# returns either the upper times, lower times or oscillation times of consecutive repetitions in seconds as a list of floats
def extract_times(file, time_type):
    upper_times = []
    lower_times = []
    oscillation_times = []
    i = 0
    while(i < len(vsebina)):
        upper_times.append(float(vsebina[i+1].split()[1]))
        lower_times.append(float(vsebina[i+3].split()[1]))
        i += 4
    for j in range(len(upper_times)):
        oscillation_times.append(upper_times[j] - upper_times[j-1])
    oscillation_times.pop(0)
    
    if (time_type == 'upper'):
        return upper_times
    elif (time_type == 'lower'):
        return lower_times
    else:
        return oscillation_times


# returns either the upper or lower lengths of consecutive repetitions in milimeter as a list of floats
def extract_lengths(file, length_type):
    upper_lengths = []
    lower_lengths = []
    i = 0
    while(i < len(vsebina)):
        upper_lengths.append(float(vsebina[i+1].split()[2]))
        lower_lengths.append(float(vsebina[i+3].split()[2]))
        i += 4
        
    if (length_type == 'upper'): 
        return upper_lengths
    else:    
        return lower_lengths


# functions that calculate certain values

# strain value coresponding to the %, area in mm^2, returns value in GPa
def calculate_youngs_moduli(file, strain, area):
    moduli = []
    forces = extract_forces(file, 'upper')
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


def draw_additional_relaxation_time(): 
    fig, ax = plt.subplots()
    ax.set_title('Additional relaxation time')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Additional relaxation time [ s ]')
    plt.scatter(range(len(all_additional_relaxations)), all_additional_relaxations, s=1)
    
    
def draw_oscillation_time():
    fig, ax = plt.subplots()
    ax.set_title('Oscillation time')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Oscillation time [ s ]')
    plt.scatter(range(len(all_oscillation_times)), all_oscillation_times, s=1)


def draw_young_modulus():
    fig, ax = plt.subplots()
    ax.set_title('Young\'s modulus with respect to the number of repetitions')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Young\'s modulus [ GPa ]')
    plt.scatter(range(len(all_moduli)), all_moduli, s=1)

if __name__ == "__main__":
    
    all_additional_relaxations = []
    all_upper_forces = []
    all_lower_forces = []
    all_oscillation_times = []
    all_upper_lengths = []
    all_lower_lengths = []
    all_moduli = []
    
    # adding up measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\aging\meritve_aging\measurements_to_be_processed'):
        file = open(entry.path)
        vsebina = file.readlines()

        all_additional_relaxations += extract_additional_relaxations(file)
        all_upper_forces += extract_forces(file, 'upper')
        all_lower_forces += extract_forces(file, 'lower')
        all_oscillation_times += extract_times(file, 'oscillation')
        all_upper_lengths += extract_lengths(file, 'upper')
        all_lower_lengths += extract_lengths(file, 'lower')
        all_moduli += calculate_youngs_moduli(file, 30, 1.6)
        file.close()
        
    # drawing all the graphs
    draw_forces('upper')
    draw_forces('lower')
    draw_lengths('upper')
    draw_lengths('lower')
    draw_additional_relaxation_time()
    draw_oscillation_time()
    draw_young_modulus()





