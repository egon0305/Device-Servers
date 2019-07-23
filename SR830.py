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
        self._auto_ON = False
    
    def write(self, value):
        print(self.inst.query(value))
        
    def get_X(self):
        self.x=self.inst.query("OUTP?1")
        self.x = self.x.strip("\n")
        if self._auto_ON :
            self.__auto_range(float(self.x))
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

    def set_auto_range(self,value):
        self._auto_ON = False
        if value == 'on':
            self.senslist = ([2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9, 1e-6, 2e-6, 
                          5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3,
                          10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1])
            self.x=np.abs(float(self.get_X()))
            for i in np.arange(26, -1, -1):
                if  self.x< 0.85*self.senslist[i]:
                    self.sens=i
            self.inst.write('SENS ' +str(self.sens))
            self._auto_ON = True
            
        elif value == 'off':
            self._auto_ON = False
            
    def __auto_range(self,value):
        i = self.sens
        value=np.abs(value)
        if value < 0.1*self.senslist[i]:
            i = i-1
        elif value > 0.85*self.senslist[i]:
            i=i+2
        if i < 12:
            i=12
        if i != self.sens:
            self.inst.write('SENS ' +str(i))
            self.sens=i
            print('SR830 changed range to '+ str(self.senslist[i]) +'value now'+ str(value) +'\n')
        #0.1 0.85 can be changed as combination of (0.3 i-1,0.9 i+1) (0.2 i-1,0.9 i+1) (0.1 i-1,0.85 i+2)
    
    def closeall(self):
        self.inst.close()
    
