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


class Change_color_inverting_matrix() :
  
  def matrix00(self,instance) :
    ''' No colors inverting, nothing change.
        The image should appear like it was.
        matrix = [1,0,0,0,
                  0,1,0,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nNo colors inverting, nothing change.\nThe image should appear like it was.")
    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")     
  
  def matrix01(self,instance) :
    ''' Suppress red and let the grenn and blue values unchanged. 
        The image should appear without his red tone.
        matrix = [0,0,0,0,
                  0,1,0,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress red and let the green and blue values unchanged.\nThe image should appear without his red tone.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")
      
  def matrix02(self,instance) :
    ''' Suppress green and let the red and blue values unchanged. 
        The image should appear without his green tone.
        matrix = [1,0,0,0,
                  0,0,0,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress green tone and let the red and blue values unchanged.\nThe image should appear without his green tone.")

    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")  
    
  def matrix03(self,instance) :
    ''' Suppress blue and let the red and green values unchanged. 
        The image should appear without his blue tone.
        matrix = [1,0,0,0,
                  0,1,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress blue tone and let the red and green values unchanged.\nThe image should appear without his blue tone.")

    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0") 
    
  def matrix04(self,instance) :
    ''' Suppress green and blue and let the red value unchanged.
        The image should appear red tones and black.
        matrix = [1,0,0,0,
                  0,0,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress the green and blue tone and let red value unchanged.\nThe image should appear red tones and black.")

    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")        
   
  def matrix05(self,instance) :
    ''' Suppress red and blue and let the green value unchanged.
        The image should appear in green tones and black.
        matrix = [0,0,0,0,
                  0,1,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress the red tone and the blue tone and let green value unchanged.\nThe image should appear in green tones and black.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")         
   
  def matrix06(self,instance) :
    ''' Suppress red and green and let the blue value unchanged.
        The image should appear in blue tones and black.
        matrix = [0,0,0,0,
                  0,0,0,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress the red tone and the green tone and let blue value unchanged.\nThe image should appear in blue tones and black.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")          
  
  def matrix07(self,instance) :
    ''' Suppress red and green and blue.
        The image should appear in black.
        matrix = [0,0,0,0,
                  0,0,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nsupress the red tone and the green tone and the blue tone.\nThe image should appear in black.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    
    
    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")
    
  def matrix08(self,instance) :
    ''' Set all tones (red,green,blue) on the red value from every pixel.
        The image should appear in grayscale based on the red pixel value.
        matrix = [1,0,0,0,
                  1,0,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nSet all tones (red,green,blue) on the red value from every pixel.\nThe image should appear in grayscale based on the red pixel value.")

    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")  
    
  def matrix09(self,instance) :
    ''' Set all tones (red,green,blue) on the green value from every pixel.
        The image should appear in grayscale based on the green pixel value.
        matrix = [0,1,0,0,
                  0,1,0,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nSet all tones (red,green,blue) on the green value from every pixel.\nThe image should appear in grayscale based on the green pixel value.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")  
    
  def matrix10(self,instance) :
    ''' Set all tones (red,green,blue) on the blue value from every pixel.
        The image should appear in grayscale based on the blue pixel value.
        matrix = [0,0,1,0,
                  0,0,1,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nSet all tones (red,green,blue) on the blue value from every pixel.\nThe image should appear in grayscale based on the blue pixel value.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")    
  
  def matrix11(self,instance) :
    ''' Invert red and blue values and let the green value unchanged.
        The image should appear red-blue tones inversed.
        matrix = [0,0,1,0,
                  0,1,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values and let the green value unchanged.\nThe image should appear red-blue tones inversed.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("1")
    instance.button_matrix_green_green_button.set_data("value","1")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")    
  
  def matrix12(self,instance) :
    ''' Invert red and blue values and remove the green tones.
        The image should appear red-blue tones inversed without green tones.
        matrix = [0,0,1,0,
                  0,0,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values and remove the green tones.\nThe image should appear red-blue tones inversed without green tones.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")    
    
  def matrix13(self,instance) :
    ''' Invert red and blue values and set green on blue value to form an yellow tone.
        The image should appear yellow toned with red-blue color inversion.
        matrix = [0,0,1,0,
                  0,0,1,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values and set green on blue value to form an yellow tone.\nThe image should appear yellow toned with red-blue color inversion.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix14(self,instance) :
    ''' Invert red and blue values and set green on red value to form an turkish tone.
        The image should appear turkish toned with red-blue color inversion.
        matrix = [0,0,1,0,
                  1,0,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values and set green on red value to form an turkish tone.\nThe image should appear turkish toned with red-blue color inversion.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix15(self,instance) :
    ''' Invert red and blue values (red take the blue values) and remove green and blue tones.
        The image should appear red toned and black.
        matrix = [0,0,1,0,
                  0,0,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values (red take the blue values) and remove green and blue tones.\nThe image should appear red toned and black.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix16(self,instance) :
    ''' Invert red and blue values (blue take the red values) and remove green and red tones.
        The image should appear blue toned and black.
        matrix = [0,0,0,0,
                  0,0,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and blue values (blue take the red values) and remove green and red tones.\nThe image should appear blue toned and black.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix17(self,instance) :
    ''' Invert red and green values and remove the blue tone.
        The image should appear red-green toned inversed without blue tones.
        matrix = [0,1,0,0,
                  1,0,0,0,
                  0,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and green values and remove the blue tone.\nThe image should appear red-green toned inversed without blue tones.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix18(self,instance) :
    ''' Invert red and green-blue values to form an turkish tone.
        The image should appear red-(green-blue) toned inversed with an turkish tone.
        matrix = [0,1,0,0,
                  1,0,0,0,
                  1,0,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and green-blue values to form an turkish tone.\nThe image should appear red-(green-blue) toned inversed with an turkish tone.")

    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("1")
    instance.button_matrix_blue_red_button.set_data("value","1")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")      
  
  def matrix19(self,instance) :
    ''' Invert red and green values and set blue on the green pixel value to form an pink tone.
        The image should appear red-green inversed with an pink tone.
        matrix = [0,1,0,0,
                  1,0,0,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and green values and set blue on the green pixel value to form an pink tone.\nThe image should appear red-green inversed with an pink tone.")
    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0") 
    
  def matrix20(self,instance) :
    ''' Invert red and green values and let the blue value unchanged.
        The image should appear red-green inversed without blue tone change.
        matrix = [0,1,0,0,
                  1,0,0,0,
                  0,0,1,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert red and green values and let the blue value unchanged.\nThe image should appear red-green inversed without blue tone change.")
    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("1")
    instance.button_matrix_green_red_button.set_data("value","1")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("0")
    instance.button_matrix_green_blue_button.set_data("value","0")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("0")
    instance.button_matrix_blue_green_button.set_data("value","0")
    
    instance.button_matrix_blue_blue_label.set_text("1")
    instance.button_matrix_blue_blue_button.set_data("value","1")        
  
  def matrix21(self,instance) :
    ''' Invert green and blue values and remove the red tone.
        The image should appear green-blue inversed without red tone.
        matrix = [0,0,0,0,
                  0,0,1,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert green and blue values and remove the red tone.\nThe image should appear green-blue inversed without red tone.")
    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")        
  
  def matrix22(self,instance) :
    ''' Invert green and blue values and let the red tone unchanged.
        The image should appear green-blue inversed without red tone changing.
        matrix = [1,0,0,0,
                  0,0,1,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert green and blue values and let the red tone unchanged.\nThe image should appear green-blue inversed without red tone changing.")
    instance.button_matrix_red_red_label.set_text("1")
    instance.button_matrix_red_red_button.set_data("value","1")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0") 
    
  def matrix23(self,instance) :
    ''' Invert green and blue values and set the red tone on green value to form an pink tone.
        The image should appear green-blue inversed with an pink tone.
        matrix = [0,1,0,0,
                  0,0,1,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert green and blue values and set the red tone on green value to form an pink tone.\nThe image should appear green-blue inversed with an pink tone.")
    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("1")
    instance.button_matrix_red_green_button.set_data("value","1")
    
    instance.button_matrix_red_blue_label.set_text("0")
    instance.button_matrix_red_blue_button.set_data("value","0")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0") 
    
  def matrix24(self,instance) :
    ''' Invert green and blue values and set the red tone on blue value to form an yellow tone.
        The image should appear green-blue inversed with an yellow tone.
        matrix = [0,0,1,0,
                  0,0,1,0,
                  0,1,0,0,
                  0,0,0,1]
    '''
    
    instance.frame_matrix_filters.set_tooltip_text("Predefine matrix:\nInvert green and blue values and set the red tone on blue value to form an yellow tone.\nThe image should appear green-blue inversed with an yellow tone.")
    instance.button_matrix_red_red_label.set_text("0")
    instance.button_matrix_red_red_button.set_data("value","0")
    
    instance.button_matrix_red_green_label.set_text("0")
    instance.button_matrix_red_green_button.set_data("value","0")
    
    instance.button_matrix_red_blue_label.set_text("1")
    instance.button_matrix_red_blue_button.set_data("value","1")
    
    
    instance.button_matrix_green_red_label.set_text("0")
    instance.button_matrix_green_red_button.set_data("value","0")
    
    instance.button_matrix_green_green_label.set_text("0")
    instance.button_matrix_green_green_button.set_data("value","0")
    
    instance.button_matrix_green_blue_label.set_text("1")
    instance.button_matrix_green_blue_button.set_data("value","1")
    

    instance.button_matrix_blue_red_label.set_text("0")
    instance.button_matrix_blue_red_button.set_data("value","0")
    
    instance.button_matrix_blue_green_label.set_text("1")
    instance.button_matrix_blue_green_button.set_data("value","1")
    
    instance.button_matrix_blue_blue_label.set_text("0")
    instance.button_matrix_blue_blue_button.set_data("value","0")   
    
  
  
change_matrix=Change_color_inverting_matrix()        