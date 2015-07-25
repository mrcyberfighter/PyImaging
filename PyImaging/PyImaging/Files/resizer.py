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

from __future__ import division
from PIL import Image


class Resizer() :
  
  def resizer(self,filepath,frame_width,frame_height) :
    '''filepath=path with ext'''
    filepath=Image.open(filepath)
    self.image_size=filepath.size
    width=frame_width
    height=frame_height
    factor=frame_width/frame_height
    if not (self.image_size[0]/self.image_size[1] == 1 or self.image_size[1]/self.image_size[0] == 1) and len(str(self.image_size[0]/self.image_size[1])) < 5 :
      while len(str(self.image_size[0]/self.image_size[1])) < 5 :
        self.image_size=(self.image_size[0]+1,self.image_size[1]+1)
  
    if self.image_size[0] >= width and self.image_size[1] > height :
      self.factor_width=self.image_size[0]/self.image_size[1]
      factor_height=self.image_size[1]/self.image_size[0]
      self.width=0.0
      self.height=0.0
      kontrolle=0
      
      
      if self.factor_width == 1 or factor_height == 1:
        if height > width :
          self.width=width+.0
          self.height=width+.0
        elif height < width :
          self.width=height+.0
          self.height=height+.0
        else :
          self.width=height+.0
          self.height=height+.0
      
  
      if self.image_size[0] > self.image_size[1] :
  
        if self.factor_width < factor : #rapport: width/height  
          while self.height < height :
            if (self.height + factor_height) >= height :
              self.width=self.width*factor_height
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height
        
        elif self.factor_width > factor :
          while self.width < width :
            if (self.width + self.factor_width) >= width :
              self.height=self.height*self.factor_width
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height  
  
      if self.image_size[0] < self.image_size[1] :
  
        if self.factor_width < factor :  #rapport: width/height  
          while self.height < height :
            if (self.height + factor_height) >= height :
              self.width=self.width*factor_height
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height
        
        elif self.factor_width > factor : #rapport: width/height  
          while self.width < width :
            if (self.width + self.factor_width) >= width :
              self.height=self.height*self.factor_width
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height  
      
      
      return str(round(self.width))[0:str(round(self.width)).index('.')], str(round(self.height))[0:str(round(self.height)).index('.')]

    elif self.image_size[0] > width and self.image_size[1] <= height :
      self.factor_width=self.image_size[0]/self.image_size[1]
      factor_height=self.image_size[1]/self.image_size[0]
      self.width=0.0
      self.height=0.0
      if self.image_size[0] == self.image_size[1] :
        if height > width :
          self.width=width+.0
          self.height=width+.0
        elif height < width :
          self.width=height+.0
          self.height=height+.0
        else :
          self.width=height+.0
          self.height=height+.0
  
      if self.factor_width < factor :  #rapport: width/height  
        while self.height < height :
          if (self.height + factor_height) >= height :
            self.width=self.width*factor_height
            break
          self.width=self.width+self.factor_width
          self.height=self.height+factor_height
    
      elif self.factor_width > factor : #rapport: width/height  
        while self.width < width :
          if (self.width + self.factor_width) >= width :
            self.height=self.height*self.factor_width
            break
          self.width=self.width+self.factor_width
          self.height=self.height+factor_height  
      
      
      
      return str(round(self.width))[0:str(round(self.width)).index('.')], str(round(self.height))[0:str(round(self.height)).index('.')]
      
    elif self.image_size[0] <= width and self.image_size[1] > height :
      self.factor_width=self.image_size[0]/self.image_size[1]
      factor_height=self.image_size[1]/self.image_size[0]
      self.width=0.0
      self.height=0.0
      
      
      if self.image_size[0] == self.image_size[1] :
        if height > width :
          self.width=width+.0
          self.height=width+.0
        elif height < width :
          self.width=height+.0
          self.height=height+.0
        else :
          self.width=height+.0
          self.height=height+.0
    
      
      if self.image_size[0] > self.image_size[1] :
  
        if self.factor_width < factor :  #rapport: width/height  
          while self.height < height :
            if (self.height + factor_height) >= height :
              self.width=self.width*factor_height
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height
          
        elif self.factor_width > factor :
          while self.width < width :
            if (self.width + self.factor_width) >= width :
              self.height=self.height*self.factor_width
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height  
  
      if self.image_size[0] < self.image_size[1] :
  
        if self.factor_width < factor :              #rapport: width/height   
          while self.height < height :
            if (self.height + factor_height) >= height :
              self.width=self.width*factor_height
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height
            
        elif self.factor_width > factor : #rapport: width/height  
          while self.width < width :
            if (self.width + self.factor_width) >= width :
              self.height=self.height*self.factor_width
              break
            self.width=self.width+self.factor_width
            self.height=self.height+factor_height  
      
      
      return str(round(self.width))[0:str(round(self.width)).index('.')], str(round(self.height))[0:str(round(self.height)).index('.')]
      
    elif self.image_size[0] <= width and self.image_size[1] <= height :
      self.factor_width=self.image_size[0]/self.image_size[1]
      self.width=self.image_size[0]
      self.height=self.image_size[1]
      return str(self.image_size[0]), str(self.image_size[1])

  def assertionen(self,a) :
    result='Assertion successfull'
    try :
      assert(round(self.width/self.height,a) == round(self.factor_width,a))
    except :  
      result='Assertion failed.\nBe aware of false positive !!!'
    return result  
  