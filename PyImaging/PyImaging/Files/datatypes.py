#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
#                                                                      #
# PyImaging an image treatment programme with severals effects.        #
# And image files mergin capabilities.                                 #
# Copyright (C) 2014 Eddie Bruggemann                                  #
#                                                                      #
# This file is part of PyImaging.                                      #
# PyImaging is free software: you can redistribute it and/or modify    # 
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  # 
#                                                                      #
# PyImaging is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with PyImaging. If not, see <http://www.gnu.org/licenses/>     #
#                                                                      #
######################################################################## 


class Color(object) :
  def __init__(self,ub_v=False,f_v=False) :
    if ub_v:
      self.r=ub_v[0] ;
      self.g=ub_v[1] ;
      self.b=ub_v[2] ;
      if len(ub_v) == 4 :
        self.a=ub_v[3]
      else :
        self.a=False
    
    elif f_v :
      self.r=f_v[0] ;
      self.g=f_v[1] ;
      self.b=f_v[2] ;
      if len(f_v) == 4 :
        self.a=f_v[3]
      else :
        self.a=False
      
  def set_in_float_values(self) :
    if type(self.r) == int :
      self.r=self.r/255.
    if type(self.g) == int :
      self.g=self.g/255.
    if type(self.b) == int :
      self.b=self.b/255.
    if type(self.a) == int :
      self.a=self.a/255.
    else : 
      self.a=False 
    
    if not self.a :
      return (self.r,self.g,self.b)
    else :
      return (self.r,self.g,self.b,self.a)
   
  def get_ubyte_v_rgba(self) :
    if type(self.r) == float :
      self.r=int(self.r*255)
    if type(self.g) == float :
      self.g=int(self.g*255)
    if type(self.b) == float :
      self.b=int(self.b*255)
    if type(self.a) == float :
      self.a=int(self.a*255)
    else : 
      self.a=False 
    
    if not self.a :
      return (self.r,self.g,self.b)
    else :
      return (self.r,self.g,self.b,self.a)
   
  def get_ubyte_v_rgb(self) :
    if type(self.r) == float :
      self.r=int(self.r*255)
    if type(self.g) == float :
      self.g=int(self.g*255)
    if type(self.b) == float :
      self.b=int(self.b*255)
    
    return (self.r,self.g,self.b)
    
    
class CMatrix(object) :
  def __init__(self,red,green,blue,alpha=1) :
    
    self.red=red 
    self.blue=blue
    self.green=green
    self.alpha=alpha
    
    self.matrix=range(0,16)
    self.matrix[0]=1   ; self.matrix[4]=0  ; self.matrix[8]=0    ; self.matrix[12]=0 ;
    self.matrix[1]=0   ; self.matrix[5]=1  ; self.matrix[9]=0    ; self.matrix[13]=0 ;
    self.matrix[2]=0   ; self.matrix[6]=0  ; self.matrix[10]=1   ; self.matrix[14]=0 ;
    self.matrix[3]=0   ; self.matrix[7]=0  ; self.matrix[11]=0   ; self.matrix[15]=1 ;
    
    self._move_matrix=range(0,16)  
    
  def scale(self,red_factor,green_factor,blue_factor) :
    self._move_matrix[0]=red_factor ; self._move_matrix[4]=0            ; self._move_matrix[8]=0            ; self._move_matrix[12]=0 ;
    self._move_matrix[1]=0          ; self._move_matrix[5]=green_factor ; self._move_matrix[9]=0            ; self._move_matrix[13]=0 ;
    self._move_matrix[2]=0          ; self._move_matrix[6]=0            ; self._move_matrix[10]=blue_factor ; self._move_matrix[14]=0 ;
    self._move_matrix[3]=0          ; self._move_matrix[7]=0            ; self._move_matrix[11]=0           ; self._move_matrix[15]=1 ;
    
    self._multiply()  
  
  def colors_matrix(self,red,green,blue,alpha) :
    if not isinstance(red,list) and not isinstance(red,tuple) :
      raise TypeError(list,tuple)
    if not isinstance(green,list) and not isinstance(green,tuple) :
      raise TypeError(list,tuple)
    if not isinstance(blue,list) and not isinstance(blue,tuple) :
      raise TypeError(list,tuple)
    
    red_red_factor=red[0] ; red_green_factor=red[1] ; red_blue_factor=red[2] ;
    
    green_red_factor=green[0] ; green_green_factor=green[1] ; green_blue_factor=green[2] ;
    
    blue_red_factor=blue[0] ; blue_green_factor=blue[1] ; blue_blue_factor=blue[2] ;
    
    red   = self.red*red_red_factor + self.green*red_green_factor + self.blue*red_blue_factor ;
    green = self.red*green_red_factor + self.green*green_green_factor + self.blue*green_blue_factor ;
    blue  = self.red*blue_red_factor + self.green*blue_blue_factor + self.blue*blue_blue_factor ;
    
    alpha = self.alpha*alpha
    
    return (red,green,blue,alpha)
    
  def set_alpha(self,alpha) :
    self._move_matrix[0]=1 ; self._move_matrix[4]=0 ; self._move_matrix[8]=0  ; self._move_matrix[12]=0 ;
    self._move_matrix[1]=0 ; self._move_matrix[5]=1 ; self._move_matrix[9]=0  ; self._move_matrix[13]=0 ;
    self._move_matrix[2]=0 ; self._move_matrix[6]=0 ; self._move_matrix[10]=1 ; self._move_matrix[14]=0 ;
    self._move_matrix[3]=0 ; self._move_matrix[7]=0 ; self._move_matrix[11]=0 ; self._move_matrix[15]=alpha ;
    
    self._multiply()  
    
  
  def _multiply(self) :
    x=0
    tmp_matrix=range(0,16)
    while x < 16 :
      value1= x % 4
      value2=(x/4)*4
      tmp_matrix[x]=self._move_matrix[value1] * self.matrix[value2+0] + self._move_matrix[value1+4] * self.matrix[value2+1]+ self._move_matrix[value1+8] * self.matrix[value2+2]+ self._move_matrix[value1+12] *  self.matrix[value2+3]
      x += 1
    
    for v in range(0,16) :
      self.matrix[v]=tmp_matrix[v]
  
  def get_result_rgb(self) :
   
    red   =  self.red * self.matrix[0] + self.green * self.matrix[1] + self.blue * self.matrix[2]  + self.alpha * self.matrix[3]   
    green =  self.red * self.matrix[4] + self.green * self.matrix[5] + self.blue * self.matrix[6]  + self.alpha * self.matrix[7]   
    blue  =  self.red * self.matrix[8] + self.green * self.matrix[9] + self.blue * self.matrix[10] + self.alpha * self.matrix[11]  
    
    return red,green,blue
  
  def get_result_rgba(self) :
    red   =  self.red * self.matrix[0] + self.green * self.matrix[1] + self.blue * self.matrix[2]  + self.alpha * self.matrix[3]   
    green =  self.red * self.matrix[4] + self.green * self.matrix[5] + self.blue * self.matrix[6]  + self.alpha * self.matrix[7]   
    blue  =  self.red * self.matrix[8] + self.green * self.matrix[9] + self.blue * self.matrix[10] + self.alpha * self.matrix[11] 
    
    alpha = self.alpha * self.matrix[15]
    
    return (red,green,blue,alpha)
  
  def mult_matrix(self,matrix) :
    self._move_matrix[0]=matrix[0] ; self._move_matrix[4]=matrix[4] ; self._move_matrix[8]=matrix[8]   ; self._move_matrix[12]=matrix[12] ;
    self._move_matrix[1]=matrix[1] ; self._move_matrix[5]=matrix[5] ; self._move_matrix[9]=matrix[9]   ; self._move_matrix[13]=matrix[13] ; 
    self._move_matrix[2]=matrix[2] ; self._move_matrix[6]=matrix[6] ; self._move_matrix[10]=matrix[10] ; self._move_matrix[14]=matrix[14] ;
    self._move_matrix[3]=matrix[3] ; self._move_matrix[7]=matrix[7] ; self._move_matrix[11]=matrix[11] ; self._move_matrix[15]=matrix[15] ;
    
    self._multiply() 
    