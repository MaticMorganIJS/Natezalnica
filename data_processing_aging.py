# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 15:18:16 2022

@author: Matic
"""


import os
import numpy as np
import matplotlib.pyplot as plt

 # mass extracted in miligrams #
def ExtractMasses(mass_type):
    upper_masses = []
    lower_masses = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 1):
                upper_masses.append(float(line.split('\t')[0]))
            else:
                lower_masses.append(float(line.split('\t')[0]))
    
    if (mass_type == 'upper'):
        return upper_masses
    else:
        return lower_masses


def ExtractTimes(time_type):
    upper_times = []
    lower_times = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 1):
                upper_times.append(float(line.split('\t')[1]))
            else:
                lower_times.append(float(line.split('\t')[1]))
    
    if (time_type == 'upper'):
        return upper_times
    else:
        return lower_times
    
def ExtractLengths(length_type):
    upper_lengths = []
    lower_lengths = []
    for idx, line in enumerate(vsebina):
        if line[0] == '#':
            continue
        else:
            if (idx % 2 == 1):
                upper_lengths.append(float(line.split('\t')[2]))
            else:
                lower_lengths.append(float(line.split('\t')[2]))
    
    if (length_type == 'upper'):
        return upper_lengths
    else:
        return lower_lengths

def IsBroken():
    upper_masses = ExtractMasses('upper')
    lower_masses = ExtractMasses('lower')
    lower_masses_avg = sum(lower_masses) / len(lower_masses)
    broken = False
    for u in upper_masses:
        if (abs(u - lower_masses_avg) < 1000):
            broken = True
            
    return broken

def ExtractGoodMasses():
    if IsBroken():
        upper_masses = ExtractMasses('upper')
        lower_masses = ExtractMasses('lower')
        lower_masses_avg = sum(lower_masses) / len(lower_masses)
        while (abs(upper_masses[-1] - lower_masses_avg) < 1000):
            upper_masses.pop(-1)
        
        return upper_masses
            
            
# functions that calculate certain values #

 # stress field calculated in F / m^2
def CalculateStressFields(mass_type, area):
    masses = ExtractMasses(mass_type)
    stress_fields = []
    for m in masses:
        stress_fields.append((9.81 * m) / area)
        
    return stress_fields

 # strain value coresponding to the %, area in mm^2, returns value in GPa
def CalculateYoungModulus(strain, area):
    moduli = []
    stress_fields = CalculateStressFields('upper', area)
    for f in stress_fields:
        moduli.append((f / (strain * 0.01)) / 1000000)
    
    return moduli

 # functions that draw the specified graphs
def DrawMasses(mass_type):
    if (mass_type == 'upper'):
        fig, ax = plt.subplots()
        ax.set_title('Upper masses')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Upper masses [ mg ]')
        xs = range(len(all_upper_masses))
        ys = all_upper_masses
        plt.scatter(xs, ys, s=1)
    
    else:
        fig, ax = plt.subplots()
        ax.set_title('Lower masses')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Lower masses [ mg ]')
        xs = range(len(all_lower_masses))
        ys = all_lower_masses
        plt.scatter(xs, ys, s=1)
        

def DrawStressFields(force_type):
     if (force_type == 'upper'):
        fig, ax = plt.subplots()
        ax.set_title('Upper stress fields')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Stress field [ N / m^2 ]')
        xs = range(len(all_upper_stress_fields))
        ys = all_upper_stress_fields
        plt.scatter(xs, ys, s=1)
        
    
     else:
        fig, ax = plt.subplots()
        ax.set_title('Lower stress fields')
        plt.xlabel('Consecutive measurement [ / ]')
        plt.ylabel('Stress field [ N / m^2 ]')
        xs = range(len(all_lower_stress_fields))
        ys = all_lower_stress_fields
        plt.scatter(xs, ys, s=1)


def DrawYoungsModuli():
    fig, ax = plt.subplots()
    # ax.set_title('Young\'s modulus with respect to the number of repetitions')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Young\'s modulus [ GPa ]')
    xs = range(len(all_moduli))
    ys = all_moduli
    plt.scatter(xs, ys, s=1)
  
    
def draw_single_young_modulus():
    fig, ax = plt.subplots()
    ax.set_title('Young\'s modulus with respect to the number of repetitions')
    plt.xlabel('Consecutive measurement [ / ]')
    plt.ylabel('Young\'s modulus [ GPa ]')
    plt.scatter(range(len(moduli)), all_moduli, s=1)


if __name__ == "__main__":

    area = 1.4
    strain = 30
    
    all_upper_masses = []
    all_lower_masses = []
    all_upper_stress_fields = []
    all_lower_stress_fields = []
    all_moduli = []

     # adding up measurements from all files in the specified directory
    for entry in os.scandir(r'C:\Users\Matic\Documents\1_služba\aging\meritve_aging\measurements_to_be_processed\aging'):
        file = open(entry.path)
        vsebina = file.readlines()
        
        try:

            all_upper_masses += ExtractMasses('upper')
            all_lower_masses += ExtractMasses('lower')
            all_upper_stress_fields += CalculateStressFields('upper', area)
            all_lower_stress_fields += CalculateStressFields('lower', area)
            all_moduli += CalculateYoungModulus(strain, area)
            
            file.close()
            
        except:
            print(f"File {file} couldn't be processed.")
            file.close()
            
        finally:
            file.close()
            

     # drawing all the graphs
    DrawMasses('upper')
    DrawMasses('lower')
    DrawStressFields('upper')
    DrawStressFields('lower')
    DrawYoungsModuli()
