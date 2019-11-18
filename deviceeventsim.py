# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:39:24 2019

@author: Magaywer
"""

import os
import sys
import tkinter
import tkinter.filedialog as tkFileDialog

class DeviceEventSim:
    def __init__(self, n, type_data, dim):
        self.n = n;
        self.type_data = type_data
        self.dim = dim

        self.data = self.openFile()
        self.dict = self.createDict()
        
    def openFile(self):
        print("abrindo o arquivo")
        
        root = tkinter.Tk()
        file = tkFileDialog.askopenfile(mode='r')    
        root.destroy()
        
        if (file == None):
            sys.exit()
         
        pathname = os.path.dirname(file.name)
        os.chdir(pathname)
        
        read_data = file.read().split("\n")
        file.close()
    
        data_aux = ['']* (self.n)
        for i in range(self.n):
            data_aux[i] = read_data[i].split(";")
            
        return data_aux
    
    def createDict(self):
        dict_aux = {}
        for elem in self.data:
            sensor = []
            for i in range(1, self.dim):
                sensor.append(elem[i])
            dict_aux[elem[0]] = [self.type_data, sensor]

        return dict_aux