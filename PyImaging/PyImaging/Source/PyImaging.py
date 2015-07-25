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


######################
# GUI modules.
import pygtk
pygtk.require('2.0')
import gtk
######################

###############################
# System modules. 
from sys import path,argv

from os.path import expanduser, basename, isfile, isdir
from os import listdir, remove, mkdir, chmod

import atexit

import cPickle
###############################

#################################
# Main images treatment modules. 
from PIL import Image, ImageChops, ImageEnhance
#################################

# PIL image filter constantes. ########################################################################################
from ImageFilter import BLUR,CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,EMBOSS,FIND_EDGES,SHARPEN,SMOOTH,SMOOTH_MORE
#######################################################################################################################

####################################################################################################
path.append("/usr/share/PyImaging/Files") # Add filepath to personal module from the programm.

# Add personnal modules
from resizer import Resizer       # Image resizing into a frame module.

from filesloadselector import *   # File open file selector dialog module.  
from filesavingselector import *  # File save file selector dialog module.

from datatypes import  *          # Datatypes for Colors management class and Color matrix class.

from infosstatsdialog import *    # Image file informations stats dialog module.

# Images files mergin dialog windows modules.
from blenddialog import *      
from compositedialog import *  
from screendialog import *     

from differencedialog import * 
from lighterdialog import *    
from darkerdialog import *     
from adddialog import *        
from substractdialog import *  
from multiplydialog import *   

from adjustmentseditordialog import *

# Files mergin failure message toplevel
from file_mergin_error_dialog import error_file_mergin_message

# Color matrix dialog window module.
from colormatrixdialog import  *

# Color matrix settings module.
from change_matrix import *

# red,green,blue scaling dialog window module.
from redscaleeditordialog import  *
from greenscaleeditordialog import *
from bluescaleeditordialog import *
####################################################################################################

class Process_effects() :
  ''' Class having methods for effects processing. ''' 
  def __init__(self) :
    
    # List of images instances.
    self.operation_list_displaying_image=[]
    self.operation_list_image_instance_processing=[]
    
    # Mirroring position.
    self.image_mirror_orientation="S"
    
    # Resizing by rotating.
    self.rotate_resized=False
    
    # Filters in realtionship to user selection.
    self.filter_dict={ 0 : BLUR, 1 : CONTOUR, 2 : DETAIL, 3 : EDGE_ENHANCE, 4 : EDGE_ENHANCE_MORE, 5 : EMBOSS, 6 : FIND_EDGES, 7 : SHARPEN, 8 : SMOOTH, 9 : SMOOTH_MORE}
    
    # Getting user selection:
    self.grayscale_dict={ 0:"grayscale average",1:"grayscale minimum",2:"grayscale maximum",3:"grayscale red",4:"grayscale green",5:"grayscale blue"}
    
    self.do_undo=False
    self.do_redo=False
    
  def undo(self,widget,event=False) :
    ''' Undo operation processing operation method. '''
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if (image_settings_file.images_counter-2 >= 0 and not self.do_undo) or (image_settings_file.images_counter-1 >= 0 and self.do_undo) :
      # Undo is possible because the images instances counter variable is greater than:
      # -) 2 and no Undo operation has been performed from the user.
      # -) 1 and an Undo operation has even been performed from the user.
      
      if not self.do_undo : 
	# No undo has been performed from the user: the current image is up-to-date.
        self.save_image_counter=image_settings_file.images_counter-1 # Saving the images intances counter variable.
        image_settings_file.images_counter -= 2                      # Decrement the images instances counter variable.
        
      else :
	# An Undo operation has even been performed from the user.
        image_settings_file.images_counter -= 1                      # Decrement the images instances counter variable.
      
      self.do_undo=True                                              # Set the Undo control variable on True to mark the Undo operation. 
      
      
      # Set the current image to display to the image to display before the current Undo operation.
      image_settings_file.image_to_display,image_settings_file.image_to_display_filepath = self.operation_list_displaying_image[image_settings_file.images_counter]
      
      # Update the size of the image to display, in case it has been changed throught an rotation operation.
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=image_settings_file.image_to_display.size
      
      # Set the current image instance, to process effects on, to the image to instance before the current Undo operation.
      image_settings_file.image_processing=self.operation_list_image_instance_processing[image_settings_file.images_counter]
      
      # Update GUI with display image instance.
      image_settings_file.configure_image_display()
      image_settings_file.display_image()
      
  def redo(self,widget,event=False) :
    ''' Redo operation processing operation method. '''
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo and image_settings_file.images_counter+1 <= self.save_image_counter:
      # The redo operation is valid.
      self.do_redo=True                        # Set the Redo control variable on True to mark the Redo operation. 
      
      image_settings_file.images_counter += 1  # Increment the images instances counter variable.
      
      # Set the current image to display to the image to display after the current Redo operation.
      image_settings_file.image_to_display,image_settings_file.image_to_display_filepath = self.operation_list_displaying_image[image_settings_file.images_counter]
      
      # Update the size of the image to display, in case it has been changed throught an rotation operation.
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=image_settings_file.image_to_display.size
      
      # Set the current image instance, to process effects on, to the image to instance after the current Redo operation.
      image_settings_file.image_processing=self.operation_list_image_instance_processing[image_settings_file.images_counter]
      

      # Update GUI with display image instance.
      image_settings_file.configure_image_display()
      image_settings_file.display_image()
  
  def update_after_undo(self) :
    ''' Clean up function in case of user perform an effect operation and has done Undo-Redo operations before. '''
    
    i=self.save_image_counter # Iterator variable to set to the number of Undo operations.
    while i > image_settings_file.images_counter :
      # Actualized the images instances containers.
      
      #to_remove=self.operation_list_displaying_image.pop(i)[1]
      self.operation_list_displaying_image.pop(i)          # Pop all images instances after the current images instances counter value.
      self.operation_list_image_instance_processing.pop(i) # Pop all images instances after the current images instances counter value.
      #remove(to_remove)
  
      i -= 1
    
    self.do_undo=False  # Set the Undo control variable on False to mark that the user process an effect after Undo-Redo operations. 
    self.do_redo=False  # Set the Redo control variable on False to mark that the user process an effect after Undo-Redo operations.
    
    image_settings_file.images_counter += 1  # Increment the images instances counter.
        
        
  
  def rotate_image(self,widget,event=False,rotation=False) :
    ''' Image rotations method '''
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    if widget.name == "rotate left" or rotation == "left" :
      # We process the rotation on the image to display in the GUI, instance.
      # And on the effect processsing image instance.
      image_settings_file.image_to_display=image_settings_file.image_to_display.rotate(90)
      image_settings_file.image_processing=image_settings_file.image_processing.rotate(90)
      
    elif widget.name == "rotate right" or rotation == "right" :
      # We process the rotation on the image to display in the GUI, instance.
      # And on the effect processsing image instance.
      image_settings_file.image_to_display=image_settings_file.image_to_display.rotate(270)
      image_settings_file.image_processing=image_settings_file.image_processing.rotate(270)
     
    
      
    # Update processing image instance size. 
    image_settings_file.image_processing_width,image_settings_file.image_processing_height=image_settings_file.image_processing_height,image_settings_file.image_processing_width 
    
    # Rotated image width/height factors settings.
    image_settings_file.image_size_width_factor=float(image_settings_file.image_processing_height)/float(image_settings_file.image_processing_width)
    image_settings_file.image_size_height_factor=float(image_settings_file.image_processing_width)/float(image_settings_file.image_processing_height)
      
    
    if image_settings_file.rotate_90_need_thumbnail_H and not self.rotate_resized:
      # Case the image is larger than heigher and need to be resized for rotated displaying.
      
      # We save the width and height iof the GUI image instance.
      self.rotate_saved_width,self.rotate_saved_height=image_settings_file.image_to_display_width,image_settings_file.image_to_display_height
      
      # We invert width and height, in sea of resizing, so that the GUI display image enter in the GUI frame by resizing and so that the GUI display image is correct oriented.
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=image_settings_file.image_to_display_height,image_settings_file.image_to_display_width
      
      # Resize an tmp file, in sea of the final GUI display image instance resizing, with inverted width an height values. 
      tmp_rotate_image=image_settings_file.image_to_display.resize((image_settings_file.image_to_display_width,image_settings_file.image_to_display_height))
      tmp_rotate_image.save("/tmp/PyImaging/pyimage_tmp_rotate.{0}".format(image_settings_file.image_instance.format.lower()))
      
      # Perform resizing operation on GUI display image, of basis of the tmp file created above. 
      resizing=Resizer()
      image_new_size=resizing.resizer("/tmp/PyImaging/pyimage_tmp_rotate.{0}".format(image_settings_file.image_instance.format.lower()),image_settings_file.container_width-10,image_settings_file.container_height-10)
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=int(image_new_size[0]),int(image_new_size[1])
      image_settings_file.image_to_display=image_settings_file.image_to_display.resize((image_settings_file.image_to_display_width,image_settings_file.image_to_display_height))
      
      
      # Saving GUI display image and store the settings.
      tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
      image_settings_file.image_to_display_filepath=tmp_path
      image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
      self.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
      
      # resizing operation has been executed.
      self.rotate_resized=True
      
      
    elif not image_settings_file.rotate_90_need_thumbnail_V and self.rotate_resized :
      # Case the image is larger than heigher and need to be resized for rotated displaying.
      # And the image have been resized: we restore the inital values becuase we rotate into an horizontal orientation.
      
      # Restore the width and height settings from saved values.
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=self.rotate_saved_width,self.rotate_saved_height
      
      # Resize operation to restore the inital width and height values. 
      image_settings_file.image_to_display=image_settings_file.image_to_display.resize((image_settings_file.image_to_display_width,image_settings_file.image_to_display_height))
      
      # Saving GUI display image and store the settings.
      tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
      image_settings_file.image_to_display_filepath=tmp_path
      image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
      self.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
      
      # resizing operation has restore initial values.
      self.rotate_resized=False

    else :
      # Case the image is heigher than larger we dont need to reduce the image by rotating.
      
      #  We invert width and height, so that the GUI display image is correct oriented.
      image_settings_file.image_to_display_width,image_settings_file.image_to_display_height=image_settings_file.image_to_display_height,image_settings_file.image_to_display_width
      
      # Saving GUI display image and store the settings.
      tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
      image_settings_file.image_to_display_filepath=tmp_path
      image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
      self.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
      
    
    # Store effect processsing image instance in processing list.
    self.operation_list_image_instance_processing.append(image_settings_file.image_processing)
    
    # Update instance counter.
    image_settings_file.images_counter += 1
    
    # Update GUI with display image instance.
    image_settings_file.configure_image_display()
    image_settings_file.display_image()
        

  def flip_image(self,widget,event=False,flipping=False) :
    ''' Image mirroring method 
        We notice the mirror position by coordinates
        S: Sud  (Down)
        N: Nord (Up)
        E: East (Left)
        W: West (Right)
    '''
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    if widget.get_name() in ("flip up","flip down") or (flipping in ("flip up","flip down")) : # We indentify the type of mirroring.
      
      if self.image_mirror_orientation.startswith('S') : # Case the image is not horizontal flipped actually.
        
        if widget.get_name() == "flip up" or flipping == "flip up" :
          
          if self.image_mirror_orientation.endswith('E') :
            
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180) # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              image_settings_file.image_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180) # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation="NE" # Update current mirroring position.
          
          elif self.image_mirror_orientation.endswith('W') :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_TOP_BOTTOM) # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              image_settings_file.image_processing=image_settings_file.image_processing.transpose(Image.FLIP_TOP_BOTTOM) # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation="NW" # Update current mirroring position.
          
          else :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_TOP_BOTTOM) # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              image_settings_file.image_processing=image_settings_file.image_processing.transpose(Image.FLIP_TOP_BOTTOM) # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation="N" # Update current mirroring position.
      
      
        elif widget.get_name() == "flip down"  or flipping == "flip down" :
          # We cannot flip to the down if we are at down.
          return
        
      elif self.image_mirror_orientation.startswith('N') : # Case the image is horizontal flipped actually.
        
        if widget.get_name() == "flip down" or flipping == "flip down" :
          
          if self.image_mirror_orientation.endswith('E') :
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180)   # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.ROTATE_180)                                    # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.FLIP_LEFT_RIGHT)                               # Performing the mirrroring effect for the GUI image instance. 
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180)       # Performing the mirrroring effect on processing image instance.
              tmp_processing=tmp_processing.transpose(Image.ROTATE_180)                             # Performing the mirrroring effect on processing image instance. 
              image_settings_file.image_processing=tmp_processing.transpose(Image.FLIP_LEFT_RIGHT)  # Performing the mirrroring effect on processing image instance.
              
            self.image_mirror_orientation = "SE" # Update current mirroring position.
            
          elif self.image_mirror_orientation.endswith('W') :
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180)   # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.ROTATE_180)                                    # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180)    # Performing the mirrroring effect on processing image instance.
              image_settings_file.image_processing=tmp_processing.transpose(Image.ROTATE_180)    # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "SW" # Update current mirroring position.
            
          else :
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180)  # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.ROTATE_180)                                   # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180)  # Performing the mirrroring effect on processing image instance.
              image_settings_file.image_processing=tmp_processing.transpose(Image.ROTATE_180)  # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = 'S' # Update current mirroring position.
            
        elif widget.get_name() == "flip up" or flipping == "flip up" :
          # We cannot flip to the up if we are at up.
          return    
      
      
    elif widget.get_name() in ("flip left","flip right") or (flipping in ("flip left","flip right")) :

      if self.image_mirror_orientation.startswith('S') :
        
        if widget.get_name() == "flip left" or flipping == "flip left" :
          
          if self.image_mirror_orientation.endswith('E') :
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180) # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.ROTATE_180)                                  # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180)    # Performing the mirrroring effect on processing image instance.
              image_settings_file.image_processing=tmp_processing.transpose(Image.ROTATE_180)    # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation="SW" # Update current mirroring position.
          
          elif self.image_mirror_orientation.endswith('W') :
            # We cannot flip to the left if we are at left.
            return
          
          
        elif widget.get_name() == "flip right" or flipping == "flip right" :
          
          if self.image_mirror_orientation.endswith('E') :
            # We cannot flip to the right if we are at right.
            return
          
          elif self.image_mirror_orientation.endswith('W') :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_LEFT_RIGHT)    # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              image_settings_file.image_processing=image_settings_file.image_processing.transpose(Image.FLIP_LEFT_RIGHT)    # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "SE" # Update current mirroring position.
          
          else :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_LEFT_RIGHT)    # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              image_settings_file.image_processing=image_settings_file.image_processing.transpose(Image.FLIP_LEFT_RIGHT)    # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "SE" # Update current mirroring position. 
            
      elif self.image_mirror_orientation.startswith('N') :
        
        if widget.get_name() == "flip right" or flipping == "flip right" :
          
          if self.image_mirror_orientation.endswith("W") :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_TOP_BOTTOM)    # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.FLIP_LEFT_RIGHT)                                     # Performing the mirrroring effect for the GUI image instance.
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.FLIP_TOP_BOTTOM)    # Performing the mirrroring effect on processing image instance.
              Image_settings.image_processing=tmp_processing.transpose(Image.FLIP_LEFT_RIGHT)         # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "NE" # Update current mirroring position. 
          
          elif self.image_mirror_orientation.endswith("E") :
            # We cannot flip to the right if we are at right.
            return
          
          else :
            tmp=image_settings_file.image_to_display.transpose(Image.FLIP_TOP_BOTTOM)    # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.FLIP_LEFT_RIGHT)                                     # Performing the mirrroring effect for the GUI image instance. 
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.FLIP_TOP_BOTTOM)    # Performing the mirrroring effect on processing image instance.
              Image_settings.image_processing=tmp_processing.transpose(Image.FLIP_LEFT_RIGHT)         # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "NE" # Update current mirroring position. 
            
            
        elif widget.get_name() == "flip left" or flipping == "flip left" :
          
          if self.image_mirror_orientation.endswith("E") :
            tmp=image_settings_file.image_to_display.transpose(Image.ROTATE_180)    # Performing the mirrroring effect for the GUI image instance.
            tmp=tmp.transpose(Image.FLIP_TOP_BOTTOM)                                # Performing the mirrroring effect for the GUI image instance. 
            tmp=tmp.transpose(Image.ROTATE_180)
            
            if image_settings_file.need_thumbnail :
              tmp_processing=image_settings_file.image_processing.transpose(Image.ROTATE_180)         # Performing the mirrroring effect on processing image instance.
              tmp_processing=image_settings_file.image_processing.transpose(Image.FLIP_TOP_BOTTOM)    # Performing the mirrroring effect on processing image instance.
              image_settings_file.image_processing=tmp_processing.transpose(Image.ROTATE_180)              # Performing the mirrroring effect on processing image instance.
            
            self.image_mirror_orientation = "NW" # Update current mirroring position. 
          
          elif self.image_mirror_orientation.endswith("W") :
            # We cannot flip to the left if we are at left.
            return
          
        
        
          
    # Saving GUI display image and store the settings.
    tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
    image_settings_file.image_to_display_filepath=tmp_path
    tmp.save(tmp_path,format=image_settings_file.image_instance.format)
    self.operation_list_displaying_image.append((tmp,tmp_path))
    
    # Store effect processsing image instance in processing list.
    self.operation_list_image_instance_processing.append(image_settings_file.image_processing)
    
    # Update instance counter.
    image_settings_file.images_counter += 1
    
    # Update GUI with display image instance.
    image_settings_file.configure_image_display()
    image_settings_file.display_image()
    
  def apply_filter(self,widget,event=False,filter_index=False) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    if filter_index == False :
      # The user launch the filter applying from the buttonbar.
      
      # Apply user selection filter on display image instance.
      image_settings_file.image_to_display=image_settings_file.image_to_display.filter(self.filter_dict.get(gui.combo_set_filters.get_active()))
      
      # Apply user selection filter on processing image instance.
      image_settings_file.image_processing=image_settings_file.image_processing.filter(self.filter_dict.get(gui.combo_set_filters.get_active()))
    
    else :
      # The user launch the filter applying from the menu.
      
      # Apply user selection filter on display image instance.
      image_settings_file.image_to_display=image_settings_file.image_to_display.filter(self.filter_dict.get(filter_index))
      
      # Apply user selection filter on processing image instance.
      image_settings_file.image_processing=image_settings_file.image_processing.filter(self.filter_dict.get(filter_index))
      
    
    # Saving GUI display image and store the settings.
    tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
    image_settings_file.image_to_display_filepath=tmp_path
    image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
    self.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
    
    # Store effect processsing image instance in processing list.
    self.operation_list_image_instance_processing.append(image_settings_file.image_processing)
    
    # Update instance counter.
    image_settings_file.images_counter += 1
    
    # Update GUI with display image instance.
    image_settings_file.configure_image_display()
    image_settings_file.display_image()
  
  def apply_adjustment(self,type_of_computing=1,value=1.0) :
    if type_of_computing == 1 :
      # Apply user selection Enhance on display image instance.
      image_to_display_enhance=ImageEnhance.Color(image_settings_file.image_to_display)
      
      # Apply user selection Enhance on processing image instance.
      image_processing_enhance=ImageEnhance.Color(image_settings_file.image_processing)
     
    elif type_of_computing == 2 :
      # Apply user selection Enhance on display image instance.
      image_to_display_enhance=ImageEnhance.Brightness(image_settings_file.image_to_display)
      
      # Apply user selection Enhance on processing image instance.
      image_processing_enhance=ImageEnhance.Brightness(image_settings_file.image_processing) 
    
    elif type_of_computing == 3 :
      # Apply user selection Enhance on display image instance.
      image_to_display_enhance=ImageEnhance.Contrast(image_settings_file.image_to_display)
      
      # Apply user selection Enhance on processing image instance.
      image_processing_enhance=ImageEnhance.Contrast(image_settings_file.image_processing) 
    
    elif type_of_computing == 4 :
      # Apply user selection Enhance on display image instance.
      image_to_display_enhance=ImageEnhance.Sharpness(image_settings_file.image_to_display)
      
      # Apply user selection Enhance on processing image instance.
      image_processing_enhance=ImageEnhance.Sharpness(image_settings_file.image_processing) 
    
    image_settings_file.image_to_display=image_to_display_enhance.enhance(value)  
    image_settings_file.image_processing=image_processing_enhance.enhance(value)
	
    # Saving GUI display image and store the settings.
    tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
    image_settings_file.image_to_display_filepath=tmp_path
    image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
    self.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
    
    # Store effect processsing image instance in processing list.
    self.operation_list_image_instance_processing.append(image_settings_file.image_processing)
    
    # Update instance counter.
    image_settings_file.images_counter += 1
    
    # Update GUI with display image instance.
    image_settings_file.configure_image_display()
    image_settings_file.display_image()	
	
    
  
  def acquire_data_from_image(self) :
    # Internal PIL method for image data getting.
    image_settings_file.image_to_display.getdata()
    image_settings_file.image_processing.getdata()
    
    # Getting image to display pixels array and count.
    self.image_to_display_pixels_array=list(image_settings_file.image_to_display.im)
    self.image_to_display_pixels_count=len(self.image_to_display_pixels_array)-1
    
    # Getting processing image instance pixels array and count.
    self.processing_image_pixels_array=list(image_settings_file.image_processing.im)
    self.processing_image_pixels_count=len(self.processing_image_pixels_array)-1
  
  def set_grayscale(self,widget,event,base=False) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    # Getting pixels values from display and processing image instance.
    self.acquire_data_from_image()
    
    if not base :
      # The user launch the grayscaling operation from the buttonbar button.
      # Getting user grayscale computing settings.
      self.processing_type=self.grayscale_dict.get(gui.combo_set_grayscale.get_active())
    else :
      # The user launch the grayscaling operation from the menu.
      # Getting user grayscale computing settings.
      self.processing_type=base  
    
    # Launch grayscaling operation on every pixel with progressbar displaying.
    gui.create_progressbar_dialog(self.processing_type)
    
  def set_intensity_change(self,widget,event) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    # Getting pixels values from display and processing image instance.
    self.acquire_data_from_image()
    
    if gui.set_intensity_action == "RGBA" :  # The user has change the colors intensity last.   
     
      # Launch colors intensity change operation on every pixel with progressbar displaying.
      gui.create_progressbar_dialog("colors intensity") 
    
    elif gui.set_intensity_action == "ALL" : # The user has change the global intensity last.  
      
      # Launch global intensity change operation on every pixel with progressbar displaying.
      gui.create_progressbar_dialog("global colors intensity")    
      
      
  def set_colors_inverting_matrix(self,widget,event) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    # Getting pixels values from display and processing image instance.
    self.acquire_data_from_image()
    
    # Getting the settings input from the user.
    gui.get_color_inverting_matrix()
    
    # Launch color inverting operation on every pixel with progressbar displaying.
    gui.create_progressbar_dialog("colors inverting matrix")  
  
  def set_colors_percent_matrix(self,widget,event) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if self.do_undo :
      self.update_after_undo()

    
    color_matrix_dialog=Color_matrix_dialog()  # Instantiate the color scaling matrix dialog class. 
    
    # Display the color scaling matrix dialog window. 
    # And getting users settings.
    red_percents_factors,green_percents_factors,blue_percents_factors,self.alpha_value=color_matrix_dialog.create_dialog() 
    
    del(color_matrix_dialog)
    
    if red_percents_factors and green_percents_factors and blue_percents_factors and self.alpha_value :
      
      # Getting pixels values from display and processing image instance.
      self.acquire_data_from_image()
      
      # Computing the user inputs to pixels multiply factors, for the color red scaling.
      red_red_factor=red_percents_factors[0]/100.
      red_green_factor=red_percents_factors[1]/100.
      red_blue_factor=red_percents_factors[2]/100.
      
      # Computing the user inputs to pixels multiply factors, for the color green scaling.
      green_red_factor=green_percents_factors[0]/100.
      green_green_factor=green_percents_factors[1]/100.
      green_blue_factor=green_percents_factors[2]/100.
      
      # Computing the user inputs to pixels multiply factors, for the color blue scaling.
      blue_red_factor=blue_percents_factors[0]/100.
      blue_green_factor=blue_percents_factors[1]/100.
      blue_blue_factor=blue_percents_factors[2]/100.
      
      # Computing the user inputs to pixels multiply factors, for the alpha channel scaling.
      self.alpha_value=self.alpha_value/100.
      
      # Save user inputs values converted to an pixel multiply for effect processing.
      self.red_values=tuple((red_red_factor,red_green_factor,red_blue_factor))
      self.green_values=tuple((green_red_factor,green_green_factor,green_blue_factor))
      self.blue_values=tuple((blue_red_factor,blue_green_factor,blue_blue_factor))
      
      gui.create_progressbar_dialog("color matrix")
    
    # Getting pixels values from display and processing image instance.
    self.acquire_data_from_image()
  
  def files_mergin(self,widget,event=False,file_merge_type=False) :
    ''' File mergin functionlities main method. '''
    
    if widget.get_name() == "blend" or file_merge_type == "blend" :
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      blend_dialog=Blend_dialog()
      blend_image1_filepath, blend_image1_format, blend_image2_filepath, blend_image2_format, blend_alpha, blend_output = blend_dialog.create_dialog()
      
      if blend_image1_filepath and  blend_image2_filepath and isinstance(blend_alpha,float) and blend_output[0] and blend_output[1]  and blend_output[2][0] and blend_output[2][1] :
        blend_image1_instance=Image.open(blend_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        blend_image2_instance=Image.open(blend_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if blend_image1_instance.mode != blend_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if blend_image1_instance.mode == "RGB" or blend_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=blend_image2_instance.format
	    blend_image2_instance=blend_image2_instance.convert(blend_image1_instance.mode)
	    blend_image2_instance.save("/tmp/PyImaging/pyimage_blend_image2.{0}".format(format_str.lower()))
	    blend_image2_instance=Image.open("/tmp/PyImaging/pyimage_blend_image2.{0}".format(format_str.lower()))
	    
	  
	  elif blend_image2_instance.mode == "RGB" or blend_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=blend_image1_instance.format
	    blend_image1_instance=blend_image1_instance.convert(blend_image2_instance.mode)
	    blend_image1_instance.save("/tmp/PyImaging/pyimage_blend_image1.{0}".format(format_str.lower()))
	    blend_image1_instance=Image.open("/tmp/PyImaging/pyimage_blend_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	     # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      blend_image1_instance=blend_image1_instance.convert("RGB")
	      blend_image1_instance.save("/tmp/PyImaging/pyimage_blend_image1.{0}".format(format_str.lower()))
	      blend_image1_instance=Image.open("/tmp/PyImaging/pyimage_blend_image1.{0}".format(format_str.lower()))
	      
	      blend_image2_instance=blend_image2_instance.convert("RGB")
	      blend_image2_instance.save("/tmp/PyImaging/pyimage_blend_image2.{0}".format(format_str.lower()))
	      blend_image2_instance=Image.open("/tmp/PyImaging/pyimage_blend_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      blend_dialog.blend_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(blend_image1_filepath,blend_image2_filepath)
	      del(blend_dialog)                   # Deletion of the toplevel containing class instance.
	      return 
	  
	# Image 1 resizing and creation of an temporary file which we store the path for futur use.
	blend_image1_instance=blend_image1_instance.resize(blend_output[2])
	blend_image1_path="/tmp/PyImaging/pyimage_blend_image1.{0}".format(blend_output[1].lower())
	blend_image1_instance.save(blend_image1_path,format=blend_image1_format)
	
	# Image 2 resizing and creation of an temporary file which we store the path for futur use.
	blend_image2_instance=blend_image2_instance.resize(blend_output[2])
	blend_image2_path="/tmp/PyImaging/pyimage_blend_image2.{0}".format(blend_output[1].lower())
	blend_image2_instance.save(blend_image2_path,format=blend_image2_format)
	  
      
	  
  
	blend_image1_instance=Image.open(blend_image1_path) # Open the temporary file, which is resized, for apply blend function. 
	blend_image2_instance=Image.open(blend_image2_path) # Open the temporary file, which is resized, for apply blend function.  
	
	try :
	  # Applying of the blend function of the resized temporary files and result file saving.
	  blend_output_image_instance=Image.blend(blend_image1_instance, blend_image2_instance, blend_alpha)
	  blend_output_image_instance.save(blend_output[0],format=blend_output[1])
	except :
	  error_file_mergin_message(blend_image1_filepath,blend_image2_filepath)  
        
      
      
      blend_dialog.blend_dialog.destroy() # Dialog destroying.
      
      del(blend_dialog)                   # Deletion of the toplevel containing class instance.
      
    elif widget.get_name() == "composite" or file_merge_type == "composite" :
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      composite_dialog=Composite_dialog()
      composite_image1_filepath, composite_image1_format, composite_image2_filepath, composite_image2_format, composite_image_mask_filepath, composite_image_mask_format, composite_output = composite_dialog.create_dialog()
      
      if composite_image1_filepath and  composite_image2_filepath and composite_image_mask_filepath and composite_output[0] and composite_output[1]  and composite_output[2][0] and composite_output[2][1] :
        composite_image1_instance=Image.open(composite_image1_filepath)          # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        composite_image2_instance=Image.open(composite_image2_filepath)          # Open the image 2, given from the user, needed for applying resizing, to the same size, operations.
        composite_image_mask_instance=Image.open(composite_image_mask_filepath)  # Open the mask image, given from the user, needed for applying resizing, to the same size, operations.
        
        
	if composite_image1_instance.mode != composite_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if composite_image1_instance.mode == "RGB" or composite_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=composite_image2_instance.format
	    composite_image2_instance=composite_image2_instance.convert(composite_image1_instance.mode)
	    composite_image2_instance.save("/tmp/PyImaging/pyimage_composite_image2.{0}".format(format_str.lower()))
	    composite_image2_instance=Image.open("/tmp/PyImaging/pyimage_composite_image2.{0}".format(format_str.lower()))
	    
	    
	  elif composite_image2_instance.mode == "RGB" or composite_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=composite_image1_instance.format
	    composite_image1_instance=composite_image1_instance.convert(composite_image2_instance.mode)
	    composite_image1_instance.save("/tmp/PyImaging/pyimage_composite_image1.{0}".format(format_str.lower()))
	    composite_image1_instance=Image.open("/tmp/PyImaging/pyimage_composite_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      composite_image1_instance=composite_image1_instance.convert("RGB")
	      composite_image1_instance.save("/tmp/PyImaging/pyimage_composite_image1.{0}".format(format_str.lower()))
	      composite_image1_instance=Image.open("/tmp/PyImaging/pyimage_composite_image1.{0}".format(format_str.lower()))
	      
	      composite_image2_instance=composite_image2_instance.convert("RGB")
	      composite_image2_instance.save("/tmp/PyImaging/pyimage_composite_image2.{0}".format(format_str.lower()))
	      composite_image2_instance=Image.open("/tmp/PyImaging/pyimage_composite_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      composite_dialog.composite_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(composite_image1_filepath,composite_image2_filepath)
              del(composite_dialog)                       # Deletion of the toplevel containing class instance.
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        composite_image1_instance=composite_image1_instance.resize(composite_output[2])
        composite_image1_path="/tmp/PyImaging/pyimage_composite_image1.{0}".format(composite_image1_format.lower())
        composite_image1_instance.save(composite_image1_path,format=composite_image1_format)
        
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        composite_image2_instance=composite_image2_instance.resize(composite_output[2])
        composite_image2_path="/tmp/PyImaging/pyimage_composite_image2.{0}".format(composite_image2_format.lower())
        composite_image2_instance.save(composite_image2_path,format=composite_image2_format)
        
        # Image mask resizing and creation of an temporary file which we store the path for futur use.
        composite_image_mask_instance=composite_image_mask_instance.resize(composite_output[2])
        composite_image_mask_path="/tmp/PyImaging/pyimage_composite_image_mask.{0}".format(composite_image_mask_format.lower())
        composite_image_mask_instance.save(composite_image_mask_path,format=composite_image_mask_format)
          
   
        composite_image1_instance=Image.open(composite_image1_path)         # Open the temporary file, which is resized, for apply composite function. 
        composite_image2_instance=Image.open(composite_image2_path)         # Open the temporary file, which is resized, for apply composite function. 
        composite_image_mask_instance=Image.open(composite_image_mask_path) # Open the temporary file, which is resized, for apply composite function. 
        
        
        try :
          # Applying of the composite function of the resized temporary files and result file saving.
          composite_output_image_instance=Image.composite(composite_image1_instance, composite_image2_instance, composite_image_mask_instance)
          composite_output_image_instance.save(composite_output[0],format=composite_output[1])
        except :
	  error_file_mergin_message(composite_image1_filepath,composite_image2_filepath)  
      
      
      composite_dialog.composite_dialog.destroy() # Dialog destroying.
      
      del(composite_dialog)                       # Deletion of the toplevel containing class instance.
      
  
    elif widget.get_name() == "screen" or file_merge_type == "screen" :
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      screen_dialog=Screen_dialog()
      screen_image1_filepath, screen_image1_format, screen_image2_filepath, screen_image2_format, screen_output = screen_dialog.create_dialog()
      
      if screen_image1_filepath and  screen_image2_filepath and screen_output[0] and screen_output[1]  and screen_output[2][0] and screen_output[2][1] :
        screen_image1_instance=Image.open(screen_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        screen_image2_instance=Image.open(screen_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if screen_image1_instance.mode != screen_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if screen_image1_instance.mode == "RGB" or screen_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=screen_image2_instance.format
	    screen_image2_instance=screen_image2_instance.convert(screen_image1_instance.mode)
	    screen_image2_instance.save("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	    screen_image2_instance=Image.open("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	    
	  
	  elif screen_image2_instance.mode == "RGB" or screen_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=screen_image1_instance.format
	    screen_image1_instance=screen_image1_instance.convert(screen_image2_instance.mode)
	    screen_image1_instance.save("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	    screen_image1_instance=Image.open("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      screen_image1_instance=screen_image1_instance.convert("RGB")
	      screen_image1_instance.save("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	      screen_image1_instance=Image.open("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	      
	      screen_image2_instance=screen_image2_instance.convert("RGB")
	      screen_image2_instance.save("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	      screen_image2_instance=Image.open("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      screen_dialog.screen_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(screen_image1_filepath,screen_image2_filepath)
              del(screen_dialog)                    # Deletion of the toplevel containing class instance.
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        screen_image1_instance=screen_image1_instance.resize(screen_output[2])
        screen_image1_path="/tmp/PyImaging/pyimage_screen_image1.{0}".format(screen_image1_format.lower())
        screen_image1_instance.save(screen_image1_path,format=screen_image1_format)
        
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        screen_image2_instance=screen_image2_instance.resize(screen_output[2])
        screen_image2_path="/tmp/PyImaging/pyimage_screen_image2.{0}".format(screen_image2_format.lower())
        screen_image2_instance.save(screen_image2_path,format=screen_image2_format)
          
   
        screen_image1_instance=Image.open(screen_image1_path) # Open the temporary file, which is resized, for apply screen function. 
        screen_image2_instance=Image.open(screen_image2_path) # Open the temporary file, which is resized, for apply screen function.   
        
        try :
	  # Applying of the screen function of the resized temporary files and result file saving.
	  screen_output_image_instance=ImageChops.screen(screen_image1_instance, screen_image2_instance)
	  screen_output_image_instance.save(screen_output[0],format=screen_output[1])
        except :
	  error_file_mergin_message(screen_image1_filepath,screen_image2_filepath)
      
      
      screen_dialog.screen_dialog.destroy() # Dialog destroying.
      
      del(screen_dialog)                    # Deletion of the toplevel containing class instance.
      
    elif file_merge_type == "darker" : 
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      darker_dialog=Darker_dialog()
      darker_image1_filepath, darker_image1_format, darker_image2_filepath, darker_image2_format, darker_output = darker_dialog.create_dialog()
      
      if darker_image1_filepath and  darker_image2_filepath and darker_output[0] and darker_output[1]  and darker_output[2][0] and darker_output[2][1] :
        darker_image1_instance=Image.open(darker_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        darker_image2_instance=Image.open(darker_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if darker_image1_instance.mode != darker_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if darker_image1_instance.mode == "RGB" or darker_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=darker_image2_instance.format
	    darker_image2_instance=darker_image2_instance.convert(darker_image1_instance.mode)
	    darker_image2_instance.save("/tmp/PyImaging/pyimage_darker_image2.{0}".format(format_str.lower()))
	    darker_image2_instance=Image.open("/tmp/PyImaging/pyimage_darker_image2.{0}".format(format_str.lower()))
	    
	    
	  elif darker_image2_instance.mode == "RGB" or darker_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=darker_image1_instance.format
	    darker_image1_instance=darker_image1_instance.convert(darker_image2_instance.mode)
	    darker_image1_instance.save("/tmp/PyImaging/pyimage_darker_image1.{0}".format(format_str.lower()))
	    darker_image1_instance=Image.open("/tmp/PyImaging/pyimage_darker_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      darker_image1_instance=darker_image1_instance.convert("RGB")
	      darker_image1_instance.save("/tmp/PyImaging/pyimage_darker_image1.{0}".format(format_str.lower()))
	      darker_image1_instance=Image.open("/tmp/PyImaging/pyimage_darker_image1.{0}".format(format_str.lower()))
	      
	      darker_image2_instance=darker_image2_instance.convert("RGB")
	      darker_image2_instance.save("/tmp/PyImaging/pyimage_darker_image2.{0}".format(format_str.lower()))
	      darker_image2_instance=Image.open("/tmp/PyImaging/pyimage_darker_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      darker_dialog.darker_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(darker_image1_filepath,darker_image2_filepath)
	      del(darker_dialog)                    # Deletion of the toplevel containing class instance.
	      return 
	  
	# Image 1 resizing and creation of an temporary file which we store the path for futur use.
	darker_image1_instance=darker_image1_instance.resize(darker_output[2])
	darker_image1_path="/tmp/PyImaging/pyimage_darker_image1.{0}".format(darker_image1_format.lower())
	darker_image1_instance.save(darker_image1_path,format=darker_image1_format)
	
	# Image 2 resizing and creation of an temporary file which we store the path for futur use.
	darker_image2_instance=darker_image2_instance.resize(darker_output[2])
	darker_image2_path="/tmp/PyImaging/pyimage_darker_image2.{0}".format(darker_image2_format.lower())
	darker_image2_instance.save(darker_image2_path,format=darker_image2_format)
	  
  
	darker_image1_instance=Image.open(darker_image1_path) # Open the temporary file, which is resized, for apply darker function.
	darker_image2_instance=Image.open(darker_image2_path) # Open the temporary file, which is resized, for apply darker function. 
	
	try :
	  # Applying of the darker function of the resized temporary files and result file saving.
	  darker_output_image_instance=ImageChops.darker(darker_image1_instance, darker_image2_instance)
	  darker_output_image_instance.save(darker_output[0],format=darker_output[1])
	except :
	  error_file_mergin_message(darker_image1_filepath,darker_image2_filepath)
      
      
      darker_dialog.darker_dialog.destroy() # Dialog destroying.
      
      del(darker_dialog)                    # Deletion of the toplevel containing class instance.
      
    elif file_merge_type == "lighter" :
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      lighter_dialog=Lighter_dialog()
      lighter_image1_filepath, lighter_image1_format, lighter_image2_filepath, lighter_image2_format, lighter_output = lighter_dialog.create_dialog()
      
      if lighter_image1_filepath and  lighter_image2_filepath and lighter_output[0] and lighter_output[1]  and lighter_output[2][0] and lighter_output[2][1] :
        lighter_image1_instance=Image.open(lighter_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations.
        lighter_image2_instance=Image.open(lighter_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations.
        
        
	if lighter_image1_instance.mode != lighter_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if lighter_image1_instance.mode == "RGB" or lighter_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=lighter_image2_instance.format
	    lighter_image2_instance=lighter_image2_instance.convert(lighter_image1_instance.mode)
	    lighter_image2_instance.save("/tmp/PyImaging/pyimage_lighter_image2.{0}".format(format_str.lower()))
	    lighter_image2_instance=Image.open("/tmp/PyImaging/pyimage_lighter_image2.{0}".format(format_str.lower()))
	    
	    
	  elif lighter_image2_instance.mode == "RGB" or lighter_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=lighter_image1_instance.format
	    lighter_image1_instance=lighter_image1_instance.convert(lighter_image2_instance.mode)
	    lighter_image1_instance.save("/tmp/PyImaging/pyimage_lighter_image1.{0}".format(format_str.lower()))
	    lighter_image1_instance=Image.open("/tmp/PyImaging/pyimage_lighter_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      lighter_image1_instance=lighter_image1_instance.convert("RGB")
	      lighter_image1_instance.save("/tmp/PyImaging/pyimage_lighter_image1.{0}".format(format_str.lower()))
	      lighter_image1_instance=Image.open("/tmp/PyImaging/pyimage_lighter_image1.{0}".format(format_str.lower()))
	      
	      lighter_image2_instance=lighter_image2_instance.convert("RGB")
	      lighter_image2_instance.save("/tmp/PyImaging/pyimage_lighter_image2.{0}".format(format_str.lower()))
	      lighter_image2_instance=Image.open("/tmp/PyImaging/pyimage_lighter_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      lighter_dialog.lighter_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(lighter_image1_filepath,lighter_image2_filepath)
	      del(lighter_dialog)                     # Deletion of the toplevel containing class instance.
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        lighter_image1_instance=lighter_image1_instance.resize(lighter_output[2])
        lighter_image1_path="/tmp/PyImaging/pyimage_lighter_image1.{0}".format(lighter_image1_format.lower())
        lighter_image1_instance.save(lighter_image1_path,format=lighter_image1_format)
        
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        lighter_image2_instance=lighter_image2_instance.resize(lighter_output[2])
        lighter_image2_path="/tmp/PyImaging/pyimage_lighter_image2.{0}".format(lighter_image2_format.lower())
        lighter_image2_instance.save(lighter_image2_path,format=lighter_image2_format)
        
   
        lighter_image1_instance=Image.open(lighter_image1_path) # Open the temporary file, which is resized, for apply lighter function.
        lighter_image2_instance=Image.open(lighter_image2_path) # Open the temporary file, which is resized, for apply lighter function. 
        
        try :
          # Applying of the lighter function of the resized temporary files and result file saving.
          lighter_output_image_instance=ImageChops.lighter(lighter_image1_instance, lighter_image2_instance)
          lighter_output_image_instance.save(lighter_output[0],format=lighter_output[1])
        except :
	  error_file_mergin_message(lighter_image1_filepath,lighter_image2_filepath)
      
      
      lighter_dialog.lighter_dialog.destroy() # Dialog destroying.
      
      del(lighter_dialog)                     # Deletion of the toplevel containing class instance.
      
    elif file_merge_type == "difference" : 
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      difference_dialog=Difference_dialog()
      difference_image1_filepath, difference_image1_format, difference_image2_filepath, difference_image2_format, difference_output = difference_dialog.create_dialog()
      
      if difference_image1_filepath and  difference_image2_filepath and difference_output[0] and difference_output[1]  and difference_output[2][0] and difference_output[2][1] :
        difference_image1_instance=Image.open(difference_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        difference_image2_instance=Image.open(difference_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if difference_image1_instance.mode != difference_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if difference_image1_instance.mode == "RGB" or difference_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=difference_image2_instance.format
	    difference_image2_instance=difference_image2_instance.convert(difference_image1_instance.mode)
	    difference_image2_instance.save("/tmp/PyImaging/pyimage_difference_image2.{0}".format(format_str.lower()))
	    difference_image2_instance=Image.open("/tmp/PyImaging/pyimage_difference_image2.{0}".format(format_str.lower()))
	    
	    
	  elif difference_image2_instance.mode == "RGB" or difference_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=difference_image1_instance.format
	    difference_image1_instance=difference_image1_instance.convert(difference_image2_instance.mode)
	    difference_image1_instance.save("/tmp/PyImaging/pyimage_difference_image1.{0}".format(format_str.lower()))
	    difference_image1_instance=Image.open("/tmp/PyImaging/pyimage_difference_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      difference_image1_instance=difference_image1_instance.convert("RGB")
	      difference_image1_instance.save("/tmp/PyImaging/pyimage_difference_image1.{0}".format(format_str.lower()))
	      difference_image1_instance=Image.open("/tmp/PyImaging/pyimage_difference_image1.{0}".format(format_str.lower()))
	      
	      difference_image2_instance=difference_image2_instance.convert("RGB")
	      difference_image2_instance.save("/tmp/PyImaging/pyimage_difference_image2.{0}".format(format_str.lower()))
	      difference_image2_instance=Image.open("/tmp/PyImaging/pyimage_difference_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      difference_dialog.difference_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(difference_image1_filepath,difference_image2_filepath)
              del(difference_dialog)                        # Deletion of the toplevel containing class instance. 
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        difference_image1_instance=difference_image1_instance.resize(difference_output[2])
        difference_image1_path="/tmp/PyImaging/pyimage_difference_image1.{0}".format(difference_image1_format.lower())
        difference_image1_instance.save(difference_image1_path,format=difference_image1_format)
          
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        difference_image2_instance=difference_image2_instance.resize(difference_output[2])
        difference_image2_path="/tmp/PyImaging/pyimage_difference_image2.{0}".format(difference_image2_format.lower())
        difference_image2_instance.save(difference_image2_path,format=difference_image2_format)
          
   
        difference_image1_instance=Image.open(difference_image1_path) # Open the temporary file, which is resized, for apply difference function.
        difference_image2_instance=Image.open(difference_image2_path) # Open the temporary file, which is resized, for apply difference function.  
        
        try :
          # Applying of the difference function of the resized temporary files and result file saving.
          difference_output_image_instance=ImageChops.difference(difference_image1_instance, difference_image2_instance)
          difference_output_image_instance.save(difference_output[0],format=difference_output[1])
        except :
	  error_file_mergin_message(difference_image1_filepath,difference_image2_filepath)
      
      
      difference_dialog.difference_dialog.destroy() # Dialog destroying.
      
      del(difference_dialog)                        # Deletion of the toplevel containing class instance. 
      
    elif file_merge_type == "multiply" :
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      multiply_dialog=Multiply_dialog()
      multiply_image1_filepath, multiply_image1_format, multiply_image2_filepath, multiply_image2_format, multiply_output = multiply_dialog.create_dialog()
      
      if multiply_image1_filepath and  multiply_image2_filepath and multiply_output[0] and multiply_output[1]  and multiply_output[2][0] and multiply_output[2][1] :
        multiply_image1_instance=Image.open(multiply_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations.
        multiply_image2_instance=Image.open(multiply_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations.
        
        
	if multiply_image1_instance.mode != multiply_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if multiply_image1_instance.mode == "RGB" or multiply_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=multiply_image2_instance.format
	    multiply_image2_instance=multiply_image2_instance.convert(multiply_image1_instance.mode)
	    multiply_image2_instance.save("/tmp/PyImaging/pyimage_multiply_image2.{0}".format(format_str.lower()))
	    multiply_image2_instance=Image.open("/tmp/PyImaging/pyimage_multiply_image2.{0}".format(format_str.lower()))
	    
	    
	  elif multiply_image2_instance.mode == "RGB" or multiply_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=multiply_image1_instance.format
	    multiply_image1_instance=multiply_image1_instance.convert(multiply_image2_instance.mode)
	    multiply_image1_instance.save("/tmp/PyImaging/pyimage_multiply_image1.{0}".format(format_str.lower()))
	    multiply_image1_instance=Image.open("/tmp/PyImaging/pyimage_multiply_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      multiply_image1_instance=multiply_image1_instance.convert("RGB")
	      multiply_image1_instance.save("/tmp/PyImaging/pyimage_multiply_image1.{0}".format(format_str.lower()))
	      multiply_image1_instance=Image.open("/tmp/PyImaging/pyimage_multiply_image1.{0}".format(format_str.lower()))
	      
	      multiply_image2_instance=multiply_image2_instance.convert("RGB")
	      multiply_image2_instance.save("/tmp/PyImaging/pyimage_multiply_image2.{0}".format(format_str.lower()))
	      multiply_image2_instance=Image.open("/tmp/PyImaging/pyimage_multiply_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      multiply_dialog.multiply_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(multiply_image1_filepath,multiply_image2_filepath)
              del(multiply_dialog)                      # Deletion of the toplevel containing class instance. 
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        multiply_image1_instance=multiply_image1_instance.resize(multiply_output[2])
        multiply_image1_path="/tmp/PyImaging/pyimage_multiply_image1.{0}".format(multiply_image1_format.lower())
        multiply_image1_instance.save(multiply_image1_path,format=multiply_image1_format)
        
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        multiply_image2_instance=multiply_image2_instance.resize(multiply_output[2])
        multiply_image2_path="/tmp/PyImaging/pyimage_multiply_image2.{0}".format(multiply_image2_format.lower())
        multiply_image2_instance.save(multiply_image2_path,format=multiply_image2_format)
          
   
        multiply_image1_instance=Image.open(multiply_image1_path) # Open the temporary file, which is resized, for apply multiply function.
        multiply_image2_instance=Image.open(multiply_image2_path) # Open the temporary file, which is resized, for apply multiply function. 
        
        try :
          # Applying of the multiply function of the resized temporary files and result file saving.
          multiply_output_image_instance=ImageChops.multiply(multiply_image1_instance, multiply_image2_instance)
          multiply_output_image_instance.save(multiply_output[0],format=multiply_output[1])
        except :
	  error_file_mergin_message(multiply_image1_filepath,multiply_image2_filepath)
      
      
      multiply_dialog.multiply_dialog.destroy() # Dialog destroying.
      
      del(multiply_dialog)                      # Deletion of the toplevel containing class instance. 
      
    
    elif file_merge_type == "add" : 
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      add_dialog=Add_dialog()
      add_image1_filepath, add_image1_format, add_image2_filepath, add_image2_format, add_scale, add_offset, add_output = add_dialog.create_dialog()
      
      if add_image1_filepath and  add_image2_filepath and add_output[0] and add_output[1]  and add_output[2][0] and add_output[2][1] :
        add_image1_instance=Image.open(add_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        add_image2_instance=Image.open(add_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if add_image1_instance.mode != add_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if add_image1_instance.mode == "RGB" or add_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=add_image2_instance.format
	    add_image2_instance=add_image2_instance.convert(add_image1_instance.mode)
	    add_image2_instance.save("/tmp/PyImaging/pyimage_add_image2.{0}".format(format_str.lower()))
	    add_image2_instance=Image.open("/tmp/PyImaging/pyimage_add_image2.{0}".format(format_str.lower()))
	    
	  
	  elif add_image2_instance.mode == "RGB" or add_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=add_image1_instance.format
	    add_image1_instance=add_image1_instance.convert(add_image2_instance.mode)
	    add_image1_instance.save("/tmp/PyImaging/pyimage_add_image1.{0}".format(format_str.lower()))
	    add_image1_instance=Image.open("/tmp/PyImaging/pyimage_add_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      add_image1_instance=add_image1_instance.convert("RGB")
	      add_image1_instance.save("/tmp/PyImaging/pyimage_add_image1.{0}".format(format_str.lower()))
	      add_image1_instance=Image.open("/tmp/PyImaging/pyimage_add_image1.{0}".format(format_str.lower()))
	      
	      add_image2_instance=add_image2_instance.convert("RGB")
	      add_image2_instance.save("/tmp/PyImaging/pyimage_add_image2.{0}".format(format_str.lower()))
	      add_image2_instance=Image.open("/tmp/PyImaging/pyimage_add_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      add_dialog.add_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(add_image1_filepath,add_image2_filepath)
	      del(add_dialog)                 # Deletion of the toplevel containing class instance. 
	      return 
        
        # Image 1 resizing and creation of an temporary file which we store the path for futur use.
        add_image1_instance=add_image1_instance.resize(add_output[2])
        add_image1_path="/tmp/PyImaging/pyimage_add_image1.{0}".format(add_image1_format.lower())
        add_image1_instance.save(add_image1_path,format=add_image1_format)
        
        # Image 2 resizing and creation of an temporary file which we store the path for futur use.
        add_image2_instance=add_image2_instance.resize(add_output[2])
        add_image2_path="/tmp/PyImaging/pyimage_add_image2.{0}".format(add_image2_format.lower())
        add_image2_instance.save(add_image2_path,format=add_image2_format)
        
   
        add_image1_instance=Image.open(add_image1_path) # Open the temporary file, which is resized, for apply multiply function.
        add_image2_instance=Image.open(add_image2_path) # Open the temporary file, which is resized, for apply multiply function. 
        
        try :
          # Applying of the add function of the resized temporary files and result file saving.
          add_output_image_instance=ImageChops.add(add_image1_instance, add_image2_instance,add_scale,add_offset)
          add_output_image_instance.save(add_output[0],format=add_output[1])
        except :
	  error_file_mergin_message(add_image1_filepath,add_image2_filepath)
      
      
      add_dialog.add_dialog.destroy() # Dialog destroying.
      
      del(add_dialog)                 # Deletion of the toplevel containing class instance. 
      
    elif file_merge_type == "substract" :  
      # Instanciate the toplevel containing class and displaying of the dialog window who return the entered value from the user.
      subtract_dialog=Substract_dialog()
      subtract_image1_filepath, subtract_image1_format, subtract_image2_filepath, subtract_image2_format, subtract_scale, subtract_offset, subtract_output = subtract_dialog.create_dialog()
      
      if subtract_image1_filepath and  subtract_image2_filepath and subtract_output[0] and subtract_output[1]  and subtract_output[2][0] and subtract_output[2][1] :
        subtract_image1_instance=Image.open(subtract_image1_filepath) # Open the image 1, given from the user, needed for applying resizing, to the same size, operations. 
        subtract_image2_instance=Image.open(subtract_image2_filepath) # Open the image 2, given from the user, needed for applying resizing, to the same size, operations. 
        
        
	if subtract_image1_instance.mode != subtract_image2_instance.mode :
	  # The image files to merge must have the same mode.
	  # So that it is not the case we:
	  
	  if subtract_image1_instance.mode == "RGB" or subtract_image1_instance.mode == "P" :
	    # Convert the image file 2 into the mode from image file 1, which is in an generic mode: "RGB" or "P".
	    format_str=subtract_image2_instance.format
	    subtract_image2_instance=subtract_image2_instance.convert(subtract_image1_instance.mode)
	    subtract_image2_instance.save("/tmp/PyImaging/pyimage_subtract_image2.{0}".format(format_str.lower()))
	    subtract_image2_instance=Image.open("/tmp/PyImaging/pyimage_subtract_image2.{0}".format(format_str.lower()))
	    
	  
	  elif subtract_image2_instance.mode == "RGB" or subtract_image2_instance.mode == "P" :
	    # Convert the image file 1 into the mode from image file 2, which is in an generic mode: "RGB" or "P".
	    format_str=subtract_image1_instance.format
	    subtract_image1_instance=subtract_image1_instance.convert(subtract_image2_instance.mode)
	    subtract_image1_instance.save("/tmp/PyImaging/pyimage_subtract_image1.{0}".format(format_str.lower()))
	    subtract_image1_instance=Image.open("/tmp/PyImaging/pyimage_subtract_image1.{0}".format(format_str.lower()))
	    
	    
	  else :
	    # The 2 image files don't are in an generic mode: "RGB" or "P".
	    try :
	      # So we try to convert it into the "RGB" mode.
	      subtract_image1_instance=subtract_image1_instance.convert("RGB")
	      subtract_image1_instance.save("/tmp/PyImaging/pyimage_subtract_image1.{0}".format(format_str.lower()))
	      subtract_image1_instance=Image.open("/tmp/PyImaging/pyimage_subtract_image1.{0}".format(format_str.lower()))
	      
	      subtract_image2_instance=subtract_image2_instance.convert("RGB")
	      subtract_image2_instance.save("/tmp/PyImaging/pyimage_subtract_image2.{0}".format(format_str.lower()))
	      subtract_image2_instance=Image.open("/tmp/PyImaging/pyimage_subtract_image2.{0}".format(format_str.lower()))
	      
	    except :
	      # The image files conversion has failed: we cannot merge the files.
	      subtract_dialog.subtract_dialog.destroy() # Dialog destroying.
	      error_file_mergin_message(subtract_image1_filepath,subtract_image2_filepath)
	      subtract_dialog.subtract_dialog.destroy() # Dialog destroying.
	      del(subtract_dialog)                      # Deletion of the toplevel containing class instance.  
	      return 
	  
	# Image 1 resizing and creation of an temporary file which we store the path for futur use.
	subtract_image1_instance=subtract_image1_instance.resize(subtract_output[2])
	subtract_image1_path="/tmp/PyImaging/pyimage_subtract_image1.{0}".format(subtract_image1_format.lower())
	subtract_image1_instance.save(subtract_image1_path,format=subtract_image1_format)
	
	# Image 2 resizing and creation of an temporary file which we store the path for futur use.
	subtract_image2_instance=subtract_image2_instance.resize(subtract_output[2])
	subtract_image2_path="/tmp/PyImaging/pyimage_subtract_image2.{0}".format(subtract_image2_format.lower())
	subtract_image2_instance.save(subtract_image2_path,format=subtract_image2_format)
	  
  
	subtract_image1_instance=Image.open(subtract_image1_path) # Open the temporary file, which is resized, for apply subtract function.
	subtract_image2_instance=Image.open(subtract_image2_path) # Open the temporary file, which is resized, for apply subtract function. 
	
	try :
	  # Applying of the subtract function of the resized temporary files and result file saving.
	  subtract_output_image_instance=ImageChops.subtract(subtract_image1_instance, subtract_image2_instance,subtract_scale,subtract_offset)
	  subtract_output_image_instance.save(subtract_output[0],format=subtract_output[1])
	except :
	  error_file_mergin_message(subtract_image1_filepath,subtract_image2_filepath)
      
      
      subtract_dialog.subtract_dialog.destroy() # Dialog destroying.
      
      del(subtract_dialog)                      # Deletion of the toplevel containing class instance.  
      
  def display_image_informations(self,widget,event) :
    
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if self.do_undo :
      self.update_after_undo()
    

    # Make an temporary file to get the current image file informations and stats.
    image_informations_path="/tmp/PyImaging/pyimage_to_process_info.{0}".format(image_settings_file.image_instance.format.lower())
    image_settings_file.image_processing.save(image_informations_path,image_settings_file.image_instance.format)   
    
    image_informations_instance=Image.open(image_informations_path)
    
    # Create and display image file informations and stats.
    informations_dialog=Informations_dialog(image_informations_instance,image_settings_file.image_instance.filename)
    informations_dialog.create_dialog()
    
    del(informations_dialog)
    
    
      
class Image_settings() :
  def __init__(self) :
    self.container_width,self.container_height=695,545 # Size of the image (maybe a thumbnail) wieving container. 
    self.images_counter=0                              # Counter. 
    self.user_home=expanduser('~')                     # User home directory path.
    self.image_instance_is_loaded=False                # Indicator if an image is curently loaded.
   
  def create_tmp_dir(self) :
    if not isdir("/tmp/PyImaging") :
      mkdir("/tmp/PyImaging")
      chmod("/tmp/PyImaging",0777)
    else :
      chmod("/tmp/PyImaging",0777)
      
   
  def choose_image(self,widget,event=False) :
    ''' Function to call the file selector for loading an image '''
    
    file_load_selector=File_Loading_Selector()
    
    self.image_filepath = file_load_selector.select_file()
    
    
    file_load_selector.select_file_toplevel.destroy()
    
    self.create_tmp_dir()
    
    if self.image_filepath :
      if self.load_image_settings(self.image_filepath) :
        self.configure_image_display()
        self.display_image()
      else :
        gui.load_error_dialog(self.image_filepath)
  
  def save_image(self,widget,event=False) :
    ''' Function to call the file selector for saving an image '''
    
    file_saving_Selector=File_Saving_Selector(format_str="."+self.image_instance.format.lower(),mode=self.mode,size=[self.image_processing_width,self.image_processing_height],width_factor=self.image_size_width_factor,height_factor=self.image_size_height_factor,processing_instance=self.image_processing)
    has_saved=file_saving_Selector.select_file()
    file_saving_Selector.select_file_toplevel.destroy()
    
  def check_thumbnail(self) :
    ''' Check if we need to used an thumbnail for displaying the user selected image in the GUI image display container. '''
    
    self.need_thumbnail = self.image_width > self.container_width-10 or self.image_height > self.container_height-10
  
  def check_rotation_resizing_needed(self) :
    ''' Check if we need to resize the image by rotating operations, in case the image is larger than heigher. ''' 
        
    self.rotate_90_need_thumbnail_H=self.image_to_display_width > self.container_height 
    self.rotate_90_need_thumbnail_V=self.image_to_display_height > self.container_width
  
  def load_image_settings(self,filepath) :
    ''' Loading the image and processing of thumbling if needed and storage of some image attributes and image instances. ''' 
    
    self.image_instance=Image.open(filepath)
          
    self.image_instance_is_loaded=True
    
    # (Re)Set the undo|redo images instances containing list and counter.
    process_effect.operation_list_displaying_image=[]
    process_effect.operation_list_image_instance_processing=[]
    # Mirroring position.
    process_effect.image_mirror_orientation="S"
    # Resizing by rotating.
    process_effect.rotate_resized=False
    
    self.images_counter=0  
    
    self.image_width,self.image_height=self.image_instance.size 
    self.image_size_width_factor=float(self.image_height)/float(self.image_width)
    self.image_size_height_factor=float(self.image_width)/float(self.image_height) 
    
    self.mode=self.image_instance.mode
    
    # Creating an image processing instance.
    self.image_processing=self.image_instance.convert("RGBA")
    
    
    self.image_has_alpha=False 
    
    try : 
      self.image_processing.save("/tmp/PyImaging/pyimage_to_process.{0}".format(self.image_instance.format.lower()),self.image_instance.format) 
      self.image_has_alpha=True
    except :
      self.image_processing=self.image_instance.convert("RGB")
      try :
        self.image_processing.save("/tmp/PyImaging/pyimage_to_process.{0}".format(self.image_instance.format.lower()),self.image_instance.format) 
      except :
        return False
      
    self.image_processing_width,self.image_processing_height=self.image_width,self.image_height
    
    self.check_thumbnail()
    
    
    if self.need_thumbnail :
      # We must display an thumbnail of the image to the user.
      
      if self.image_has_alpha :
        # Ceation of image to display. 
        self.image_to_display = self.image_instance.convert("RGBA")
           
      else :
        # Ceation of image to display.
        self.image_to_display = self.image_instance.convert("RGB")
        
      # Resizing to thumbnail size.
      resizing=Resizer()
      image_new_size=resizing.resizer(self.image_filepath,self.container_width-10,self.container_height-10)
      
      # Storage of GUI display image width and height.
      self.image_to_display_width,self.image_to_display_height=int(image_new_size[0]),int(image_new_size[1])
      
      # Creating the thumbnail.
      self.image_to_display.thumbnail((int(image_new_size[0]),int(image_new_size[1])),Image.ANTIALIAS)
      self.image_to_display_filepath="/tmp/PyImaging/pyimage_to_display.{0}".format(self.image_instance.format.lower())
      
      
      
      self.image_to_display.save(self.image_to_display_filepath, format=self.image_to_display.format)
      
      
      
    else :
      # The image is little enought for direct GUI displaying.
      if self.image_has_alpha :
        self.image_to_display = self.image_instance.convert("RGBA")
   
      else :
        self.image_to_display = self.image_instance.convert("RGB")
        
      self.image_to_display_width,self.image_to_display_height=self.image_width,self.image_height
      
      self.image_to_display_filepath=self.image_filepath
    
    
    process_effect.operation_list_displaying_image.append((self.image_to_display,self.image_to_display_filepath))
    process_effect.operation_list_image_instance_processing.append(self.image_processing)
    
    self.images_counter += 1
    
    self.check_rotation_resizing_needed()   
    
    return True
  
  def configure_image_display(self) :
    ''' Function to update the GUI image instance we display tro the user. '''
    try :
      self.image_to_display_widget.destroy()
    except :
      pass
       
    self.image_to_display_widget=gtk.Image()
    self.image_to_display_widget.set_from_file(self.image_to_display_filepath)
    self.image_to_display_widget.show()
     
  def display_image(self) :
    ''' Function to positioning the GUI image and to put it into the container. '''
    
    # Computing so that the image is centered in the GUI. 
    pos_x,pos_y=(self.container_width/2)-(self.image_to_display_width/2),(self.container_height/2)-(self.image_to_display_height/2)
    
  
    gui.fixed.put(self.image_to_display_widget,pos_x,pos_y)
    
    

class GUI() :
  def __init__(self) :
    global process_effect,image_settings_file
    
    process_effect=Process_effects()
    image_settings_file=Image_settings()
    
    self.predefine_color_inverting_matrix_index=0
    
    self.red_intensity_value=0
    self.green_intensity_value=0
    self.blue_intensity_value=0
    self.alpha_intensity_value=0
    
    self.global_intensity_value=0
    
    self.set_intensity_action=False
    
    self.is_computing=False
    
    self.main_window=gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.main_window.set_border_width(10)
    self.main_window.set_title('PyImaging')
    self.main_window.set_resizable(False)
    self.main_window.set_size_request(645+345,600+96)
    self.main_window.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#505050'))
    #self.main_window.modify_fg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#404040'))
    
    
    self.main_vbox=gtk.VBox()
    
    self.config_menubar()
    
    self.load_execution_speed()
    
    
    self.upper_vbox=gtk.VBox()
    
    self.upper_vbox.set_size_request(640+335,151)
    self.upper_vbox.set_border_width(5)
    
    
    self.buttonbox_top_container=gtk.EventBox()
    self.buttonbox_top_container.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#c0c0c0'))
    
    self.buttonbox_top=gtk.Toolbar() #gtk.Toolbar()
    self.buttonbox_top.modify_bg(gtk.STATE_NORMAL,self.buttonbox_top.get_colormap().alloc_color('#c0c0c0'))
    self.buttonbox_top.set_size_request(640+345,(150-48)/2)
    
    self.config_button_box_top()
    
    self.buttonbox_top.show()
    
    
    self.buttonbox_bottom_container=gtk.EventBox()
    self.buttonbox_bottom_container.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#c0c0c0'))
    
    self.buttonbox_bottom=gtk.Toolbar()
    self.buttonbox_bottom.modify_bg(gtk.STATE_NORMAL,self.buttonbox_bottom.get_colormap().alloc_color('#c0c0c0'))
    self.buttonbox_bottom.set_size_request(640+345,(150-48)/2)
    
    self.config_button_box_bottom()
    
    self.buttonbox_bottom.show()
    
    
    self.buttonbox_top_container.add(self.buttonbox_top)
    self.buttonbox_top_container.show()
    
    self.buttonbox_bottom_container.add(self.buttonbox_bottom)
    self.buttonbox_bottom_container.show()
    
    
    self.upper_vbox.pack_start(self.menu_bar)
    self.upper_vbox.pack_start(self.buttonbox_top_container)
    self.upper_vbox.pack_start(self.buttonbox_bottom_container)
    self.upper_vbox.show()
    
    self.down_hbox=gtk.HBox()
    self.down_hbox.set_size_request(720+345,580)
    
    
    self.fixed_container=gtk.EventBox()
    self.fixed_container.modify_bg(gtk.STATE_NORMAL,self.fixed_container.get_colormap().alloc_color('#f0f0f0'))
    self.fixed_container.set_border_width(5)
    
    self.fixed= gtk.Fixed() 
    self.fixed.set_size_request(720,580)
    
    
    self.fixed.show()
    
    self.fixed_container.add(self.fixed)
    self.fixed_container.show()
    
    self.right_vbox_container=gtk.EventBox()
    self.right_vbox_container.modify_bg(gtk.STATE_NORMAL,self.right_vbox_container.get_colormap().alloc_color('#c0c0c0'))
    self.right_vbox_container.set_border_width(5)
    
    self.right_vbox=gtk.VBox()
    self.right_vbox.set_size_request(280,580)
    self.right_vbox.show()
    
    self.right_vbox_container.add(self.right_vbox)
    
    self.config_right_panel()
    
    self.right_vbox_container.show()
    
    self.down_hbox.pack_start(self.fixed_container)
    self.down_hbox.pack_start(self.right_vbox_container)
    self.down_hbox.show()
    
    self.main_vbox.pack_start(self.upper_vbox)
    self.main_vbox.pack_start(self.down_hbox)
    
    self.main_vbox.show()
    
    
  def config_menubar(self) :
    self.menu_bar=gtk.MenuBar()
    self.menu_bar.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#a0a0a0'))
    self.menu_bar.set_size_request(641+345,33)
    
    
    self.menu_files=gtk.Menu()
    self.menu_files.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_files_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_FILE, accel_group=None)
    self.menu_files_root.set_always_show_image(True)
    self.menu_files_root.set_label("Files")
    
    self.menu_files_load_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_OPEN, accel_group=None)
    self.menu_files_load_image.set_always_show_image(True)
    self.menu_files_load_image.set_label("Load image")
    self.menu_files_load_image.connect("activate",image_settings_file.choose_image)
    self.menu_files_load_image.show()
    
    self.menu_files_save_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_SAVE_AS, accel_group=None)
    self.menu_files_save_image.set_always_show_image(True)
    self.menu_files_save_image.set_label("Save image")
    self.menu_files_save_image.connect("activate",image_settings_file.save_image)
    self.menu_files_save_image.show()
    
    self.menu_files_separator_1=gtk.SeparatorMenuItem()
    self.menu_files_separator_1.show()
    
    self.menu_files_info_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_INFO, accel_group=None)
    self.menu_files_info_image.set_always_show_image(True)
    self.menu_files_info_image.set_label("Display image informations")
    self.menu_files_info_image.connect("activate",process_effect.display_image_informations,False)
    self.menu_files_info_image.show()
    
    self.menu_files_separator_2=gtk.SeparatorMenuItem()
    self.menu_files_separator_2.show()
    
    self.menu_files_blend_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_blend_image.set_always_show_image(True)
    self.menu_files_blend_image.set_label("Blend images interpolating")
    self.menu_files_blend_image.connect("activate",process_effect.files_mergin,False,"blend")
    self.menu_files_blend_image.show()
    
    self.menu_files_composite_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_composite_image.set_always_show_image(True)
    self.menu_files_composite_image.set_label("Composite images interpolating")
    self.menu_files_composite_image.connect("activate",process_effect.files_mergin,False,"composite")
    self.menu_files_composite_image.show()
    
    self.menu_files_screen_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_screen_image.set_always_show_image(True)
    self.menu_files_screen_image.set_label("Screen images interpolating")
    self.menu_files_screen_image.connect("activate",process_effect.files_mergin,False,"screen")
    self.menu_files_screen_image.show()
    
    self.menu_files_separator_3=gtk.SeparatorMenuItem()
    self.menu_files_separator_3.show()
    
    self.menu_files_darker_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_darker_image.set_always_show_image(True)
    self.menu_files_darker_image.set_label("Darker images interpolating")
    self.menu_files_darker_image.connect("activate",process_effect.files_mergin,False,"darker")
    self.menu_files_darker_image.show()
    
    self.menu_files_lighter_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_lighter_image.set_always_show_image(True)
    self.menu_files_lighter_image.set_label("Lighter images interpolating")
    self.menu_files_lighter_image.connect("activate",process_effect.files_mergin,False,"lighter")
    self.menu_files_lighter_image.show()
    
    self.menu_files_difference_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_difference_image.set_always_show_image(True)
    self.menu_files_difference_image.set_label("Difference images interpolating")
    self.menu_files_difference_image.connect("activate",process_effect.files_mergin,False,"difference")
    self.menu_files_difference_image.show()
    
    self.menu_files_multiply_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_multiply_image.set_always_show_image(True)
    self.menu_files_multiply_image.set_label("Multiply images interpolating")
    self.menu_files_multiply_image.connect("activate",process_effect.files_mergin,False,"multiply")
    self.menu_files_multiply_image.show()
    
    self.menu_files_add_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_add_image.set_always_show_image(True)
    self.menu_files_add_image.set_label("Add images interpolating")
    self.menu_files_add_image.connect("activate",process_effect.files_mergin,False,"add")
    self.menu_files_add_image.show()
    
    self.menu_files_substract_image=gtk.ImageMenuItem(stock_id=gtk.STOCK_DND_MULTIPLE, accel_group=None)
    self.menu_files_substract_image.set_always_show_image(True)
    self.menu_files_substract_image.set_label("Substract images interpolating")
    self.menu_files_substract_image.connect("activate",process_effect.files_mergin,False,"substract")
    self.menu_files_substract_image.show()
    
    #process_effect.files_mergin
    
    
    
    self.menu_files.append(self.menu_files_load_image)
    self.menu_files.append(self.menu_files_save_image)
    self.menu_files.append(self.menu_files_separator_1)
    self.menu_files.append(self.menu_files_info_image)
    self.menu_files.append(self.menu_files_separator_2)
    self.menu_files.append(self.menu_files_blend_image)
    self.menu_files.append(self.menu_files_composite_image)
    self.menu_files.append(self.menu_files_screen_image)  
    self.menu_files.append(self.menu_files_separator_3)
    self.menu_files.append(self.menu_files_darker_image)
    self.menu_files.append(self.menu_files_lighter_image)
    self.menu_files.append(self.menu_files_difference_image)  
    self.menu_files.append(self.menu_files_multiply_image) 
    self.menu_files.append(self.menu_files_add_image)  
    self.menu_files.append(self.menu_files_substract_image) 
    
    self.menu_files_root.set_submenu(self.menu_files)
    self.menu_files_root.show()
    
    
    self.menu_edition=gtk.Menu()
    self.menu_edition.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_edition_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_EDIT, accel_group=None)
    self.menu_edition_root.set_always_show_image(True)
    self.menu_edition_root.set_label("Edition")
    
    
    self.menu_edition_undo=gtk.ImageMenuItem(stock_id=gtk.STOCK_GOTO_LAST, accel_group=None)
    self.menu_edition_undo.set_always_show_image(True)
    self.menu_edition_undo.set_label("Undo")
    self.menu_edition_undo.connect("activate",process_effect.undo)
    self.menu_edition_undo.show()
    
    self.menu_edition_redo=gtk.ImageMenuItem(stock_id=gtk.STOCK_GOTO_FIRST, accel_group=None)
    self.menu_edition_redo.set_always_show_image(True)
    self.menu_edition_redo.set_label("Redo")
    self.menu_edition_redo.connect("activate",process_effect.redo)
    self.menu_edition_redo.show()
    
    self.menu_edition_separator_1=gtk.SeparatorMenuItem()
    self.menu_edition_separator_1.show()
    
    self.menu_edition_rotate_left=gtk.ImageMenuItem(stock_id=gtk.STOCK_UNDO, accel_group=None)
    self.menu_edition_rotate_left.set_always_show_image(True)
    self.menu_edition_rotate_left.set_label("Rotate image to left")
    self.menu_edition_rotate_left.connect("activate",process_effect.rotate_image,False,"left")
    self.menu_edition_rotate_left.show()
    
    self.menu_edition_rotate_right=gtk.ImageMenuItem(stock_id=gtk.STOCK_REDO, accel_group=None)
    self.menu_edition_rotate_right.set_always_show_image(True)
    self.menu_edition_rotate_right.set_label("Rotate image to right")
    self.menu_edition_rotate_right.connect("activate",process_effect.rotate_image,False,"right")
    self.menu_edition_rotate_right.show()
    
    self.menu_edition_separator_2=gtk.SeparatorMenuItem()
    self.menu_edition_separator_2.show()
    
    self.menu_edition_flip_up_to_down=gtk.ImageMenuItem(stock_id=gtk.STOCK_GO_UP, accel_group=None)
    self.menu_edition_flip_up_to_down.set_always_show_image(True)
    self.menu_edition_flip_up_to_down.set_label("Flip image up")
    self.menu_edition_flip_up_to_down.connect("activate",process_effect.flip_image,False,"flip up")
    self.menu_edition_flip_up_to_down.show()
    
    self.menu_edition_flip_down_to_up=gtk.ImageMenuItem(stock_id=gtk.STOCK_GO_DOWN, accel_group=None)
    self.menu_edition_flip_down_to_up.set_always_show_image(True)
    self.menu_edition_flip_down_to_up.set_label("Flip image down")
    self.menu_edition_flip_down_to_up.connect("activate",process_effect.flip_image,False,"flip down")
    self.menu_edition_flip_down_to_up.show()
    
    self.menu_edition_flip_left_to_right=gtk.ImageMenuItem(stock_id=gtk.STOCK_GO_BACK, accel_group=None)
    self.menu_edition_flip_left_to_right.set_always_show_image(True)
    self.menu_edition_flip_left_to_right.set_label("Flip image left")
    self.menu_edition_flip_left_to_right.connect("activate",process_effect.flip_image,False,"flip left")
    self.menu_edition_flip_left_to_right.show()
    
    self.menu_edition_flip_right_to_left=gtk.ImageMenuItem(stock_id=gtk.STOCK_GO_FORWARD, accel_group=None)
    self.menu_edition_flip_right_to_left.set_always_show_image(True)
    self.menu_edition_flip_right_to_left.set_label("Flip image right")
    self.menu_edition_flip_right_to_left.connect("activate",process_effect.flip_image,False,"flip right")
    self.menu_edition_flip_right_to_left.show()
    
    
    
    
    self.menu_edition.append(self.menu_edition_undo)
    self.menu_edition.append(self.menu_edition_redo)
    self.menu_edition.append(self.menu_edition_separator_1)
    self.menu_edition.append(self.menu_edition_rotate_left)
    self.menu_edition.append(self.menu_edition_rotate_right)
    self.menu_edition.append(self.menu_edition_separator_2)
    self.menu_edition.append(self.menu_edition_flip_up_to_down)
    self.menu_edition.append(self.menu_edition_flip_down_to_up)
    self.menu_edition.append(self.menu_edition_flip_left_to_right)
    self.menu_edition.append(self.menu_edition_flip_right_to_left)
    
    
    
    self.menu_edition_root.set_submenu(self.menu_edition)
    self.menu_edition_root.show()
    
    
    self.menu_effects=gtk.Menu()
    self.menu_effects.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_effects_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_PREFERENCES, accel_group=None)
    self.menu_effects_root.set_always_show_image(True)
    self.menu_effects_root.set_label("Effects")
    
    self.menu_effects_grayscale=gtk.ImageMenuItem(stock_id=gtk.STOCK_INDEX, accel_group=None)
    self.menu_effects_grayscale.set_always_show_image(True)
    self.menu_effects_grayscale.set_label("Apply grayscale")
    #self.menu_edition_flip_up_to_down.connect("activate",)
    
    self.menu_grayscale=gtk.Menu()
    self.menu_grayscale.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_grayscale_average=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_average.set_always_show_image(True)
    self.menu_grayscale_average.set_label('From average pixel value')
    self.menu_grayscale_average.connect("activate",process_effect.set_grayscale,False,"grayscale average")
    self.menu_grayscale_average.show()
    
    self.menu_grayscale_minimum=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_minimum.set_always_show_image(True)
    self.menu_grayscale_minimum.set_label('From minimal pixel value')
    self.menu_grayscale_minimum.connect("activate",process_effect.set_grayscale,False,"grayscale minimum")
    self.menu_grayscale_minimum.show()
    
    self.menu_grayscale_maximum=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_maximum.set_always_show_image(True)
    self.menu_grayscale_maximum.set_label('From maximal pixel value')
    self.menu_grayscale_maximum.connect("activate",process_effect.set_grayscale,False,"grayscale maximum")
    self.menu_grayscale_maximum.show()
    
    self.menu_grayscale_red_value=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_red_value.set_always_show_image(True)
    self.menu_grayscale_red_value.set_label('From red pixel value')
    self.menu_grayscale_red_value.connect("activate",process_effect.set_grayscale,False,"grayscale red")
    self.menu_grayscale_red_value.show()
    
    self.menu_grayscale_green_value=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_green_value.set_always_show_image(True)
    self.menu_grayscale_green_value.set_label('From green pixel value')
    self.menu_grayscale_green_value.connect("activate",process_effect.set_grayscale,False,"grayscale green")
    self.menu_grayscale_green_value.show()
    
    self.menu_grayscale_blue_value=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_grayscale_blue_value.set_always_show_image(True)
    self.menu_grayscale_blue_value.set_label('From blue pixel value')
    self.menu_grayscale_blue_value.connect("activate",process_effect.set_grayscale,False,"grayscale blue")
    self.menu_grayscale_blue_value.show()
    
    self.menu_grayscale.append(self.menu_grayscale_average)
    self.menu_grayscale.append(self.menu_grayscale_minimum)
    self.menu_grayscale.append(self.menu_grayscale_maximum)
    self.menu_grayscale.append(self.menu_grayscale_red_value)
    self.menu_grayscale.append(self.menu_grayscale_green_value)
    self.menu_grayscale.append(self.menu_grayscale_blue_value)
    
    self.menu_grayscale.show()
    
    self.menu_effects_grayscale.set_submenu(self.menu_grayscale)
    self.menu_effects_grayscale.show()
    
    self.menu_effects_separator_1=gtk.SeparatorMenuItem()
    self.menu_effects_separator_1.show()
    
    self.menu_effects_separator_2=gtk.SeparatorMenuItem()
    self.menu_effects_separator_2.show()
    
    self.menu_effects_filters=gtk.ImageMenuItem(stock_id=gtk.STOCK_EXECUTE)
    self.menu_effects_filters.set_always_show_image(True)
    self.menu_effects_filters.set_label("Apply filters")
    

    self.menu_filters=gtk.Menu()
    self.menu_filters.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_filters_blur=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_blur.set_always_show_image(True)
    self.menu_filters_blur.set_label('Blur')
    self.menu_filters_blur.connect("activate",process_effect.apply_filter,False,0)
    self.menu_filters_blur.show()

    self.menu_filters_contour=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_contour.set_always_show_image(True)
    self.menu_filters_contour.set_label('Contour')
    self.menu_filters_contour.connect("activate",process_effect.apply_filter,False,1)
    self.menu_filters_contour.show()


    self.menu_filters_detail=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_detail.set_always_show_image(True)
    self.menu_filters_detail.set_label('Detail')
    self.menu_filters_detail.connect("activate",process_effect.apply_filter,False,2)
    self.menu_filters_detail.show()

    self.menu_filters_edges_enhance=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_edges_enhance.set_always_show_image(True)
    self.menu_filters_edges_enhance.set_label('Edge enhance')
    self.menu_filters_edges_enhance.connect("activate",process_effect.apply_filter,False,3)
    self.menu_filters_edges_enhance.show()

    self.menu_filters_edges_enhance_more=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_edges_enhance_more.set_always_show_image(True)
    self.menu_filters_edges_enhance_more.set_label('Edge enhance more')
    self.menu_filters_edges_enhance_more.connect("activate",process_effect.apply_filter,False,4)
    self.menu_filters_edges_enhance_more.show()

    self.menu_filters_emboss=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_emboss.set_always_show_image(True)
    self.menu_filters_emboss.set_label('Emboss')
    self.menu_filters_emboss.connect("activate",process_effect.apply_filter,False,5)
    self.menu_filters_emboss.show()

    self.menu_filters_find_edges=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_find_edges.set_always_show_image(True)
    self.menu_filters_find_edges.set_label('Find edges')
    self.menu_filters_find_edges.connect("activate",process_effect.apply_filter,False,6)
    self.menu_filters_find_edges.show()

    self.menu_filters_sharpen=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_sharpen.set_always_show_image(True)
    self.menu_filters_sharpen.set_label('Sharpen')
    self.menu_filters_sharpen.connect("activate",process_effect.apply_filter,False,7)
    self.menu_filters_sharpen.show()

    self.menu_filters_smooth=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_smooth.set_always_show_image(True)
    self.menu_filters_smooth.set_label('Smooth')
    self.menu_filters_smooth.connect("activate",process_effect.apply_filter,False,8)
    self.menu_filters_smooth.show()

    self.menu_filters_smooth_more=gtk.ImageMenuItem(stock_id=gtk.STOCK_APPLY)
    self.menu_filters_smooth_more.set_always_show_image(True)
    self.menu_filters_smooth_more.set_label('Smooth more')
    self.menu_filters_smooth_more.connect("activate",process_effect.apply_filter,False,9)
    self.menu_filters_smooth_more.show()

    self.menu_filters.append(self.menu_filters_blur)
    self.menu_filters.append(self.menu_filters_contour)
    self.menu_filters.append(self.menu_filters_detail)
    self.menu_filters.append(self.menu_filters_edges_enhance)
    self.menu_filters.append(self.menu_filters_edges_enhance_more)
    self.menu_filters.append(self.menu_filters_emboss)
    self.menu_filters.append(self.menu_filters_find_edges)
    self.menu_filters.append(self.menu_filters_sharpen)
    self.menu_filters.append(self.menu_filters_smooth)
    self.menu_filters.append(self.menu_filters_smooth_more)
    
    self.menu_filters.show()
    
    self.menu_effects_filters.set_submenu(self.menu_filters)
    self.menu_effects_filters.show()
    
    self.menu_effects_adjustments=gtk.ImageMenuItem(stock_id=gtk.STOCK_CONVERT)
    self.menu_effects_adjustments.set_always_show_image(True)
    self.menu_effects_adjustments.set_label("Apply adjustments")
    self.menu_effects_adjustments.connect("activate",self.open_adjustment_editor,False)
    self.menu_effects_adjustments.show()
    
    self.menu_effects.append(self.menu_effects_grayscale)
    self.menu_effects.append(self.menu_effects_separator_1)
    self.menu_effects.append(self.menu_effects_filters)
    self.menu_effects.append(self.menu_effects_separator_2)
    self.menu_effects.append(self.menu_effects_adjustments)
    
    self.menu_effects_root.set_submenu(self.menu_effects)
    
    self.menu_effects_root.show()
    
    self.menu_effects_separator_2=gtk.SeparatorMenuItem()
    self.menu_effects_separator_2.show()
    
    self.menu_colors=gtk.Menu()
    self.menu_colors.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))

    self.menu_colors_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_SELECT_COLOR, accel_group=None)
    self.menu_colors_root.set_always_show_image(True)
    self.menu_colors_root.set_label("Colors tools")
    
    self.menu_colors_scaling_editor=gtk.ImageMenuItem(stock_id=gtk.STOCK_FIND_AND_REPLACE, accel_group=None)
    self.menu_colors_scaling_editor.set_always_show_image(True)
    self.menu_colors_scaling_editor.set_label("Open colors scaling matrix editor")
    self.menu_colors_scaling_editor.connect("activate",process_effect.set_colors_percent_matrix,False)
    self.menu_colors_scaling_editor.set_tooltip_text("Open the colors scaling matrix editor\nwhich what you can set the value of the colors\nin realtionship to the others colors values. To create colors mix effects.")
    self.menu_colors_scaling_editor.show()
    
    self.menu_effects_separator_3=gtk.SeparatorMenuItem()
    self.menu_effects_separator_3.show()
    
    self.menu_colors_red_scaling_editor=gtk.ImageMenuItem(stock_id=gtk.STOCK_FIND_AND_REPLACE, accel_group=None)
    self.menu_colors_red_scaling_editor.set_always_show_image(True)
    self.menu_colors_red_scaling_editor.set_label("Open redscale editor")
    self.menu_colors_red_scaling_editor.connect("activate",self.open_scaling_editor,"redscale")
    self.menu_colors_red_scaling_editor.set_tooltip_text("Open the redcaleeditor\nwhich what you can apply an red color filter to set the image in redscale.")
    self.menu_colors_red_scaling_editor.show()
    
    self.menu_colors_green_scaling_editor=gtk.ImageMenuItem(stock_id=gtk.STOCK_FIND_AND_REPLACE, accel_group=None)
    self.menu_colors_green_scaling_editor.set_always_show_image(True)
    self.menu_colors_green_scaling_editor.set_label("Open greenscale editor")
    self.menu_colors_green_scaling_editor.connect("activate",self.open_scaling_editor,"greenscale")
    self.menu_colors_green_scaling_editor.set_tooltip_text("Open the greencaleeditor\nwhich what you can apply an green color filter to set the image in greenscale.")
    self.menu_colors_green_scaling_editor.show()
   
    self.menu_colors_blue_scaling_editor=gtk.ImageMenuItem(stock_id=gtk.STOCK_FIND_AND_REPLACE, accel_group=None)
    self.menu_colors_blue_scaling_editor.set_always_show_image(True)
    self.menu_colors_blue_scaling_editor.set_label("Open bluescale editor")
    self.menu_colors_blue_scaling_editor.connect("activate",self.open_scaling_editor,"bluescale")
    self.menu_colors_blue_scaling_editor.set_tooltip_text("Open the bluecale editor\nwhich what you can apply an blue color filter to set the image in bluescale.")
    self.menu_colors_blue_scaling_editor.show()
 
    self.menu_colors.append(self.menu_colors_scaling_editor)
    self.menu_colors.append(self.menu_colors_red_scaling_editor)
    self.menu_colors.append(self.menu_colors_green_scaling_editor)
    self.menu_colors.append(self.menu_colors_blue_scaling_editor)
    
    
    self.menu_colors_root.set_submenu(self.menu_colors)
    
    self.menu_colors_root.show()
    
    self.menu_settings_main=gtk.Menu()
    self.menu_settings_main.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_settings_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_NETWORK, accel_group=None)
    self.menu_settings_root.set_always_show_image(True)
    self.menu_settings_root.set_label("Settings")
    
    
    self.menu_settings_main_speed=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_NEXT)
    self.menu_settings_main_speed.set_always_show_image(True)
    self.menu_settings_main_speed.set_label("execution speed")
    
    self.menu_settings_execution_speed=gtk.Menu()
    self.menu_settings_execution_speed.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_settings_main_speed_10=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_10.set_always_show_image(True)
    self.menu_settings_main_speed_10.set_label("   10 % ")
    self.menu_settings_main_speed_10.connect("activate",self.change_execution_speed,"10")
    self.menu_settings_main_speed_10.set_tooltip_text("Set the computing speed on 10 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_10.show()
    
    self.menu_settings_main_speed_20=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_20.set_always_show_image(True)
    self.menu_settings_main_speed_20.set_label("   20 % ")
    self.menu_settings_main_speed_20.connect("activate",self.change_execution_speed,"20")
    self.menu_settings_main_speed_20.set_tooltip_text("Set the computing speed on 20 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_20.show()
    
    self.menu_settings_main_speed_30=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_30.set_always_show_image(True)
    self.menu_settings_main_speed_30.set_label("   30 % ")
    self.menu_settings_main_speed_30.connect("activate",self.change_execution_speed,"30")
    self.menu_settings_main_speed_30.set_tooltip_text("Set the computing speed on 30 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_30.show()
    
    self.menu_settings_main_speed_40=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_40.set_always_show_image(True)
    self.menu_settings_main_speed_40.set_label("   40 % ")
    self.menu_settings_main_speed_40.connect("activate",self.change_execution_speed,"40")
    self.menu_settings_main_speed_40.set_tooltip_text("Set the computing speed on 40 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_40.show()
    
    self.menu_settings_main_speed_50=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_RECORD)
    self.menu_settings_main_speed_50.set_always_show_image(True)
    self.menu_settings_main_speed_50.set_label("   50 % ")
    self.menu_settings_main_speed_50.connect("activate",self.change_execution_speed,"50")
    self.menu_settings_main_speed_50.set_tooltip_text("Set the computing speed on 50 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_50.show()
    
    self.menu_settings_main_speed_60=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_60.set_always_show_image(True)
    self.menu_settings_main_speed_60.set_label("   60 % ")
    self.menu_settings_main_speed_60.connect("activate",self.change_execution_speed,"60")
    self.menu_settings_main_speed_60.set_tooltip_text("Set the computing speed on 60 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_60.show()
    
    self.menu_settings_main_speed_70=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_70.set_always_show_image(True)
    self.menu_settings_main_speed_70.set_label("   70 % ")
    self.menu_settings_main_speed_70.connect("activate",self.change_execution_speed,"70")
    self.menu_settings_main_speed_70.set_tooltip_text("Set the computing speed on 70 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_70.show()
    
    self.menu_settings_main_speed_80=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_80.set_always_show_image(True)
    self.menu_settings_main_speed_80.set_label("   80 % ")
    self.menu_settings_main_speed_80.connect("activate",self.change_execution_speed,"80")
    self.menu_settings_main_speed_80.set_tooltip_text("Set the computing speed on 80 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_80.show()
    
    self.menu_settings_main_speed_90=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_90.set_always_show_image(True)
    self.menu_settings_main_speed_90.set_label("   90 % ")
    self.menu_settings_main_speed_90.connect("activate",self.change_execution_speed,"90")
    self.menu_settings_main_speed_90.set_tooltip_text("Set the computing speed on 90 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_90.show()
    
    self.menu_settings_main_speed_100=gtk.ImageMenuItem(stock_id=gtk.STOCK_MEDIA_PLAY)
    self.menu_settings_main_speed_100.set_always_show_image(True)
    self.menu_settings_main_speed_100.set_label("  100 % ")
    self.menu_settings_main_speed_100.connect("activate",self.change_execution_speed,"100")
    self.menu_settings_main_speed_100.set_tooltip_text("Set the computing speed on 100 units per millisecond for buffered pixels computing operations.\nTo set depending on your computer capacities.")
    self.menu_settings_main_speed_100.show()
    
    
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_10)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_20)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_30)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_40)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_50)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_60)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_70)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_80)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_90)
    self.menu_settings_execution_speed.append(self.menu_settings_main_speed_100)
    self.menu_settings_execution_speed.show()
    
    self.menu_about_main=gtk.Menu()
    self.menu_about_main.modify_bg(gtk.STATE_NORMAL,self.main_window.get_colormap().alloc_color('#e5e5e5'))
    
    self.menu_about_root=gtk.ImageMenuItem(stock_id=gtk.STOCK_INFO, accel_group=None)
    self.menu_about_root.set_always_show_image(True)
    self.menu_about_root.set_label("About")
    
    self.menu_about_about_item=gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT)
    self.menu_about_about_item.set_always_show_image(True)
    self.menu_about_about_item.set_label("About PyImaging")
    self.menu_about_about_item.connect("activate",self.about_dialog,False)
    self.menu_about_about_item.set_tooltip_text("Display informations about the programm PyImaging.")
    self.menu_about_about_item.show()
    
    self.menu_about_main.append(self.menu_about_about_item)
    self.menu_about_main.show()
    
    self.menu_about_root.set_submenu(self.menu_about_main)
    self.menu_about_root.show()
    
    self.menu_settings_main_speed.set_submenu(self.menu_settings_execution_speed)
    self.menu_settings_main_speed.show()
    
    self.menu_settings_main.append(self.menu_settings_main_speed)
    self.menu_settings_main.show()
    
    self.menu_settings_root.set_submenu(self.menu_settings_main)
    self.menu_settings_root.show()
    
    
    self.menu_bar.append(self.menu_files_root)
    self.menu_bar.append(self.menu_edition_root)
    self.menu_bar.append(self.menu_effects_root)
    self.menu_bar.append(self.menu_colors_root)
    self.menu_bar.append(self.menu_settings_root)
    self.menu_bar.append(self.menu_about_root)
    self.menu_bar.show()
  
  def config_button_box_bottom(self) :
    
    self.button_label_rotate=gtk.Button()
    self.button_label_rotate_label=gtk.Label("Rotate")
    self.button_label_rotate_label.show()
    self.button_label_rotate_image=gtk.image_new_from_stock(gtk.STOCK_REFRESH,4)
    self.button_label_rotate_image.show()
    self.button_label_rotate_hbox=gtk.HBox()
    self.button_label_rotate_hbox.pack_start(self.button_label_rotate_image,False,False,0)
    self.button_label_rotate_hbox.pack_start(self.button_label_rotate_label,False,False,0)
    self.button_label_rotate_hbox.show()
    self.button_label_rotate.add(self.button_label_rotate_hbox)
    self.button_label_rotate.set_size_request(int((641+345)/14.0),24)
    #self.button_label_rotate.set_image(self.button_label_rotate_image)
    self.button_label_rotate.set_focus_on_click(False)
    self.button_label_rotate.show() 
    
    self.button_rotate_left = gtk.Button(None)
    self.button_rotate_left.set_name("rotate left")
    self.image_rotate_left  = gtk.image_new_from_stock(gtk.STOCK_UNDO,4)
    self.image_rotate_left.show()
    self.button_rotate_left.set_image(self.image_rotate_left)
    self.button_rotate_left.set_focus_on_click(True)
    self.button_rotate_left.set_size_request(24+12,24)
    self.button_rotate_left.connect("button-press-event",process_effect.rotate_image)
    self.button_rotate_left.show()
    
    self.button_rotate_right = gtk.Button(None)
    self.button_rotate_right.set_name("rotate right")
    self.image_rotate_right  = gtk.image_new_from_stock(gtk.STOCK_REDO,4)
    self.image_rotate_right.show()
    self.button_rotate_right.set_image(self.image_rotate_right)
    self.button_rotate_right.set_focus_on_click(True)
    self.button_rotate_right.set_size_request(24+12,24)
    self.button_rotate_right.connect("button-press-event",process_effect.rotate_image)
    self.button_rotate_right.show()
    
    self.button_label_mirror=gtk.Button()
    self.button_label_mirror_label=gtk.Label("Mirror")
    self.button_label_mirror_label.show()
    self.button_label_mirror_image=gtk.image_new_from_stock(gtk.STOCK_FULLSCREEN,4)
    self.button_label_mirror_image.show()
    self.button_label_mirror_hbox=gtk.HBox()
    self.button_label_mirror_hbox.pack_start(self.button_label_mirror_image,False,False,0)
    self.button_label_mirror_hbox.pack_start(self.button_label_mirror_label,False,False,0)
    self.button_label_mirror_hbox.show()
    self.button_label_mirror.add(self.button_label_mirror_hbox)
    self.button_label_rotate.set_size_request(int((641+345)/12.0),24)
    #self.button_label_mirror.set_image(self.button_label_mirror_image)
    self.button_label_mirror.set_focus_on_click(False)
    self.button_label_mirror.show() 
    
    self.button_mirror_up = gtk.Button(None)
    self.button_mirror_up.set_name("flip up")
    self.image_mirror_up  = gtk.image_new_from_stock(gtk.STOCK_GO_UP,4)
    self.image_mirror_up.show()
    self.button_mirror_up.set_image(self.image_mirror_up)
    self.button_mirror_up.set_focus_on_click(True)
    self.button_mirror_up.set_size_request(24+12,24)
    self.button_mirror_up.connect("button-press-event",process_effect.flip_image)
    self.button_mirror_up.show() 
    
    self.button_mirror_down = gtk.Button(None)
    self.button_mirror_down.set_name("flip down")
    self.image_mirror_down  = gtk.image_new_from_stock(gtk.STOCK_GO_DOWN,4)
    self.image_mirror_down.show()
    self.button_mirror_down.set_image(self.image_mirror_down)
    self.button_mirror_down.set_focus_on_click(True)
    self.button_mirror_down.set_size_request(24+12,24)
    self.button_mirror_down.connect("button-press-event",process_effect.flip_image)
    self.button_mirror_down.show()
    
    
    
    self.button_mirror_left = gtk.Button(None)
    self.button_mirror_left.set_name("flip left")
    self.image_mirror_left  = gtk.image_new_from_stock(gtk.STOCK_GO_BACK,4)
    self.image_mirror_left.show()
    self.button_mirror_left.set_image(self.image_mirror_left)
    self.button_mirror_left.set_focus_on_click(True)
    self.button_mirror_left.set_size_request(24+12,24)
    self.button_mirror_left.connect("button-press-event",process_effect.flip_image)
    self.button_mirror_left.show() 
    
    self.button_mirror_right = gtk.Button(None)
    self.button_mirror_right.set_name("flip right")
    self.image_mirror_right  = gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD,4)
    self.image_mirror_right.show()
    self.button_mirror_right.set_image(self.image_mirror_right)
    self.button_mirror_right.set_focus_on_click(True)
    self.button_mirror_right.set_size_request(24+12,24)
    self.button_mirror_right.connect("button-press-event",process_effect.flip_image)
    self.button_mirror_right.show()
        
    
    self.button_grayscale=gtk.Button()
    self.button_grayscale_label=gtk.Label(" Grayscale")
    self.button_grayscale_label.show()
    self.button_grayscale_image=gtk.image_new_from_stock(gtk.STOCK_INDEX,4)
    self.button_grayscale_image.show()
    self.button_grayscale_hbox=gtk.HBox()
    self.button_grayscale_hbox.pack_start(self.button_grayscale_image,False,False,0)
    self.button_grayscale_hbox.pack_start(self.button_grayscale_label,False,False,0)
    self.button_grayscale_hbox.show()
    #self.button_grayscale.set_image(self.button_grayscale_image)
    self.button_grayscale.add(self.button_grayscale_hbox)
    self.button_grayscale.set_focus_on_click(True)
    self.button_grayscale.set_size_request(int((641+345)/9.65), 24)
    self.button_grayscale.connect("button-press-event",process_effect.set_grayscale)
    self.button_grayscale.show()
    
    self.combo_set_grayscale=gtk.combo_box_new_text()
    self.combo_set_grayscale.set_size_request((641+345)/9+8,32)
    self.combo_set_grayscale.set_tooltip_text("Select base the pixel value for gray values")
    for idx,v in [(0,"average"),(1,"minimum"),(2,"maximum"),(3,"red"),(4,"green"),(5,"blue")] :
      self.combo_set_grayscale.insert_text(idx, v)
    self.combo_set_grayscale.show()
    self.combo_set_grayscale.set_active(0)
    
    self.button_filters=gtk.Button()
    self.button_filters_label=gtk.Label("Set filter")
    self.button_filters_label.show()
    self.button_filters_image=gtk.image_new_from_stock(gtk.STOCK_PROPERTIES,4)
    self.button_filters_image.show()
    self.button_filters_hbox=gtk.HBox()
    self.button_filters_hbox.pack_start(self.button_filters_image,False,False,0)
    self.button_filters_hbox.pack_start(self.button_filters_label,False,False,0)
    self.button_filters_hbox.show()
    self.button_filters.add(self.button_filters_hbox)
    self.button_filters.set_size_request(int((641+345)/10.30), 24)
    #self.button_filters.set_image(self.button_filters_image)
    self.button_filters.connect("button-press-event",process_effect.apply_filter)
    self.button_filters.show()
    
    self.combo_set_filters=gtk.combo_box_new_text()
    self.combo_set_filters.set_size_request(int((641+345)/6.35),32)
    self.combo_set_filters.set_tooltip_text("Select filter to apply")
    for idx,v in [(0,"Blur"),(1,"Contour"),(2,"Detail"),(3,"Edge enhance"),(4,"Edge enhance more"),(5,"Emboss"),(6,"Find edges"),(7,"Sharpen"),(8,"Smooth"),(9,"Smooth more")] :
      self.combo_set_filters.insert_text(idx, v)
    self.combo_set_filters.set_title("Choose a filter.")
    self.combo_set_filters.show()
    self.combo_set_filters.set_active(0)
    
    
    self.button_mult_matrix=gtk.Button()
    self.button_mult_matrix_image=gtk.image_new_from_stock(gtk.STOCK_EXECUTE,4)
    self.button_mult_matrix_image.show()
    self.button_mult_matrix_hbox=gtk.HBox()
    self.button_mult_matrix_hbox.pack_start(self.button_mult_matrix_image,False,False,0)
    self.button_mult_matrix_hbox.show()
    self.button_mult_matrix.add(self.button_mult_matrix_hbox)
    self.button_mult_matrix.set_size_request(24+12, 24)
    #self.button_mult_matrix.set_image(self.button_mult_matrix_image)
    self.button_mult_matrix.connect("button-press-event",process_effect.set_colors_percent_matrix)
    self.button_mult_matrix.show()
    
    self.buttonbox_bottom.append_space()
    self.buttonbox_bottom.append_widget(self.button_label_rotate,tooltip_text="", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_rotate_left, tooltip_text="Rotate image 90° to the left.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_rotate_right, tooltip_text="Rotate image 90° to the right.", tooltip_private_text="")
    self.buttonbox_bottom.append_space()
    self.buttonbox_bottom.append_widget(self.button_label_mirror, tooltip_text="", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_mirror_up, tooltip_text="Flip image up.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_mirror_down, tooltip_text="Flip image down.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_mirror_left, tooltip_text="Flip image left.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.button_mirror_right, tooltip_text="Flip image right.", tooltip_private_text="")
    self.buttonbox_bottom.append_space()
    self.buttonbox_bottom.append_widget(self.button_grayscale, tooltip_text="Apply grayscale to image with the current selected pixel value base.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.combo_set_grayscale, tooltip_text="Select the pixel value as base for grayscale computing.", tooltip_private_text="")
    self.buttonbox_bottom.append_space()
    self.buttonbox_bottom.append_widget(self.button_filters, tooltip_text="Apply the current selected filter to the image.", tooltip_private_text="")
    self.buttonbox_bottom.append_widget(self.combo_set_filters, tooltip_text="Select a filter to apply to the image.", tooltip_private_text="")
    self.buttonbox_bottom.append_space()
    self.buttonbox_bottom.append_widget(self.button_mult_matrix, tooltip_text="Open the colors scaling matrix editor\nwhich what you can set the value of the colors\nin realtionship to the others colors values. To create colors mix effects.", tooltip_private_text="")
    self.buttonbox_bottom.append_space()
    
    
    
  def config_button_box_top(self) :
    
    
    
    self.button_undo=gtk.Button()
    self.button_undo_label=gtk.Label("Undo")
    self.button_undo_label.show()
    self.button_undo_image=gtk.image_new_from_stock(gtk.STOCK_GOTO_LAST, 4)
    self.button_undo_image.show()
    self.button_undo_hbox=gtk.HBox()
    self.button_undo_hbox.pack_start(self.button_undo_image,False,False,0)
    self.button_undo_hbox.pack_start(self.button_undo_label,False,False,0)
    self.button_undo_hbox.show()
    self.button_undo.add(self.button_undo_hbox)
    #self.button_undo.set_image(self.button_undo_image)
    self.button_undo.connect("button-press-event",process_effect.undo)
    self.button_undo.set_size_request( int((641+345)/14.0),24)
    self.button_undo.show()
    
    self.button_redo=gtk.Button()
    self.button_redo_label=gtk.Label("Redo")
    self.button_redo_label.show()
    self.button_redo_image=gtk.image_new_from_stock(gtk.STOCK_GOTO_FIRST, 4)
    self.button_redo_image.show()
    self.button_redo_hbox=gtk.HBox()
    self.button_redo_hbox.pack_start(self.button_redo_image,False,False,0)
    self.button_redo_hbox.pack_start(self.button_redo_label,False,False,0)
    self.button_redo_hbox.show()
    self.button_redo.add(self.button_redo_hbox)
    #self.button_redo.set_image(self.button_redo_image)
    self.button_redo.connect("button-press-event",process_effect.redo)
    self.button_redo.set_size_request(int((641+345)/14.0),24)
    self.button_redo.show()
    
    self.button_open_new_image=gtk.Button()
    self.button_open_new_image_label=gtk.Label("Load image")
    self.button_open_new_image_label.show()
    self.button_open_new_image_image=gtk.image_new_from_stock(gtk.STOCK_OPEN,4)
    self.button_open_new_image_image.show()
    self.button_open_new_image_hbox=gtk.HBox()
    self.button_open_new_image_hbox.pack_start(self.button_open_new_image_image,False,False,0)
    self.button_open_new_image_hbox.pack_start(self.button_open_new_image_label,False,False,0)
    self.button_open_new_image_hbox.show()
    self.button_open_new_image.add(self.button_open_new_image_hbox)
    #self.button_open_new_image.set_image(self.button_open_new_image_image)
    self.button_open_new_image.connect("button-press-event",image_settings_file.choose_image)
    #self.button_open_new_image=gtk.Button(stock=gtk.STOCK_GO_UP)
    self.button_open_new_image.set_size_request(int((641+345)/9.0),24)
    self.button_open_new_image.show()
    
    
    self.button_save_as=gtk.Button()
    self.button_save_as_label=gtk.Label("Save image")
    self.button_save_as_label.show()
    self.button_save_as_image=gtk.image_new_from_stock(gtk.STOCK_SAVE_AS,4)
    self.button_save_as_image.show()
    self.button_save_as_hbox=gtk.HBox()
    self.button_save_as_hbox.pack_start(self.button_save_as_image,False,False,0)
    self.button_save_as_hbox.pack_start(self.button_save_as_label,False,False,0)
    self.button_save_as_hbox.show()
    self.button_save_as.add(self.button_save_as_hbox)
    #self.button_save_as.set_image(self.button_save_as_image)
    self.button_save_as.connect("button-press-event",image_settings_file.save_image)
    self.button_save_as.set_size_request(int((641+345)/9.0),24)
    self.button_save_as.show()
    
    self.button_info_image=gtk.Button()
    self.button_info_image_label=gtk.Label(" Informations about the file  ")
    self.button_info_image_label.show()
    self.button_info_image_image=gtk.image_new_from_stock(gtk.STOCK_INFO,4)
    self.button_info_image_image.show()
    self.button_info_image_hbox=gtk.HBox()
    self.button_info_image_hbox.pack_start(self.button_info_image_image,False,False,0)
    self.button_info_image_hbox.pack_start(self.button_info_image_label,False,False,0)
    self.button_info_image_hbox.show()
    self.button_info_image.add(self.button_info_image_hbox)
    #self.button_info_image.set_image(self.button_info_image_image)
    self.button_info_image.set_size_request(int((641+345)/4.5),24)
    self.button_info_image.connect("button-press-event",process_effect.display_image_informations)
    self.button_info_image.show()
    
    self.button_blend_files=gtk.Button()
    self.button_blend_files_label=gtk.Label("blend")
    self.button_blend_files_label.show()
    self.button_blend_files_image=gtk.image_new_from_stock(gtk.STOCK_DND_MULTIPLE,4)
    self.button_blend_files_image.show()
    self.button_blend_files_hbox=gtk.HBox()
    self.button_blend_files_hbox.pack_start(self.button_blend_files_image,False,False,0)
    self.button_blend_files_hbox.pack_start(self.button_blend_files_label,False,False,0)
    self.button_blend_files_hbox.show()
    self.button_blend_files.add(self.button_blend_files_hbox)
    #self.button_blend_files.set_image(self.button_blend_files_image)
    self.button_blend_files.set_name("blend")
    self.button_blend_files.set_size_request(int((641+345)/14.0),24)
    self.button_blend_files.connect("button-press-event",process_effect.files_mergin)
    self.button_blend_files.show()
    
    self.button_composite_files=gtk.Button()
    self.button_composite_files_label=gtk.Label("composite")
    self.button_composite_files_label.show()
    self.button_composite_files_image=gtk.image_new_from_stock(gtk.STOCK_DND_MULTIPLE,4)
    self.button_composite_files_image.show()
    self.button_composite_files_hbox=gtk.HBox()
    self.button_composite_files_hbox.pack_start(self.button_composite_files_image,False,False,0)
    self.button_composite_files_hbox.pack_start(self.button_composite_files_label,False,False,0)
    self.button_composite_files_hbox.show()
    self.button_composite_files.add(self.button_composite_files_hbox)
    #self.button_composite_files.set_image(self.button_composite_files_image)
    self.button_composite_files.set_name("composite")
    self.button_composite_files.set_size_request(int((641+345)/9.5),24)
    self.button_composite_files.connect("button-press-event",process_effect.files_mergin)
    self.button_composite_files.show()
    
    self.button_screen_files=gtk.Button()
    self.button_screen_files_label=gtk.Label("screen ")
    self.button_screen_files_label.show()
    self.button_screen_files_image=gtk.image_new_from_stock(gtk.STOCK_DND_MULTIPLE,4)
    self.button_screen_files_image.show()
    self.button_screen_files_hbox=gtk.HBox()
    self.button_screen_files_hbox.pack_start(self.button_screen_files_image,False,False,0)
    self.button_screen_files_hbox.pack_start(self.button_screen_files_label,False,False,0)
    self.button_screen_files_hbox.show()
    self.button_screen_files.add(self.button_screen_files_hbox)
    #self.button_screen_files.set_image(self.button_screen_files_image)
    self.button_screen_files.set_name("screen")
    self.button_screen_files.set_size_request(int((641+345)/12.5),24)
    self.button_screen_files.connect("button-press-event",process_effect.files_mergin)
    self.button_screen_files.show()
    
    self.button_about=gtk.Button()
    self.button_about_image=gtk.image_new_from_stock(gtk.STOCK_ABOUT,4)
    self.button_about_image.show()
    self.button_about_hbox=gtk.HBox()
    self.button_about_hbox.pack_start(self.button_about_image,False,False,0)
    self.button_about_hbox.show()
    self.button_about.add(self.button_about_hbox)
    #self.button_about.set_image(self.button_about_image)
    self.button_about.set_size_request(24+12,24)
    self.button_about.connect("button-press-event",self.about_dialog)
    self.button_about.show()
    
    self.buttonbox_top.set_style(gtk.TOOLBAR_TEXT)
    self.buttonbox_top.set_orientation(gtk.ORIENTATION_HORIZONTAL)
    
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_undo, tooltip_text="Undo the last action.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_redo, tooltip_text="Redo the last undo action.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_open_new_image, tooltip_text="Load an image to procssing.", tooltip_private_text="")
    self.buttonbox_top.append_widget(self.button_save_as, tooltip_text="Save current image.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_info_image, tooltip_text="Informations about the current image settings.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_blend_files, tooltip_text="Interpolate 2 images with an alpha value.", tooltip_private_text="")
    self.buttonbox_top.append_widget(self.button_composite_files, tooltip_text="Interpolate 2 images with an third mask image.", tooltip_private_text="")
    self.buttonbox_top.append_widget(self.button_screen_files, tooltip_text="Superimpose two inverted images on the top of each other.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    self.buttonbox_top.append_widget(self.button_about, tooltip_text="Information about the programm.", tooltip_private_text="")
    self.buttonbox_top.append_space()
    
  def config_right_panel(self) :
    
    self.matrix_vbox=gtk.VBox()
    self.matrix_vbox.set_size_request(315,270/2)
    
    self.frame_matrix_filters=gtk.Frame("Color inverter matrix filter")
    self.frame_matrix_filters.set_size_request(315,270/2)
    self.frame_matrix_filters.set_border_width(5)
    
    self.frame_matrix_filters.set_tooltip_text("Color inverter matrix:\nSet one value color representing row on one,\nto configure an color inversion matrix,\nor use the arrows to select an predefine color inversion matrix.")
    
    self.button_table_matrix_filters=gtk.Table(rows=4, columns=4, homogeneous=True)
    self.button_table_matrix_filters.set_size_request(315,270/2)
    self.button_table_matrix_filters.set_border_width(5)
    
    self.button_label_red_container=gtk.EventBox()
    self.button_label_red_container.modify_bg(gtk.STATE_NORMAL,self.button_label_red_container.get_colormap().alloc_color('#ff0000'))
    self.button_label_red_container.modify_bg(gtk.STATE_PRELIGHT,self.button_label_red_container.get_colormap().alloc_color('#ff0000'))
    
    self.button_label_red_label=gtk.Label("R")
    self.button_label_red_label.show()
    
    self.button_label_red_container.add(self.button_label_red_label)
    self.button_label_red_container.show()
    
    self.button_label_red_button=gtk.Button(None)
    self.button_label_red_button.set_size_request(40,40)
    self.button_label_red_button.set_can_focus(False)
    self.button_label_red_button.add(self.button_label_red_container)
    self.button_label_red_button.set_focus_on_click(False)
    self.button_label_red_button.set_tooltip_text("Red color pixel value take the value of red, green or blue pixel value,\nwhich is set to one.")
    self.button_label_red_button.show()
    
    
    self.button_table_matrix_filters.attach(self.button_label_red_button, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    self.button_label_green_container=gtk.EventBox()
    self.button_label_green_container.modify_bg(gtk.STATE_NORMAL,self.button_label_green_container.get_colormap().alloc_color('#00ff00'))
    self.button_label_green_container.modify_bg(gtk.STATE_PRELIGHT,self.button_label_green_container.get_colormap().alloc_color('#00ff00'))
    
    self.button_label_green_label=gtk.Label("G")
    self.button_label_green_label.show()
    
    self.button_label_green_container.add(self.button_label_green_label)
    self.button_label_green_container.show()
    
    self.button_label_green_button=gtk.Button(None)
    self.button_label_green_button.set_size_request(40,40)
    self.button_label_green_button.set_can_focus(False)
    self.button_label_green_button.add(self.button_label_green_container)
    self.button_label_green_button.set_focus_on_click(False)
    self.button_label_green_button.set_tooltip_text("Green color pixel value take the value of red, green or blue pixel value,\nwhich is set to one.")
    self.button_label_green_button.show()
    
    self.button_table_matrix_filters.attach(self.button_label_green_button, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_label_blue_container=gtk.EventBox()
    self.button_label_blue_container.modify_bg(gtk.STATE_NORMAL,self.button_label_blue_container.get_colormap().alloc_color('#0000ff'))
    self.button_label_blue_container.modify_bg(gtk.STATE_PRELIGHT,self.button_label_blue_container.get_colormap().alloc_color('#0000ff'))
    
    self.button_label_blue_label=gtk.Label("B")
    self.button_label_blue_label.show()
    
    self.button_label_blue_container.add(self.button_label_blue_label)
    self.button_label_blue_container.show()
    
    self.button_label_blue_button=gtk.Button(None)
    self.button_label_blue_button.set_size_request(40,40)
    self.button_label_blue_button.set_can_focus(False)
    self.button_label_blue_button.add(self.button_label_blue_container)
    self.button_label_blue_button.set_focus_on_click(False)
    self.button_label_blue_button.set_tooltip_text("Green color pixel value take the value of red, green or blue pixel value,\nwhich is set to one.")
    self.button_label_blue_button.show()
    
    self.button_table_matrix_filters.attach(self.button_label_blue_button, left_attach=0, right_attach=1, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_matrix_red_red_container=gtk.EventBox()
    self.button_matrix_red_red_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_red_red_container.get_colormap().alloc_color('#ff0000'))
    
    self.button_matrix_red_red_label=gtk.Label("1")
    self.button_matrix_red_red_label.show()
    
    self.button_matrix_red_red_container.add(self.button_matrix_red_red_label)
    self.button_matrix_red_red_container.show()
    
    self.button_matrix_red_red_button=gtk.Button(None)
    self.button_matrix_red_red_button.set_size_request(40,40)
    self.button_matrix_red_red_button.add(self.button_matrix_red_red_container)
    self.button_matrix_red_red_button.set_tooltip_text("Set the red pixel value as the red pixel value.")
    self.button_matrix_red_red_button.set_data("value","1")
    self.button_matrix_red_red_button.set_name("red:red")
    self.button_matrix_red_red_button.connect("button-press-event",self.set_color_inverting_matrix_red_value)
    self.button_matrix_red_red_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_red_red_button, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_matrix_red_green_container=gtk.EventBox()
    self.button_matrix_red_green_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_red_green_container.get_colormap().alloc_color('#00ff00'))
    
    self.button_matrix_red_green_label=gtk.Label("0")
    self.button_matrix_red_green_label.show()
    
    self.button_matrix_red_green_container.add(self.button_matrix_red_green_label)
    self.button_matrix_red_green_container.show()
    
    self.button_matrix_red_green_button=gtk.Button(None)
    self.button_matrix_red_green_button.set_size_request(40,40)
    self.button_matrix_red_green_button.add(self.button_matrix_red_green_container)
    self.button_matrix_red_green_button.set_tooltip_text("Set the red pixel value as the green pixel value.")
    self.button_matrix_red_green_button.set_data("value","0")
    self.button_matrix_red_green_button.set_name("red:green")
    self.button_matrix_red_green_button.connect("button-press-event",self.set_color_inverting_matrix_red_value)
    self.button_matrix_red_green_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_red_green_button, left_attach=2, right_attach=3, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    self.button_matrix_red_blue_container=gtk.EventBox()
    self.button_matrix_red_blue_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_red_blue_container.get_colormap().alloc_color('#0000ff'))
    
    self.button_matrix_red_blue_label=gtk.Label("0")
    self.button_matrix_red_blue_label.show()
    
    self.button_matrix_red_blue_container.add(self.button_matrix_red_blue_label)
    self.button_matrix_red_blue_container.show()
    
    self.button_matrix_red_blue_button=gtk.Button(None)
    self.button_matrix_red_blue_button.set_size_request(40,40)
    self.button_matrix_red_blue_button.add(self.button_matrix_red_blue_container)
    self.button_matrix_red_blue_button.set_tooltip_text("Set the red pixel value as the blue pixel value.")
    self.button_matrix_red_blue_button.set_data("value","0")
    self.button_matrix_red_blue_button.set_name("red:blue")
    self.button_matrix_red_blue_button.connect("button-press-event",self.set_color_inverting_matrix_red_value)
    self.button_matrix_red_blue_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_red_blue_button, left_attach=3, right_attach=4, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    self.button_matrix_green_red_container=gtk.EventBox()
    self.button_matrix_green_red_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_green_red_container.get_colormap().alloc_color('#ff0000'))
    
    self.button_matrix_green_red_label=gtk.Label("0")
    self.button_matrix_green_red_label.show()
    
    self.button_matrix_green_red_container.add(self.button_matrix_green_red_label)
    self.button_matrix_green_red_container.show()
    
    self.button_matrix_green_red_button=gtk.Button(None)
    #self.button_matrix_green_red_button.set_size_request(40,40)
    self.button_matrix_green_red_button.add(self.button_matrix_green_red_container)
    self.button_matrix_green_red_button.set_tooltip_text("Set the green pixel value as the red pixel value.")
    self.button_matrix_green_red_button.set_data("value","0")
    self.button_matrix_green_red_button.set_name("green:red")
    self.button_matrix_green_red_button.connect("button-press-event",self.set_color_inverting_matrix_green_value)
    self.button_matrix_green_red_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_green_red_button, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_matrix_green_green_container=gtk.EventBox()
    self.button_matrix_green_green_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_green_green_container.get_colormap().alloc_color('#00ff00'))
    
    self.button_matrix_green_green_label=gtk.Label("1")
    self.button_matrix_green_green_label.show()
    
    self.button_matrix_green_green_container.add(self.button_matrix_green_green_label)
    self.button_matrix_green_green_container.show()
    
    self.button_matrix_green_green_button=gtk.Button(None)
    #self.button_matrix_green_green_button.set_size_request(40,40)
    self.button_matrix_green_green_button.add(self.button_matrix_green_green_container)
    self.button_matrix_green_green_button.set_tooltip_text("Set the green pixel value as the green pixel value.")
    self.button_matrix_green_green_button.set_data("value","1")
    self.button_matrix_green_green_button.set_name("green:green")
    self.button_matrix_green_green_button.connect("button-press-event",self.set_color_inverting_matrix_green_value)
    self.button_matrix_green_green_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_green_green_button, left_attach=2, right_attach=3, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    self.button_matrix_green_blue_container=gtk.EventBox()
    self.button_matrix_green_blue_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_green_blue_container.get_colormap().alloc_color('#0000ff'))
    
    self.button_matrix_green_blue_label=gtk.Label("0")
    self.button_matrix_green_blue_label.show()
    
    self.button_matrix_green_blue_container.add(self.button_matrix_green_blue_label)
    self.button_matrix_green_blue_container.show()
    
    self.button_matrix_green_blue_button=gtk.Button(None)
    #self.button_matrix_green_blue_button.set_size_request(40,40)
    self.button_matrix_green_blue_button.add(self.button_matrix_green_blue_container)
    self.button_matrix_green_blue_button.set_tooltip_text("Set the green pixel value as the blue pixel value.")
    self.button_matrix_green_blue_button.set_data("value","0")
    self.button_matrix_green_blue_button.set_name("green:blue")
    self.button_matrix_green_blue_button.connect("button-press-event",self.set_color_inverting_matrix_green_value)
    self.button_matrix_green_blue_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_green_blue_button, left_attach=3, right_attach=4, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    
    
    self.button_matrix_blue_red_container=gtk.EventBox()
    self.button_matrix_blue_red_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_blue_red_container.get_colormap().alloc_color('#ff0000'))
    
    self.button_matrix_blue_red_label=gtk.Label("0")
    self.button_matrix_blue_red_label.show()
    
    self.button_matrix_blue_red_container.add(self.button_matrix_blue_red_label)
    self.button_matrix_blue_red_container.show()
    
    self.button_matrix_blue_red_button=gtk.Button(None)
    #self.button_matrix_blue_red_button.set_size_request(40,40)
    self.button_matrix_blue_red_button.add(self.button_matrix_blue_red_container)
    self.button_matrix_blue_red_button.set_tooltip_text("Set the blue pixel value as the red pixel value.")
    self.button_matrix_blue_red_button.set_data("value","0")
    self.button_matrix_blue_red_button.set_name("blue:red")
    self.button_matrix_blue_red_button.connect("button-press-event",self.set_color_inverting_matrix_blue_value)
    self.button_matrix_blue_red_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_blue_red_button, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_matrix_blue_green_container=gtk.EventBox()
    self.button_matrix_blue_green_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_blue_green_container.get_colormap().alloc_color('#00ff00'))
    
    self.button_matrix_blue_green_label=gtk.Label("0")
    self.button_matrix_blue_green_label.show()
    
    self.button_matrix_blue_green_container.add(self.button_matrix_blue_green_label)
    self.button_matrix_blue_green_container.show()
    
    self.button_matrix_blue_green_button=gtk.Button(None)
    #self.button_matrix_blue_green_button.set_size_request(40,40)
    self.button_matrix_blue_green_button.add(self.button_matrix_blue_green_container)
    self.button_matrix_blue_green_button.set_tooltip_text("Set the blue pixel value as the green pixel value.")
    self.button_matrix_blue_green_button.set_data("value","0")
    self.button_matrix_blue_green_button.set_name("blue:green")
    self.button_matrix_blue_green_button.connect("button-press-event",self.set_color_inverting_matrix_blue_value)
    self.button_matrix_blue_green_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_blue_green_button, left_attach=2, right_attach=3, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    self.button_matrix_blue_blue_container=gtk.EventBox()
    self.button_matrix_blue_blue_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_blue_blue_container.get_colormap().alloc_color('#0000ff'))
    
    self.button_matrix_blue_blue_label=gtk.Label("1")
    self.button_matrix_blue_blue_label.show()
    
    self.button_matrix_blue_blue_container.add(self.button_matrix_blue_blue_label)
    self.button_matrix_blue_blue_container.show()
    
    self.button_matrix_blue_blue_button=gtk.Button(None)
    #self.button_matrix_blue_blue_button.set_size_request(40,40)
    self.button_matrix_blue_blue_button.add(self.button_matrix_blue_blue_container)
    self.button_matrix_blue_blue_button.set_tooltip_text("Set the blue pixel value as the blue pixel value.")
    self.button_matrix_blue_blue_button.set_data("value","1")
    self.button_matrix_blue_blue_button.set_name("blue:blue")
    self.button_matrix_blue_blue_button.connect("button-press-event",self.set_color_inverting_matrix_blue_value)
    self.button_matrix_blue_blue_button.show()
    
    self.button_table_matrix_filters.attach(self.button_matrix_blue_blue_button, left_attach=3, right_attach=4, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    
    
    
    self.button_change_predefine_color_inverting_matrix_backward_button=gtk.Button(None)
    self.button_change_predefine_color_inverting_matrix_backward_button_image=gtk.image_new_from_stock(gtk.STOCK_GO_BACK, 2)
    self.button_change_predefine_color_inverting_matrix_backward_button.set_image(self.button_change_predefine_color_inverting_matrix_backward_button_image)
    self.button_change_predefine_color_inverting_matrix_backward_button.connect("button-press-event",self.change_predefine_color_inverting_matrix_backward)
    self.button_change_predefine_color_inverting_matrix_backward_button.show()
    
    self.button_table_matrix_filters.attach(self.button_change_predefine_color_inverting_matrix_backward_button, left_attach=0, right_attach=1, top_attach=3, bottom_attach=4, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
      
    self.button_change_predefine_color_inverting_matrix_apply_button=gtk.Button()
    self.button_change_predefine_color_inverting_matrix_apply_button_label=gtk.Label("  Compute")
    self.button_change_predefine_color_inverting_matrix_apply_button_label.show()
    self.button_change_predefine_color_inverting_matrix_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_EXECUTE,2)
    self.button_change_predefine_color_inverting_matrix_apply_button_image.show()
    self.button_change_predefine_color_inverting_matrix_apply_button_hbox=gtk.HBox()
    self.button_change_predefine_color_inverting_matrix_apply_button_hbox.pack_start(self.button_change_predefine_color_inverting_matrix_apply_button_image,False,False,0)
    self.button_change_predefine_color_inverting_matrix_apply_button_hbox.pack_start(self.button_change_predefine_color_inverting_matrix_apply_button_label,False,False,0)
    self.button_change_predefine_color_inverting_matrix_apply_button_hbox.show()
    self.button_change_predefine_color_inverting_matrix_apply_button.add(self.button_change_predefine_color_inverting_matrix_apply_button_hbox)
    #self.button_change_predefine_color_inverting_matrix_apply_button.set_image(self.button_change_predefine_color_inverting_matrix_apply_button_image)
    self.button_change_predefine_color_inverting_matrix_apply_button.set_tooltip_text("Compute the color inverting matrix with every pixel from the image.")
    self.button_change_predefine_color_inverting_matrix_apply_button.connect("button-press-event",process_effect.set_colors_inverting_matrix)
    self.button_change_predefine_color_inverting_matrix_apply_button.show()
    
    self.button_table_matrix_filters.attach(self.button_change_predefine_color_inverting_matrix_apply_button, left_attach=1, right_attach=3, top_attach=3, bottom_attach=4, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    
    
    self.button_change_predefine_color_inverting_matrix_forward_button=gtk.Button(None)
    self.button_change_predefine_color_inverting_matrix_forward_button_image=gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD, 2)
    self.button_change_predefine_color_inverting_matrix_forward_button.set_image(self.button_change_predefine_color_inverting_matrix_forward_button_image)
    self.button_change_predefine_color_inverting_matrix_forward_button.connect("button-press-event",self.change_predefine_color_inverting_matrix_forward)
    self.button_change_predefine_color_inverting_matrix_forward_button.show()
    
    self.button_table_matrix_filters.attach(self.button_change_predefine_color_inverting_matrix_forward_button, left_attach=3, right_attach=4, top_attach=3, bottom_attach=4, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    
    self.button_table_matrix_filters.show()
    
    self.frame_matrix_filters.add(self.button_table_matrix_filters)
    
    self.frame_matrix_filters.show()
    
    self.matrix_vbox.pack_start(self.frame_matrix_filters)
    
    self.matrix_vbox.show()
    
    self.right_vbox.pack_start(self.matrix_vbox)
    
    self.intensity_vbox=gtk.VBox()
    self.intensity_vbox.set_size_request(315,360/2)
    
    self.frame_intensity_filters=gtk.Frame("Change intensity")
    self.frame_intensity_filters.set_size_request(315,315)
    self.frame_intensity_filters.set_border_width(5)
    
    self.table_intensity_filters=gtk.Table(rows=4, columns=4, homogeneous=False)
    self.table_intensity_filters.set_size_request(315,360/2)
    self.table_intensity_filters.set_border_width(5)
    
    
    self.frame_intensity_red=gtk.Frame("Red.")
    self.frame_intensity_red.set_label_align(0.0, 0.5)
    #self.frame_intensity_red.set_border_width(2)
    
    self.scale_intensity_red_container=gtk.EventBox()
    self.scale_intensity_red_container.modify_bg(gtk.STATE_NORMAL,self.button_matrix_blue_blue_container.get_colormap().alloc_color('#0000ff'))
    
    self.scale_intensity_red_adjustment=gtk.Adjustment(value=0, lower=-255, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.scale_intensity_red_scale=gtk.VScale(adjustment=self.scale_intensity_red_adjustment)
    self.scale_intensity_red_scale.set_size_request(40,120)
    self.scale_intensity_red_scale.set_draw_value(True)
    self.scale_intensity_red_scale.set_digits(0)
    self.scale_intensity_red_scale.set_inverted(True)
    self.scale_intensity_red_scale.add_mark(0, gtk.POS_RIGHT, None)
    self.scale_intensity_red_scale.set_value_pos(gtk.POS_BOTTOM)
    self.scale_intensity_red_scale.set_tooltip_text("Change the red pixels values intensity of the image.\nYou can use the arrows for accurate setting.")
    self.scale_intensity_red_scale.connect("value-changed",self.get_red_intensity)
    self.scale_intensity_red_scale.connect("move-slider",self.get_red_intensity)
    self.scale_intensity_red_scale.show()
    
    self.frame_intensity_red.add(self.scale_intensity_red_scale)
    self.frame_intensity_red.show()
    
    self.table_intensity_filters.attach(self.frame_intensity_red, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)

    
    self.frame_intensity_green=gtk.Frame("Green.")
    self.frame_intensity_green.set_label_align(0.0, 0.5)
    #self.frame_intensity_green.set_border_width(2)
   
    self.scale_intensity_green_adjustment=gtk.Adjustment(value=0, lower=-255, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.scale_intensity_green_scale=gtk.VScale(adjustment=self.scale_intensity_green_adjustment)
    self.scale_intensity_green_scale.set_size_request(40,120)
    self.scale_intensity_green_scale.set_draw_value(True)
    self.scale_intensity_green_scale.set_digits(0)
    self.scale_intensity_green_scale.set_inverted(True)
    self.scale_intensity_green_scale.add_mark(0, gtk.POS_RIGHT, None)
    self.scale_intensity_green_scale.set_value_pos(gtk.POS_BOTTOM)
    self.scale_intensity_green_scale.set_tooltip_text("Change the green pixels values intensity of the image.\nYou can use the arrows for accurate setting.")
    self.scale_intensity_green_scale.connect("value-changed",self.get_green_intensity)
    self.scale_intensity_green_scale.connect("move-slider",self.get_green_intensity)
    self.scale_intensity_green_scale.show()
    
    self.frame_intensity_green.add(self.scale_intensity_green_scale)
    self.frame_intensity_green.show()
    
    self.table_intensity_filters.attach(self.frame_intensity_green, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)

    
    
    self.frame_intensity_blue=gtk.Frame("Blue.")
    self.frame_intensity_blue.set_label_align(0.0, 0.5)
    self.frame_intensity_blue.set_border_width(2)
    
    self.scale_intensity_blue_adjustment=gtk.Adjustment(value=0, lower=-255, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.scale_intensity_blue_scale=gtk.VScale(adjustment=self.scale_intensity_blue_adjustment)
    self.scale_intensity_blue_scale.set_size_request(40,120)
    self.scale_intensity_blue_scale.set_draw_value(True)
    self.scale_intensity_blue_scale.set_digits(0)
    self.scale_intensity_blue_scale.set_inverted(True)
    self.scale_intensity_blue_scale.add_mark(0, gtk.POS_RIGHT, None)
    self.scale_intensity_blue_scale.set_value_pos(gtk.POS_BOTTOM)
    self.scale_intensity_blue_scale.set_tooltip_text("Change the blue pixels values intensity of the image.\nYou can use the arrows for accurate setting.")
    self.scale_intensity_blue_scale.connect("value-changed",self.get_blue_intensity)
    self.scale_intensity_blue_scale.connect("move-slider",self.get_blue_intensity)
    self.scale_intensity_blue_scale.show()
    
    self.frame_intensity_blue.add(self.scale_intensity_blue_scale)
    self.frame_intensity_blue.show()
    
    self.table_intensity_filters.attach(self.frame_intensity_blue, left_attach=2, right_attach=3, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    
    self.frame_intensity_alpha=gtk.Frame("Alpha.")
    self.frame_intensity_alpha.set_label_align(0.0, 0.5)
    #self.frame_intensity_alpha.set_border_width(2)
    
    self.scale_intensity_alpha_adjustment=gtk.Adjustment(value=0, lower=-255, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.scale_intensity_alpha_scale=gtk.VScale(adjustment=self.scale_intensity_alpha_adjustment)
    self.scale_intensity_alpha_scale.set_size_request(40,120)
    self.scale_intensity_alpha_scale.set_draw_value(True)
    self.scale_intensity_alpha_scale.set_digits(0)
    self.scale_intensity_alpha_scale.set_inverted(True)
    self.scale_intensity_alpha_scale.add_mark(0, gtk.POS_RIGHT, None)
    self.scale_intensity_alpha_scale.set_value_pos(gtk.POS_BOTTOM)
    self.scale_intensity_alpha_scale.set_tooltip_text("Change the alpha (transparency) pixels values intensity of the image.\nYou can use the arrows for accurate setting.")
    self.scale_intensity_alpha_scale.connect("value-changed",self.get_alpha_intensity)
    self.scale_intensity_alpha_scale.connect("move-slider",self.get_alpha_intensity)
    self.scale_intensity_alpha_scale.show()
    
    self.frame_intensity_alpha.add(self.scale_intensity_alpha_scale)
    self.frame_intensity_alpha.show()
    
    self.table_intensity_filters.attach(self.frame_intensity_alpha, left_attach=3, right_attach=4, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    
    self.frame_intensity_image=gtk.Frame("Image global intensity.")
    self.frame_intensity_image.set_label_align(0.0, 0.5)
    #self.frame_intensity_image.set_border_width(2)
    
    self.scale_intensity_image_adjustment=gtk.Adjustment(value=0, lower=-255, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.scale_intensity_image_scale=gtk.HScale(adjustment=self.scale_intensity_image_adjustment)
    self.scale_intensity_image_scale.set_size_request(120,24)
    self.scale_intensity_image_scale.set_draw_value(True)
    self.scale_intensity_image_scale.set_digits(0)
    self.scale_intensity_image_scale.add_mark(0, gtk.POS_BOTTOM, None)
    self.scale_intensity_image_scale.set_value_pos(gtk.POS_RIGHT)
    self.scale_intensity_image_scale.set_tooltip_text("Change all pixels values excluding the alpha (transparency) value.")
    self.scale_intensity_image_scale.connect("value-changed",self.get_global_image_intensity)
    self.scale_intensity_image_scale.connect("move-slider",self.get_global_image_intensity)
    self.scale_intensity_image_scale.show()
    
    self.frame_intensity_image.add(self.scale_intensity_image_scale)
    self.frame_intensity_image.show()
    
    self.table_intensity_filters.attach(self.frame_intensity_image, left_attach=0, right_attach=4, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)

    
    self.scale_intensity_apply_button=gtk.Button()
    self.scale_intensity_apply_button_label=gtk.Label("   Apply intensity change")
    self.scale_intensity_apply_button_label.show()
    self.scale_intensity_apply_button_space=gtk.Label("     ")
    self.scale_intensity_apply_button_space.show()
    self.scale_intensity_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_APPLY,1)
    self.scale_intensity_apply_button_image.show()
    self.scale_intensity_apply_button_hbox=gtk.HBox()
    self.scale_intensity_apply_button_hbox.pack_start(self.scale_intensity_apply_button_space,False,False,0)
    self.scale_intensity_apply_button_hbox.pack_start(self.scale_intensity_apply_button_image,False,False,0)
    self.scale_intensity_apply_button_hbox.pack_start(self.scale_intensity_apply_button_label,False,False,0)
    self.scale_intensity_apply_button_hbox.show()
    self.scale_intensity_apply_button.add(self.scale_intensity_apply_button_hbox)
    #self.scale_intensity_apply_button.set_image(self.scale_intensity_apply_button_image)
    self.scale_intensity_apply_button.set_size_request(120,32)
    self.scale_intensity_apply_button.set_tooltip_text("Apply intensity value changing, with the current setting values, on every pixel.")
    self.scale_intensity_apply_button.connect("button-press-event",process_effect.set_intensity_change)
    self.scale_intensity_apply_button.show()
    
    self.table_intensity_filters.attach(self.scale_intensity_apply_button, left_attach=0, right_attach=4, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=0, ypadding=0)
          
    self.table_intensity_filters.show()
    
    self.frame_intensity_filters.add(self.table_intensity_filters)    
        
    self.frame_intensity_filters.show()    
    
    self.intensity_vbox.pack_start(self.frame_intensity_filters)
    
    self.intensity_vbox.show()
    
    self.right_vbox.pack_start(self.intensity_vbox)

  def change_execution_speed(self,widget,execution_speed) :
    self.reset_execution_speed_image()
    self.execution_speed=int(execution_speed)
    self.save_execution_speed(execution_speed)
    self.image_menu_execution_speed_selected=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
    self.image_menu_execution_speed_selected.show()
    widget.set_image(self.image_menu_execution_speed_selected)
  
  def save_execution_speed(self,execution_speed) :
    save_execution_speed_file=file("/usr/share/PyImaging/Settings/execution_speed.pkl","wb")
    cPickle.dump(int(execution_speed),save_execution_speed_file)
    
  def load_execution_speed(self) :
    save_execution_speed_file=file("/usr/share/PyImaging/Settings/execution_speed.pkl","rb")
    execution_speed=cPickle.load(save_execution_speed_file)
    self.execution_speed=int(execution_speed)
    if int(execution_speed) == 10 :
      self.image_menu_execution_speed_selection_10=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_10.show()
    else :
      self.image_menu_execution_speed_selection_10=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_10.show()
    if int(execution_speed) == 20 :
      self.image_menu_execution_speed_selection_20=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_20.show()
    else :
      self.image_menu_execution_speed_selection_20=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_20.show()
    if int(execution_speed) == 30 :
      self.image_menu_execution_speed_selection_30=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_30.show()
    else :
      self.image_menu_execution_speed_selection_30=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_30.show()
    if int(execution_speed) == 40 :
      self.image_menu_execution_speed_selection_40=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_40.show()
    else :
      self.image_menu_execution_speed_selection_40=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_40.show()
    if int(execution_speed) == 50 :
      self.image_menu_execution_speed_selection_50=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_50.show()
    else :
      self.image_menu_execution_speed_selection_50=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_50.show()
    if int(execution_speed) == 60 :
      self.image_menu_execution_speed_selection_60=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_60.show()
    else :
      self.image_menu_execution_speed_selection_60=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_60.show()
    if int(execution_speed) == 70 :
      self.image_menu_execution_speed_selection_70=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_70.show()
    else :
      self.image_menu_execution_speed_selection_70=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_70.show()
    if int(execution_speed) == 80 :
      self.image_menu_execution_speed_selection_80=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_80.show()
    else :
      self.image_menu_execution_speed_selection_80=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_80.show()
    if int(execution_speed) == 90 :
      self.image_menu_execution_speed_selection_90=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_90.show()
    else :
      self.image_menu_execution_speed_selection_90=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_90.show()
    if int(execution_speed) == 100 :
      self.image_menu_execution_speed_selection_100=gtk.image_new_from_stock(gtk.STOCK_MEDIA_RECORD,1)
      self.image_menu_execution_speed_selection_100.show()
    else :
      self.image_menu_execution_speed_selection_100=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
      self.image_menu_execution_speed_selection_100.show() 
   
    self.menu_settings_main_speed_10.set_image(self.image_menu_execution_speed_selection_10)
    self.menu_settings_main_speed_20.set_image(self.image_menu_execution_speed_selection_20)
    self.menu_settings_main_speed_30.set_image(self.image_menu_execution_speed_selection_30)
    self.menu_settings_main_speed_40.set_image(self.image_menu_execution_speed_selection_40)
    self.menu_settings_main_speed_50.set_image(self.image_menu_execution_speed_selection_50)
    self.menu_settings_main_speed_60.set_image(self.image_menu_execution_speed_selection_60)
    self.menu_settings_main_speed_70.set_image(self.image_menu_execution_speed_selection_70)
    self.menu_settings_main_speed_80.set_image(self.image_menu_execution_speed_selection_80)
    self.menu_settings_main_speed_90.set_image(self.image_menu_execution_speed_selection_90)
    self.menu_settings_main_speed_100.set_image(self.image_menu_execution_speed_selection_100)
  
  def reset_execution_speed_image(self) :
    self.image_menu_execution_speed_not_selected_10=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_10.show()
    self.image_menu_execution_speed_not_selected_20=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_20.show()
    self.image_menu_execution_speed_not_selected_30=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_30.show()
    self.image_menu_execution_speed_not_selected_40=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_40.show()
    self.image_menu_execution_speed_not_selected_50=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_50.show()
    self.image_menu_execution_speed_not_selected_60=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_60.show()
    self.image_menu_execution_speed_not_selected_70=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_70.show()
    self.image_menu_execution_speed_not_selected_80=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_80.show()
    self.image_menu_execution_speed_not_selected_90=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_90.show()
    self.image_menu_execution_speed_not_selected_100=gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,1)
    self.image_menu_execution_speed_not_selected_100.show()
    self.menu_settings_main_speed_10.set_image(self.image_menu_execution_speed_not_selected_10)
    self.menu_settings_main_speed_20.set_image(self.image_menu_execution_speed_not_selected_20)
    self.menu_settings_main_speed_30.set_image(self.image_menu_execution_speed_not_selected_30)
    self.menu_settings_main_speed_40.set_image(self.image_menu_execution_speed_not_selected_40)
    self.menu_settings_main_speed_50.set_image(self.image_menu_execution_speed_not_selected_50)
    self.menu_settings_main_speed_60.set_image(self.image_menu_execution_speed_not_selected_60)
    self.menu_settings_main_speed_70.set_image(self.image_menu_execution_speed_not_selected_70)
    self.menu_settings_main_speed_80.set_image(self.image_menu_execution_speed_not_selected_80)
    self.menu_settings_main_speed_90.set_image(self.image_menu_execution_speed_not_selected_90)
    self.menu_settings_main_speed_100.set_image(self.image_menu_execution_speed_not_selected_100)
    
  def change_predefine_color_inverting_matrix_forward(self,widget,event) :
    self.predefine_color_inverting_matrix_index += 1
    
    if self.predefine_color_inverting_matrix_index == 25 :
      self.predefine_color_inverting_matrix_index=0
    
    exec("change_matrix.matrix{0}(self)".format(str(self.predefine_color_inverting_matrix_index).zfill(2)))
      
  def change_predefine_color_inverting_matrix_backward(self,widget,event) :
    self.predefine_color_inverting_matrix_index -= 1
    
    if self.predefine_color_inverting_matrix_index == -1 :
      self.predefine_color_inverting_matrix_index=24
    
    exec("change_matrix.matrix{0}(self)".format(str(self.predefine_color_inverting_matrix_index).zfill(2)))
  
  def set_color_inverting_matrix_red_value(self,widget,event) :
    if widget.get_name() == "red:red" :
      if widget.get_data("value") == "0" :
        self.button_matrix_red_red_label.set_text("1")
        self.button_matrix_red_red_button.set_data("value","1")
        
        self.button_matrix_red_green_label.set_text("0")
        self.button_matrix_red_green_button.set_data("value","0")
        
        self.button_matrix_red_blue_label.set_text("0")
        self.button_matrix_red_blue_button.set_data("value","0")
      elif widget.get_data("value") == "1" :
        self.button_matrix_red_red_label.set_text("0")
        self.button_matrix_red_red_button.set_data("value","0")
        
        
    elif widget.get_name() == "red:green" :
      if widget.get_data("value") == "0" :
        self.button_matrix_red_green_label.set_text("1")
        self.button_matrix_red_green_button.set_data("value","1")
        
        self.button_matrix_red_red_label.set_text("0")
        self.button_matrix_red_red_button.set_data("value","0")
        
        self.button_matrix_red_blue_label.set_text("0")
        self.button_matrix_red_blue_button.set_data("value","0")
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_red_green_label.set_text("0")
        self.button_matrix_red_green_button.set_data("value","0")  
        
    elif widget.get_name() == "red:blue" :
      if widget.get_data("value") == "0" :
        self.button_matrix_red_blue_label.set_text("1")
        self.button_matrix_red_blue_button.set_data("value","1")
        
        self.button_matrix_red_red_label.set_text("0")
        self.button_matrix_red_red_button.set_data("value","0")
        
        self.button_matrix_red_green_label.set_text("0")
        self.button_matrix_red_green_button.set_data("value","0") 
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_red_blue_label.set_text("0")
        self.button_matrix_red_blue_button.set_data("value","0")    
        
    self.reset_color_inverting_matrix_tooltip()    
        
  def set_color_inverting_matrix_green_value(self,widget,event) :
    if widget.get_name() == "green:red" :
      if widget.get_data("value") == "0" :
        self.button_matrix_green_red_label.set_text("1")
        self.button_matrix_green_red_button.set_data("value","1")
        
        self.button_matrix_green_green_label.set_text("0")
        self.button_matrix_green_green_button.set_data("value","0")
        
        self.button_matrix_green_blue_label.set_text("0")
        self.button_matrix_green_blue_button.set_data("value","0")
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_green_red_label.set_text("0")
        self.button_matrix_green_red_button.set_data("value","0")     
        
    elif widget.get_name() == "green:green" :
      if widget.get_data("value") == "0" :
        self.button_matrix_green_green_label.set_text("1")
        self.button_matrix_green_green_button.set_data("value","1")
        
        self.button_matrix_green_red_label.set_text("0")
        self.button_matrix_green_red_button.set_data("value","0")
        
        self.button_matrix_green_blue_label.set_text("0")
        self.button_matrix_green_blue_button.set_data("value","0") 
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_green_green_label.set_text("0")
        self.button_matrix_green_green_button.set_data("value","0")     
        
    elif widget.get_name() == "green:blue" :
      if widget.get_data("value") == "0" :
        self.button_matrix_green_blue_label.set_text("1")
        self.button_matrix_green_blue_button.set_data("value","1")
        
        self.button_matrix_green_red_label.set_text("0")
        self.button_matrix_green_red_button.set_data("value","0")
        
        self.button_matrix_green_green_label.set_text("0")
        self.button_matrix_green_green_button.set_data("value","0")  
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_green_blue_label.set_text("0")
        self.button_matrix_green_blue_button.set_data("value","0")  
   
    self.reset_color_inverting_matrix_tooltip()
        
  def set_color_inverting_matrix_blue_value(self,widget,event) :
    if widget.get_name() == "blue:red" :
      if widget.get_data("value") == "0" :
        self.button_matrix_blue_red_label.set_text("1")
        self.button_matrix_blue_red_button.set_data("value","1")
        
        self.button_matrix_blue_green_label.set_text("0")
        self.button_matrix_blue_green_button.set_data("value","0")
        
        self.button_matrix_blue_blue_label.set_text("0")
        self.button_matrix_blue_blue_button.set_data("value","0")
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_blue_red_label.set_text("0")
        self.button_matrix_blue_red_button.set_data("value","0")  
        
    elif widget.get_name() == "blue:green" :
      if widget.get_data("value") == "0" :
        self.button_matrix_blue_green_label.set_text("1")
        self.button_matrix_blue_green_button.set_data("value","1")
        
        self.button_matrix_blue_red_label.set_text("0")
        self.button_matrix_blue_red_button.set_data("value","0")
        
        self.button_matrix_blue_blue_label.set_text("0")
        self.button_matrix_blue_blue_button.set_data("value","0") 
        
      elif widget.get_data("value") == "1" :
        self.button_matrix_blue_green_label.set_text("0")
        self.button_matrix_blue_green_button.set_data("value","0")  
        
    elif widget.get_name() == "blue:blue" :
      if widget.get_data("value") == "0" :
        self.button_matrix_blue_blue_label.set_text("1")
        self.button_matrix_blue_blue_button.set_data("value","1")
        
        self.button_matrix_blue_red_label.set_text("0")
        self.button_matrix_blue_red_button.set_data("value","0")
        
        self.button_matrix_blue_green_label.set_text("0")
        self.button_matrix_blue_green_button.set_data("value","0")             
      
      elif widget.get_data("value") == "1" :
        self.button_matrix_blue_blue_label.set_text("0")
        self.button_matrix_blue_blue_button.set_data("value","0")  
    
    self.reset_color_inverting_matrix_tooltip()
    
  def reset_color_inverting_matrix_tooltip(self) :
    self.frame_matrix_filters.set_tooltip_text("Color inverter matrix:\nSet one value color representing row on one,\nto configure an color inversion matrix,\nor use the arrows to select an predefine color inversion matrix.")

  
  def get_color_inverting_matrix(self) :
    self.cmatrix=range(0,16)
    
    self.cmatrix[0]=int(self.button_matrix_red_red_button.get_data("value"))   ; self.cmatrix[4]=int(self.button_matrix_green_red_button.get_data("value"))   ; self.cmatrix[8]=int(self.button_matrix_blue_red_button.get_data("value"))   ; self.cmatrix[3]=0
    self.cmatrix[1]=int(self.button_matrix_red_green_button.get_data("value")) ; self.cmatrix[5]=int(self.button_matrix_green_green_button.get_data("value")) ; self.cmatrix[9]=int(self.button_matrix_blue_green_button.get_data("value")) ; self.cmatrix[7]=0
    self.cmatrix[2]=int(self.button_matrix_red_blue_button.get_data("value"))  ; self.cmatrix[6]=int(self.button_matrix_green_blue_button.get_data("value"))  ; self.cmatrix[10]=int(self.button_matrix_blue_blue_button.get_data("value")) ; self.cmatrix[11]=0 
    self.cmatrix[12]=0                                                         ; self.cmatrix[13]=0                                                           ; self.cmatrix[14]=0                                                          ; self.cmatrix[15]=1                                                                                  
    
    
  def get_red_intensity(self,widget,event=False) :
    self.red_intensity_value=self.scale_intensity_red_adjustment.get_value()
    self.set_intensity_action="RGBA"
    
  def get_green_intensity(self,widget,event=False) :
    self.green_intensity_value=self.scale_intensity_green_adjustment.get_value() 
    self.set_intensity_action="RGBA"
    
  def get_blue_intensity(self,widget,event=False) :
    self.blue_intensity_value=self.scale_intensity_blue_adjustment.get_value()  
    self.set_intensity_action="RGBA"
    
  def get_alpha_intensity(self,widget,event=False) :
    self.alpha_intensity_value=self.scale_intensity_alpha_adjustment.get_value()  
    self.set_intensity_action="RGBA"
    
  def get_global_image_intensity(self,widget,event=False) :
    self.global_intensity_value=self.scale_intensity_image_adjustment.get_value()
    self.set_intensity_action="ALL"
    
  def open_scaling_editor(self,widget,editor_type) :
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if process_effect.do_undo :
      process_effect.update_after_undo()
    
    if editor_type == "redscale" :
      redscale_editor=Redscale_dialog()
      self.scaling_base, self.other_colors, self.green_value, self.blue_value, self.alpha_value = redscale_editor.create_dialog()
      del(redscale_editor)
      if self.scaling_base :
        
        # Getting pixels values from display and processing image instance.
        process_effect.acquire_data_from_image()
        
        self.create_progressbar_dialog("redscale")
        
    elif editor_type == "greenscale" :
      greenscale_editor=Greenscale_dialog()
      self.scaling_base, self.other_colors, self.red_value, self.blue_value, self.alpha_value = greenscale_editor.create_dialog()
      del(greenscale_editor)
      if self.scaling_base :
        
        # Getting pixels values from display and processing image instance.
        process_effect.acquire_data_from_image()
        
        self.create_progressbar_dialog("greenscale")  
    
    elif editor_type == "bluescale" :
      bluescale_editor=Blue_dialog()
      self.scaling_base, self.other_colors, self.red_value, self.green_value, self.alpha_value = bluescale_editor.create_dialog()
      del(bluescale_editor)
      if self.scaling_base :
        
        # Getting pixels values from display and processing image instance.
        process_effect.acquire_data_from_image()
        
        self.create_progressbar_dialog("bluescale")  
  
  def open_adjustment_editor(self,widget,event=False) :
    if not image_settings_file.image_instance_is_loaded :
      # No image is currently loaded.
      gui.no_image_loaded_error_dialog()
      return
    
    if gui.is_computing :
      # The programm is computing pixels, busy, we cannot apply an operation simultaneaously. 
      return
    
    if process_effect.do_undo :
      process_effect.update_after_undo()
      
    adjustment_dialog=Adjusment_dialog()
    adjustment_type,value=adjustment_dialog.create_dialog()
    
    if not isinstance(adjustment_type,bool) and not isinstance(value,bool) : 
      process_effect.apply_adjustment(adjustment_type,value)
    
    del(adjustment_dialog)
    
  
  def create_progressbar_dialog(self,type_of_computing) :
    self.progressbar_dialog=gtk.Dialog(title="Processing pixels computing", parent=self.main_window, flags=0, buttons=None)
    
    self.text_area=self.progressbar_dialog.get_content_area()
    
    self.text_area_label=gtk.Label("Process pixels computing...")
    self.text_area_label.show()
    
    self.text_area.pack_start(self.text_area_label)
    
    self.progressbar_area=self.progressbar_dialog.get_action_area()
    

    self.max_value=process_effect.processing_image_pixels_count
    
    self.progressbar_adjustment=gtk.Adjustment(value=0, lower=0, upper=self.max_value, step_incr=1, page_incr=0, page_size=0)
    
    self.progressbar = gtk.ProgressBar(self.progressbar_adjustment)
    self.progressbar.show()
    
    #self.action_hbox=self.progressbar_dialog.get_action_area()
    
    self.image_to_display_counter=0
    self.image_to_process_counter=0
    
    # Set the is busy variable on True.
    self.is_computing=True
    
    self.progressbar_area.pack_start(self.progressbar)
    
    if type_of_computing == "grayscale average" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_average)
    elif type_of_computing == "grayscale minimum" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_minimum)
    elif type_of_computing == "grayscale maximum" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_maximum)
    elif type_of_computing == "grayscale red" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_red_value)
    elif type_of_computing == "grayscale green" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_green_value)
    elif type_of_computing == "grayscale blue" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_grayscale_blue_value)
    elif type_of_computing == "colors intensity" :
      self.tempo=gtk.timeout_add (1, self.update_progressbar_change_colors_intensity_value)
    elif type_of_computing == "global colors intensity" :
      self.tempo=gtk.timeout_add (1,self.update_progressbar_change_global_image_intensity_value)
    elif type_of_computing == "colors inverting matrix" :
      self.saved_speed=self.execution_speed
      self.execution_speed=10
      self.tempo=gtk.timeout_add (1,self.update_progressbar_color_inverting_matrix)
    elif type_of_computing == "color matrix" :
      self.tempo=gtk.timeout_add (1,self.update_progressbar_color_scale_matrix)
    elif type_of_computing == "redscale" :
      self.tempo=gtk.timeout_add (1,self.update_progressbar_redscaling)  
    elif type_of_computing == "greenscale" :
      self.tempo=gtk.timeout_add (1,self.update_progressbar_greenscaling)  
    elif type_of_computing == "bluescale" :
      self.tempo=gtk.timeout_add (1,self.update_progressbar_bluescaling)    
    
    self.progressbar_dialog.show()  
  
  def reset_colors_intensity_values(self) :
    self.red_intensity_value=0
    self.scale_intensity_red_adjustment.set_value(0)
    
    self.green_intensity_value=0
    self.scale_intensity_green_adjustment.set_value(0)
    
    self.blue_intensity_value=0
    self.scale_intensity_blue_adjustment.set_value(0)
    
    self.alpha_intensity_value=0
    self.scale_intensity_alpha_adjustment.set_value(0)
  
  def reset_global_image_intensity_values(self) :
    self.global_intensity_value=0
    self.scale_intensity_image_adjustment.set_value(0)
  
  def stop_progressbar_and_set_result(self,type_of_computing=False)  :
    # Reset the is busy variable on False. 
    self.is_computing=False
    
    # Apply effect to display image instance.
    image_settings_file.image_to_display=image_settings_file.image_to_display.copy()
    image_settings_file.image_to_display.putdata(process_effect.image_to_display_pixels_array)
    
    # Saving GUI display image and store the settings.
    tmp_path="/tmp/PyImaging/pyimage_tmp_n_{1}.{0}".format(image_settings_file.image_instance.format.lower(),image_settings_file.images_counter)
    image_settings_file.image_to_display_filepath=tmp_path
    image_settings_file.image_to_display.save(tmp_path,format=image_settings_file.image_instance.format)
    process_effect.operation_list_displaying_image.append((image_settings_file.image_to_display,tmp_path))
    
    
    # Apply effect to processing image instance.
    image_settings_file.image_processing=image_settings_file.image_processing.copy()
    image_settings_file.image_processing.putdata(process_effect.processing_image_pixels_array)
  
    # Store effect processsing image instance in processing list.
    process_effect.operation_list_image_instance_processing.append(image_settings_file.image_processing)
    
    # Update instance counter.
    image_settings_file.images_counter += 1
    
    # Update GUI with display image instance.
    image_settings_file.configure_image_display()
    image_settings_file.display_image()
    
    gtk.timeout_remove(self.tempo)
    self.progressbar_dialog.destroy()
    
  
  def update_progressbar_grayscale_average(self) :
    
    
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
    
        for x in xrange(0,self.execution_speed) :
	  
	  gray=(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]) / 3
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	  self.image_to_display_counter += 1
	  
      else :
	
	gray=(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]) / 3
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	self.image_to_display_counter += 1
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	for x in xrange(0,self.execution_speed) :
	  gray=(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2]) / 3
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	  else :
	    gray=(gray,gray,gray)
	    
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
      else :
	gray=(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2]) / 3
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	else :
	  gray=(gray,gray,gray)
	  
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
	  
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_grayscale_minimum(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
      
	  gray=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	  self.image_to_display_counter += 1
      
      else :
	gray=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	self.image_to_display_counter += 1
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if  self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
      
	  gray=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
      
      else :
	
	gray=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_grayscale_maximum(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
      
	  gray=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
      
          self.image_to_display_counter += 1
      
      else :
	
	gray=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
    
	self.image_to_display_counter += 1
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  gray=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
	  
      else :
	gray=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
	
	
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_grayscale_red_value(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
	  
	  gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	  self.image_to_display_counter += 1
    
      else :
	
	gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	self.image_to_display_counter += 1
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	for x in range(0,self.execution_speed) :
	  gray=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
	  
      else :
	
	gray=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
	
	
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_grayscale_green_value(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
        
        for x in range(0,self.execution_speed) :
        
	  gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	  self.image_to_display_counter += 1
      
      else :
	gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	self.image_to_display_counter += 1
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in range(0,self.execution_speed) :
	  
	  gray=process_effect.processing_image_pixels_array[self.image_to_display_counter][1]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
	  
      else :
	gray=process_effect.processing_image_pixels_array[self.image_to_display_counter][1]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_grayscale_blue_value(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	for x in xrange(0,self.execution_speed) :
	  
	  gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	  self.image_to_display_counter += 1
      
      else :
	gray=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.image_to_display_pixels_array[self.image_to_display_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=gray
	self.image_to_display_counter += 1
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	for x in xrange(0,self.execution_speed) :
	
	  gray=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]
	  
	  if image_settings_file.image_has_alpha :
	    gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	  else :
	    gray=(gray,gray,gray)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	  self.image_to_process_counter += 1
      
      else :
	gray=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]
	  
	if image_settings_file.image_has_alpha :
	  gray=(gray,gray,gray,process_effect.processing_image_pixels_array[self.image_to_process_counter][3])
	else :
	  gray=(gray,gray,gray)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=gray
	self.image_to_process_counter += 1
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
    
    return True
  
  def update_progressbar_color_inverting_matrix(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
        
	  pixel_value=Color(ub_v=process_effect.image_to_display_pixels_array[self.image_to_display_counter])
	  pixel_value.set_in_float_values()
	  m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	  m.mult_matrix(self.cmatrix)
	  
	  pixel_value=Color(f_v=m.get_result_rgb())
	  
	  if image_settings_file.image_has_alpha :
	    pixel_value=pixel_value.get_ubyte_v_rgba()
	  else :
	    pixel_value=pixel_value.get_ubyte_v_rgb()
	    
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
      
      else :
	
	pixel_value=Color(ub_v=process_effect.image_to_display_pixels_array[self.image_to_display_counter])
	pixel_value.set_in_float_values()
	m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	m.mult_matrix(self.cmatrix)
	
	pixel_value=Color(f_v=m.get_result_rgb())
	
	if image_settings_file.image_has_alpha :
	  pixel_value=pixel_value.get_ubyte_v_rgba()
	else :
	  pixel_value=pixel_value.get_ubyte_v_rgb()
	  
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  pixel_value=Color(ub_v=process_effect.processing_image_pixels_array[self.image_to_process_counter])
	  pixel_value.set_in_float_values()
	  m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	  m.mult_matrix(self.cmatrix)
	  
	  pixel_value=Color(f_v=m.get_result_rgb()) 
	  
	  if image_settings_file.image_has_alpha :
	    pixel_value=pixel_value.get_ubyte_v_rgba()
	  else :
	    pixel_value=pixel_value.get_ubyte_v_rgb()
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
          self.image_to_process_counter += 1
      
      else :
	
	pixel_value=Color(ub_v=process_effect.processing_image_pixels_array[self.image_to_process_counter])
	pixel_value.set_in_float_values()
	m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	m.mult_matrix(self.cmatrix)
	
	pixel_value=Color(f_v=m.get_result_rgb()) 
	
	if image_settings_file.image_has_alpha :
	  pixel_value=pixel_value.get_ubyte_v_rgba()
	else :
	  pixel_value=pixel_value.get_ubyte_v_rgb()
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
	
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.execution_speed=self.saved_speed
      self.stop_progressbar_and_set_result()
     
    return True  
  
  def update_progressbar_color_scale_matrix(self) :
    
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  pixel_value=Color(ub_v=process_effect.image_to_display_pixels_array[self.image_to_display_counter])
	  m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	  pixel_value=Color(ub_v=m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value))
	  
	  if image_settings_file.image_has_alpha :
	    pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255),min(int(pixel_value.a),255))
	  else :
	    pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255))
	    
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
      
      else :
	
	pixel_value=Color(ub_v=process_effect.image_to_display_pixels_array[self.image_to_display_counter])
	m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	pixel_value=Color(ub_v=m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value))
	
	if image_settings_file.image_has_alpha :
	  pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255),min(int(pixel_value.a),255))
	else :
	  pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255))
	  
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
	  
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  pixel_value=Color(ub_v=process_effect.processing_image_pixels_array[self.image_to_process_counter])
	  m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	  m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value)
	  pixel_value=Color(ub_v=m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value))
	  
	  if image_settings_file.image_has_alpha :
	    pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255),min(int(pixel_value.a),255))
	  else :
	    pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255))
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
	  
      else :
	
	pixel_value=Color(ub_v=process_effect.processing_image_pixels_array[self.image_to_process_counter])
	m=CMatrix(pixel_value.r,pixel_value.g,pixel_value.b,pixel_value.a)
	m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value)
	pixel_value=Color(ub_v=m.colors_matrix(process_effect.red_values,process_effect.green_values,process_effect.blue_values,process_effect.alpha_value))
	
	if image_settings_file.image_has_alpha :
	  pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255),min(int(pixel_value.a),255))
	else :
	  pixel_value=(min(int(pixel_value.r),255),min(int(pixel_value.g),255),min(int(pixel_value.b),255))
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
	  
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      
      self.stop_progressbar_and_set_result()
    
    return True  
  
  def update_progressbar_change_colors_intensity_value(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
        
	  if self.red_intensity_value != 0 :
	    red=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+self.red_intensity_value,255)))
	  else :
	    red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  
	  if self.green_intensity_value != 0 :
	    green=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+self.green_intensity_value,255)))
	  else :
	    green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  
	  if self.blue_intensity_value != 0 :
	    blue=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]+self.blue_intensity_value,255)))
	  else :
	    blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]
	  
	  if image_settings_file.image_has_alpha :
	  
	    if self.alpha_intensity_value != 0 :
	      alpha=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]+self.alpha_intensity_value,255)))
	    else :
	      alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	    
	    pixel_value=(red,green,blue,alpha)
	    
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
      
      else :
	if self.red_intensity_value != 0 :
	  red=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+self.red_intensity_value,255)))
	else :
	  red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	
	if self.green_intensity_value != 0 :
	  green=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+self.green_intensity_value,255)))
	else :
	  green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	
	if self.blue_intensity_value != 0 :
	  blue=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]+self.blue_intensity_value,255)))
	else :
	  blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]
	
	if image_settings_file.image_has_alpha :
	
	  if self.alpha_intensity_value != 0 :
	    alpha=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]+self.alpha_intensity_value,255)))
	  else :
	    alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	  
	  pixel_value=(red,green,blue,alpha)
	  
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
	  
	  
      
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
      
        for x in xrange(0,self.execution_speed) :
      
	  if self.red_intensity_value != 0 :
	    red=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+self.red_intensity_value,255)))
	  else :
	    red=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  
	  if self.green_intensity_value != 0 :
	    green=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+self.green_intensity_value,255)))
	  else :
	    green=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	  
	  if self.blue_intensity_value != 0 :
	    blue=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]+self.blue_intensity_value,255)))
	  else :
	    blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]
	  
	  if image_settings_file.image_has_alpha :
	    if self.alpha_intensity_value != 0 :
	      alpha=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][3]+self.alpha_intensity_value,255)))
	    else :
	      alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	    
	    pixel_value=(red,green,blue,alpha)
	    
	  else :
	    pixel_value=(red,green,blue)
	    
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
      
      else :
	if self.red_intensity_value != 0 :
	  red=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+self.red_intensity_value,255)))
	else :
	  red=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	
	if self.green_intensity_value != 0 :
	  green=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+self.green_intensity_value,255)))
	else :
	  green=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	
	if self.blue_intensity_value != 0 :
	  blue=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]+self.blue_intensity_value,255)))
	else :
	  blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]
	
	if image_settings_file.image_has_alpha :
	  if self.alpha_intensity_value != 0 :
	    alpha=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][3]+self.alpha_intensity_value,255)))
	  else :
	    alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	  
	  pixel_value=(red,green,blue,alpha)
	  
	else :
	  pixel_value=(red,green,blue)
	  
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
      self.reset_colors_intensity_values()
    
    return True  
  
  def update_progressbar_change_global_image_intensity_value(self) :
    
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  red=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+self.global_intensity_value,255)))
	  green=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+self.global_intensity_value,255)))
	  blue=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]+self.global_intensity_value,255)))
	  
	  if image_settings_file.image_has_alpha :
	    alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
      
      else :
	
	red=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+self.global_intensity_value,255)))
	green=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+self.global_intensity_value,255)))
	blue=max(0,int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]+self.global_intensity_value,255)))
	
	if image_settings_file.image_has_alpha :
	  alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
	  
	  red=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+self.global_intensity_value,255)))
	  green=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+self.global_intensity_value,255)))
	  blue=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]+self.global_intensity_value,255)))
	  
	  if image_settings_file.image_has_alpha :
	    alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
	  
      else :
	
	red=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+self.global_intensity_value,255)))
	green=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+self.global_intensity_value,255)))
	blue=max(0,int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]+self.global_intensity_value,255)))
	
	if image_settings_file.image_has_alpha :
	  alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
	
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
      self.reset_global_image_intensity_values()
    
    return True  
  
  def update_progressbar_redscaling(self) :
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
	  
	  if self.scaling_base == "average" :
	    red=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    red=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "maximum" :
	    red=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "red" :
	    red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  elif self.scaling_base == "green" :
	    red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  elif self.scaling_base == "blue" :
	    red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	    
	  if self.other_colors == 0 :
	    green=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.green_value/100.),255))
	    blue=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.blue_value/100.),255))
	  elif self.other_colors == 1 :
	    green=int(self.green_value)
	    blue=int(self.blue_value)
	  else :
	    green=0
	    blue=0
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
    
      else :
	
	if self.scaling_base == "average" :
	  red=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  red=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "maximum" :
	  red=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "red" :
	  red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	elif self.scaling_base == "green" :
	  red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	elif self.scaling_base == "blue" :
	  red=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	  
	if self.other_colors == 0 :
	  green=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.green_value/100.),255))
	  blue=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.blue_value/100.),255))
	elif self.other_colors == 1 :
	  green=int(self.green_value)
	  blue=int(self.blue_value)
	else :
	  green=0
	  blue=0
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
	
	
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
	  if self.scaling_base == "average" :
	    red=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    red=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "maximum" :
	    red=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "red" :
	    red=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  elif self.scaling_base == "green" :
	    red=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	  elif self.scaling_base == "blue" :
	    red=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	    
	  if self.other_colors == 0 :
	    green=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.green_value/100.),255))
	    blue=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.blue_value/100.),255))
	  elif self.other_colors == 1 :
	    green=int(self.green_value)
	    blue=int(self.blue_value)
	  else :
	    green=0
	    blue=0
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
      
      else :
	
	if self.scaling_base == "average" :
	  red=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  red=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "maximum" :
	  red=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "red" :
	  red=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	elif self.scaling_base == "green" :
	  red=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	elif self.scaling_base == "blue" :
	  red=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	  
	if self.other_colors == 0 :
	  green=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.green_value/100.),255))
	  blue=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.blue_value/100.),255))
	elif self.other_colors == 1 :
	  green=int(self.green_value)
	  blue=int(self.blue_value)
	else :
	  green=0
	  blue=0
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][0]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
	  
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
      self.reset_global_image_intensity_values()
    
    return True  
    
  def update_progressbar_greenscaling(self) :
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  if self.scaling_base == "average" :
	    green=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    green=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "maximum" :
	    green=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "red" :
	    green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  elif self.scaling_base == "green" :
	    green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  elif self.scaling_base == "blue" :
	    green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	    
	  if self.other_colors == 0 :
	    red=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.red_value/100.),255))
	    blue=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.blue_value/100.),255))
	  elif self.other_colors == 1 :
	    red=int(self.red_value)
	    blue=int(self.blue_value)
	  else :
	    red=0
	    blue=0
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
      
      else :
	
	if self.scaling_base == "average" :
	  green=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  green=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "maximum" :
	  green=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "red" :
	  green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	elif self.scaling_base == "green" :
	  green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	elif self.scaling_base == "blue" :
	  green=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	  
	if self.other_colors == 0 :
	  red=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.red_value/100.),255))
	  blue=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.blue_value/100.),255))
	elif self.other_colors == 1 :
	  red=int(self.red_value)
	  blue=int(self.blue_value)
	else :
	  red=0
	  blue=0
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
	  
	  
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
      
	  if self.scaling_base == "average" :
	    green=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    green=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "maximum" :
	    green=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "red" :
	    green=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  elif self.scaling_base == "green" :
	    green=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	  elif self.scaling_base == "blue" :
	    green=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	    
	  if self.other_colors == 0 :
	    red=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.red_value/100.),255))
	    blue=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.blue_value/100.),255))
	  elif self.other_colors == 1 :
	    red=int(self.red_value)
	    blue=int(self.blue_value)
	  else :
	    red=0
	    blue=0
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
	  
      else :
	
	if self.scaling_base == "average" :
	  green=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  green=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "maximum" :
	  green=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "red" :
	  green=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	elif self.scaling_base == "green" :
	  green=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	elif self.scaling_base == "blue" :
	  green=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	  
	if self.other_colors == 0 :
	  red=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.red_value/100.),255))
	  blue=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.blue_value/100.),255))
	elif self.other_colors == 1 :
	  red=int(self.red_value)
	  blue=int(self.blue_value)
	else :
	  red=0
	  blue=0
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][1]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
	  
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
      self.reset_global_image_intensity_values()
    
    return True  
  
  def update_progressbar_bluescaling(self) :
    if self.image_to_display_counter < process_effect.image_to_display_pixels_count :
      
      if self.image_to_display_counter+self.execution_speed < process_effect.image_to_display_pixels_count :
	
	for x in xrange(0,self.execution_speed) :
	  
	  if self.scaling_base == "average" :
	    blue=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    blue=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "maximum" :
	    blue=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	  elif self.scaling_base == "red" :
	    blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	  elif self.scaling_base == "green" :
	    blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	  elif self.scaling_base == "blue" :
	    blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	    
	  if self.other_colors == 0 :
	    green=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.green_value/100.),255))
	    red=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.red_value/100.),255))
	  elif self.other_colors == 1 :
	    green=int(self.green_value)
	    red=int(self.red_value)
	  else :
	    green=0
	    red=0
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	  self.image_to_display_counter += 1
    
      else :
	
	if self.scaling_base == "average" :
	  blue=int( (process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]+process_effect.image_to_display_pixels_array[self.image_to_display_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  blue=min([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "maximum" :
	  blue=max([process_effect.image_to_display_pixels_array[self.image_to_display_counter][0],process_effect.image_to_display_pixels_array[self.image_to_display_counter][1],process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]])
	elif self.scaling_base == "red" :
	  blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][0]
	elif self.scaling_base == "green" :
	  blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][1]
	elif self.scaling_base == "blue" :
	  blue=process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]  
	  
	if self.other_colors == 0 :
	  green=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.green_value/100.),255))
	  red=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.red_value/100.),255))
	elif self.other_colors == 1 :
	  green=int(self.green_value)
	  red=int(self.red_value)
	else :
	  green=0
	  red=0
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.image_to_display_pixels_array[self.image_to_display_counter][2]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.image_to_display_pixels_array[self.image_to_display_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.image_to_display_pixels_array[self.image_to_display_counter]=pixel_value
	self.image_to_display_counter += 1
	  
    
    if self.image_to_process_counter < process_effect.processing_image_pixels_count :
      
      if self.image_to_process_counter+self.execution_speed < process_effect.processing_image_pixels_count :
        
        for x in xrange(0,self.execution_speed) :
	  
	  if self.scaling_base == "average" :
	    blue=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	  elif self.scaling_base == "minimum" :
	    blue=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "maximum" :
	    blue=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	  elif self.scaling_base == "red" :
	    blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	  elif self.scaling_base == "green" :
	    blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	  elif self.scaling_base == "blue" :
	    blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	    
	  if self.other_colors == 0 :
	    red=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.red_value/100.),255))
	    green=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.green_value/100.),255))
	  elif self.other_colors == 1 :
	    red=int(self.red_value)
	    green=int(self.green_value)
	  else :
	    red=0
	    green=0
	    
	  
	  if image_settings_file.image_has_alpha :
	    if self.other_colors == 0 :
	      alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.alpha_value/100.),255))
	    elif self.other_colors == 1 :
	      alpha=int(self.alpha_value)
	    else :
	      alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	      
	    pixel_value=(red,green,blue,alpha)
	  else :
	    pixel_value=(red,green,blue)
	  
	  process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	  self.image_to_process_counter += 1
	  
      else :
	
	if self.scaling_base == "average" :
	  blue=int( (process_effect.processing_image_pixels_array[self.image_to_process_counter][0]+process_effect.processing_image_pixels_array[self.image_to_process_counter][1]+process_effect.processing_image_pixels_array[self.image_to_process_counter][2])/3 )
	elif self.scaling_base == "minimum" :
	  blue=min([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "maximum" :
	  blue=max([process_effect.processing_image_pixels_array[self.image_to_process_counter][0],process_effect.processing_image_pixels_array[self.image_to_process_counter][1],process_effect.processing_image_pixels_array[self.image_to_process_counter][2]])
	elif self.scaling_base == "red" :
	  blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][0]
	elif self.scaling_base == "green" :
	  blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][1]
	elif self.scaling_base == "blue" :
	  blue=process_effect.processing_image_pixels_array[self.image_to_process_counter][2]  
	  
	if self.other_colors == 0 :
	  red=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.red_value/100.),255))
	  green=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.green_value/100.),255))
	elif self.other_colors == 1 :
	  red=int(self.red_value)
	  green=int(self.green_value)
	else :
	  red=0
	  green=0
	  
	
	if image_settings_file.image_has_alpha :
	  if self.other_colors == 0 :
	    alpha=int(min(process_effect.processing_image_pixels_array[self.image_to_process_counter][2]*(self.alpha_value/100.),255))
	  elif self.other_colors == 1 :
	    alpha=int(self.alpha_value)
	  else :
	    alpha=process_effect.processing_image_pixels_array[self.image_to_process_counter][3]
	    
	  pixel_value=(red,green,blue,alpha)
	else :
	  pixel_value=(red,green,blue)
	
	process_effect.processing_image_pixels_array[self.image_to_process_counter]=pixel_value
	self.image_to_process_counter += 1
      
      self.progressbar_adjustment.set_value(self.image_to_process_counter)
      self.progressbar.set_text(" Process pixel: %s / %s. " % (str(self.image_to_process_counter).zfill(len(str(self.max_value))),str(self.max_value)))
      
      
      
      
    
    if self.image_to_process_counter == process_effect.processing_image_pixels_count :
      self.stop_progressbar_and_set_result()
      self.reset_global_image_intensity_values()
    
    return True  
  
  def no_image_loaded_error_dialog(self) :
    self.no_image_loaded_error_message_dialog=gtk.MessageDialog(parent=self.main_window, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format=None)
    
    self.no_image_loaded_error_message_dialog.set_markup("<big>First load an image to process effects on,\n\tbefore applying actions !</big>" )
    self.no_image_loaded_error_message_dialog.show()
    self.no_image_loaded_error_message_dialog.run()
    self.no_image_loaded_error_message_dialog.destroy()
  
  def load_error_dialog(self,filepath) :
    self.load_error_message_dialog=gtk.MessageDialog(parent=self.main_window, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=None)
    spaces=len("Failed to load image file:")-len(basename(filepath))
    if spaces > 0 :
      spaces_1=((len("Failed to load image file:")-len(basename(filepath)))/2)*" "
      spaces_2=""
    elif spaces == 0 :
      spaces_1=""
      spaces_2=""
    else :
      spaces_1=""
      spaces_2=((len("Failed to load image file:")-len(basename(filepath)))/2)*" "
    
    self.load_error_message_dialog.set_markup("<big>Failed to load image file:\n%s%s%s</big>" % (spaces_1,basename(filepath),spaces_2) )
    self.load_error_message_dialog.show()
    self.load_error_message_dialog.run()
    self.load_error_message_dialog.destroy()
  
  def about_dialog(self,widget,event) :
    self.about_dialog=gtk.AboutDialog()
    self.about_dialog.set_name("PyImaging")
    self.about_dialog.set_program_name("PyImaging")
    self.about_dialog.set_version("1.0.0")
    self.about_dialog.set_copyright("gplv3")
    self.about_dialog.set_comments("Enjoy to process images with PyImaging.\nThank's to my mother and the doctors.\nStay away from drugs: drugs destroy your brain and your life !!!")
    self.license_file=file("/usr/share/PyImaging/License/gpl.txt","r")
    self.about_dialog.set_license(self.license_file.read())
    self.license_file.close()
    self.about_dialog.set_wrap_license(True)
    self.about_dialog.set_authors(["Bruggemann Eddie alias mrcyberfighter\nContact: mrcyberfighter@gmail.com\nEddie Bruggemann 2014 © gplv3."])
    self.about_dialog.set_documenters(["Bruggemann Eddie alias mrcyberfighter\nContact: mrcyberfighter@gmail.com\nEddie Bruggemann 2014 © gplv3.\n\nDocumentation *.pdf file available at:\n/usr/share/PyImaging/Documentation/\n/usr/share/doc/PyImaging/"])
    self.about_dialog.set_artists(["Bruggemann Eddie alias mrcyberfighter\nContact: mrcyberfighter@gmail.com\nEddie Bruggemann 2014 © gplv3."])
    self.icon_file=gtk.gdk.pixbuf_new_from_file("/usr/share/PyImaging/Icon/PyImaging_Icon.png")
    self.about_dialog.set_logo(self.icon_file)
    button_list=self.about_dialog.get_action_area().get_children()
    button_list[2].connect("button-press-event",self.destroy_about_dialog)
    self.about_dialog.show()
  
  def destroy_about_dialog(self,widget,event) :
    self.about_dialog.destroy()
  
  def shutdown(self,widget,event) :
    widget.destroy()
    gtk.main_quit()

  
  
  
      
  def run(self) :
    
    self.main_window.add(self.main_vbox)
    self.main_window.connect("delete_event",self.shutdown)
    self.main_window.show()
    gtk.main()
    
 
def cleam_tmp_files() :
  ''' Temporary files deletion function. at exit '''
  for v in listdir("/tmp/PyImaging/") :
    remove("/tmp/PyImaging/"+v)
    
  

if __name__ == "__main__" :
    atexit.register(cleam_tmp_files)
    if len(argv) == 1 :
      gui=GUI()
      image_settings_file.create_tmp_dir()
      gui.run()
    elif len(argv) == 2 :
      
      if isfile(argv[1]) :
	
        if argv[1].lower().endswith(".bmp") or argv[1].lower().endswith(".jpg") or argv[1].lower().endswith(".jpeg") or argv[1].lower().endswith(".pcx") or argv[1].lower().endswith(".pdf") or argv[1].lower().endswith(".png") or argv[1].lower().endswith(".ppm") or argv[1].lower().endswith(".tif") or argv[1].lower().endswith(".tiff") or argv[1].lower().endswith(".xbm") :
	    
	  gui=GUI()
	  image_settings_file.create_tmp_dir()
	  image_settings_file.image_filepath=argv[1]
	  if not image_settings_file.load_image_settings(argv[1]) :
	    del(gui)
	    quit()
	  image_settings_file.configure_image_display()
	  image_settings_file.display_image()
	  gui.run()
	  
	else :
	  print "Error, non-supported file format: %s" % basename(argv[1])
	  print "supported file formats: *.bmp | *.jpg | *.jpeg | *.pcx | *.pdf | *.png | *.ppm | *.tif | *.tiff"
	  quit()
      else :
	print "usage: %s image_filepath" % argv[0]
		
      

    

    




