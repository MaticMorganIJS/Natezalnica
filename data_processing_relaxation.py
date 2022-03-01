# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:04:07 2022

@author: Matic
"""

import os
import matplotlib.pyplot as plt


# function that extracts consecutive forces which are measured every 0.1 seconds
def extract_forces(file):
    forces = []
    for line in vsebina:
        forces.append(float(line.split('\t')[0]))
    
    return forces


# function that draw the specified graph
def draw_forces():
    fig, ax = plt.subplots()
    ax.set_title('Upper force')
    plt.xlabel('Time [ 0.1 s ]')
    plt.ylabel('Force [ mg ]')
    plt.scatter(range(len(all_forces)), all_forces, s=1)



if __name__ == "__main__":
    
    all_forces = []
    
    # adding up measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\aging\meritve_aging\measurements_to_be_processed'):
        file = open(entry.path)
        vsebina = file.readlines()
        all_forces += extract_forces(file)
        file.close()

    draw_forces()
