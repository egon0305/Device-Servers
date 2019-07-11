# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang
"""
import visa
import numpy as np
rm=visa.ResourceManager()

class SR830():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def write(self, value):
        print(self.inst.query(value))
        
    def get_X(self):
        self.x=self.inst.query("OUTP?1")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_Y(self):
        self.x=self.inst.query("OUTP?2")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_R(self):
        self.x=self.inst.query("OUTP?3")
        self.x = self.x.strip("\n")
        return self.x
    
    def get_Theta(self):
        self.x=self.inst.query("OUTP?4")
        self.x = self.x.strip("\n")
        return self.x
    
    def set_AC_Volt(self,value):
        self.inst.write("SLVL"+str(value))
        
    def scan_bias(self,low,high,num):
        self.x=np.linspace(float(low),float(high),int(num)+1)
        for i in range(int(num)+1):
            self.set_AC_Volt(self.x[i])
            self.get_X()
            self.get_Y()
    
    def set_range(self, value):
        self.senslist = ([2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9, 1e-6, 2e-6, 
                          5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3,
                          10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1])
        self.x = 26
        for i in np.arange(26, -1, -1):
            if value < self.senslist[i]:
                self.x = i
            
        self.inst.write('SENS ' +str(self.x))
        
    def closeall(self):
        self.inst.close()
    
