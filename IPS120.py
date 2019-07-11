# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:41:08 2018

@author: Mak & Shan group
"""

import visa 
rm=visa.ResourceManager()
import numpy as np
class IPS120():
    
    def __init__(self,address):    
        self.inst = rm.open_resource(address)
        self.inst.write_termination='\r'
        self.inst.read_termination='\r'
        self.inst.write('C3')

#get magnet parameters
        
    def get_setp(self):
        return self.inst.query('R8')
    
    def get_magfield(self):
        while True:
            self.r1=self.inst.query('R7')
            self.r2=list(self.r1)
            self.l=len(self.r2)
            if self.l>3 and (self.r2)[0]=='R' and (self.r2)[1]=='+':
                break
        self.r1=self.r1.strip('R+')
        return float(self.r1)


#get magnet parameters
    def set_pfield(self,setp):
        self.inst.query('P1')
        self.inst.query('J0'+str(setp))
        self.inst.query('A1')

    def set_nfield(self,setp):
        self.inst.query('P2')
        self.inst.query('J0'+str(setp))
        self.inst.query('A1')
       
    def set_positive_field(self,setp,rate):
        if rate < 0.3:
            self.inst.write('J'+str(setp))
            self.inst.write('T'+str(rate))
            self.inst.write('A1')

    def set_negative_field(self,setp,rate):
        if rate < 0.3:
            self.inst.write('J'+str(setp))
            self.inst.write('T'+str(rate))
            self.inst.write('A1')
            
    def set_fieldup(self,setp,rate):
        self.inst.write('P1')
        if rate < 0.3:
            self.inst.write('J'+str(setp))
            self.inst.write('T'+str(rate))
            self.inst.write('A1')

    def set_fielddown(self,setp,rate):
        self.inst.write('P2')
        if rate < 0.3:
            self.inst.write('J'+str(setp))
            self.inst.write('T'+str(rate))
            self.inst.write('A1')
    
    def set_heateroff(self):
        self.inst.query('H0')
    
    def set_heateron(self):
        self.inst.query('H1')
        
    def swap(self):
        self.inst.write('P4')

        
