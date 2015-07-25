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


import pygtk
pygtk.require('2.0')
import gtk
  
from os.path import basename, expanduser
  
from PIL import Image, ImageChops  
  
# Personnal modules.  
from filesloadselector import *
from filesaveasfilepathselector import *
from file_mergin_error_dialog import error_file_mergin_message


class Screen_dialog() :
  def __init__(self) :
    
    self.image1_filepath=False
    self.image2_filepath=False
    
    self.image1_format_str=""
    self.image2_format_str=""
    
    self.result_image_filepath,self.result_image_size,self.result_image_format=False,False,False
    
    self.image2_size_cmp=65536*64
    self.image1_size_cmp=65536*64
    
    self.last_loaded_image=False
    
    self.size=[0,0]
    
    self.width_spinner_bool=True
    
  
  def get_image1_filepath(self,widget,event) :
    image1_filepath_selector=File_Loading_Selector(True)
    filepath=image1_filepath_selector.select_file()
    image1_filepath_selector.select_file_toplevel.destroy()
    if filepath :
      self.image1_filepath=filepath
      
      self.image1_instance=Image.open(filepath)
      
      self.image1_format_str=self.image1_instance.format
      
      self.screen_image1_filename_entry.set_text(basename(filepath))
      
      size=self.image1_instance.size
      
      self.image1_size=[size[0],size[1]]
      
      self.last_loaded_image=1
      
      self.image1_size_cmp=(float(self.image1_size[0])+float(self.image1_size[1]))/2 
      
      self.image1_width_factor=float(self.image1_size[1])/float(self.image1_size[0]) 
      
      self.image1_height_factor=float(self.image1_size[0])/float(self.image1_size[1]) 
      
      self.result_file_path_format=self.image1_instance.format
      
      self.update_size_image()
      
  def get_image2_filepath(self,widget,event) :
    image2_filepath_selector=File_Loading_Selector(True)
    filepath=image2_filepath_selector.select_file()
    image2_filepath_selector.select_file_toplevel.destroy()
    if filepath :
      self.image2_filepath=filepath
      
      self.image2_instance=Image.open(filepath)
      
      self.image2_format_str=self.image2_instance.format
      
      self.screen_image2_filename_entry.set_text(basename(filepath))
      
      size=self.image2_instance.size
      
      self.image2_size=[size[0],size[1]]
      
      self.last_loaded_image=2
      
      self.image2_size_cmp=(float(self.image2_size[0])+float(self.image2_size[1]))/2 
      
      self.image2_width_factor=float(self.image2_size[1])/float(self.image2_size[0]) 
      
      self.image2_height_factor=float(self.image2_size[0])/float(self.image2_size[1]) 
      
      self.result_file_path_format=self.image2_instance.format
      
      self.update_size_image()      
        
  def get_result_image_filepath(self,widget,event) :
    if self.image1_filepath and self.image2_filepath :
      result_image_filepath_selector=File_Save_filepath_Selector(format_str=self.result_file_path_format,mode="RGBA",size=self.size,width_factor=self.width_factor,height_factor=self.height_factor)
      self.result_image_filepath,self.result_image_size,self.result_image_format=result_image_filepath_selector.select_file()
      result_image_filepath_selector.select_file_toplevel.destroy()
      if self.result_image_filepath :
        
        self.screen_save_as_filename_entry.set_text(basename(self.result_image_filepath))
        self.size=self.result_image_size
        self.screen_save_as_width_spinner.set_value(self.size[0])
        self.screen_save_as_height_spinner.set_value(self.size[1])
        
        
  def check_width_height_factors(self) :
    if self.image1_size_cmp <= self.image2_size_cmp :
      self.width_factor=self.image1_width_factor
      self.height_factor=self.image1_height_factor
      self.bool_compute_ratio=True
      self.size=self.image1_size  
      
      
      
    elif self.image2_size_cmp <= self.image1_size_cmp :
      self.width_factor=self.image2_width_factor
      self.height_factor=self.image2_height_factor
      self.bool_compute_ratio=True
      self.size=self.image2_size      
  
  def update_size_image(self) :
    self.check_width_height_factors()   
    
    self.screen_save_as_width_spinner.set_value(self.size[0])
    self.screen_save_as_height_spinner.set_value(self.size[1])
  
  
  
  def get_width_value(self,widget=False) :
    if widget :
      self.size[0]=int(widget.get_value())
      self.bool_compute_ratio=False
      self.ratio_computing()
      self.width_spinner_bool=True
    
  def get_height_value(self,widget=False) :
    if widget :
      self.size[1]=int(widget.get_value())
      self.bool_compute_ratio=False
      self.ratio_computing()
      self.width_spinner_bool=False
    
  def set_width_value(self) :
    self.screen_save_as_width_spinner.set_value(self.size[0])
    self.bool_change_size=True
    
  def set_height_value(self) :
    self.screen_save_as_height_spinner.set_value(self.size[1])
    self.bool_change_size=True
  
  def ratio_computing(self) :
    if not self.bool_compute_ratio :
      if self.width_spinner_bool :
        self.size[0]=int(self.screen_save_as_width_spinner.get_value())
        self.size[1]=int(self.size[0]*self.width_factor)
      else :
        self.size[1]=int(self.screen_save_as_height_spinner.get_value())
        self.size[0]=int(self.size[1]*self.height_factor)
        
      self.bool_change_size=True
      self.bool_compute_ratio=True 
      
      self.set_height_value()  
      self.set_width_value()
     
  
  def create_dialog(self) :
    global img1,img1_format,img2,img2_format,res
    
    self.screen_dialog=gtk.Window(type=gtk.WINDOW_TOPLEVEL)
    self.screen_dialog.set_title("Screen images files merging operation.")
    
    self.screen_dialog.connect("delete_event",closed)
    
    self.screen_dialog.set_size_request(512+256+16-4,512+128+16)
    self.screen_dialog.modify_bg(gtk.STATE_NORMAL,self.screen_dialog.get_colormap().alloc_color('#d0d0d0'))
    
    self.screen_main_area_vbox=gtk.VBox()
    
    self.screen_area_vbox=gtk.VBox()
    
    self.screen_description_frame=gtk.Frame(None)
    self.screen_description_frame.set_border_width(5)
    self.screen_description_frame_button_label=gtk.Button()
    self.screen_description_frame_button_label_label=gtk.Label(" Description")
    self.screen_description_frame_button_label_label.show()
    self.screen_description_frame_button_label_image=gtk.image_new_from_stock(gtk.STOCK_INFO,2)
    self.screen_description_frame_button_label_image.show()
    self.screen_description_frame_button_label_image_hbox=gtk.HBox()
    self.screen_description_frame_button_label_image_hbox.pack_start(self.screen_description_frame_button_label_image,False,False,0)
    self.screen_description_frame_button_label_image_hbox.pack_start(self.screen_description_frame_button_label_label,False,False,0)
    self.screen_description_frame_button_label_image_hbox.show()
    self.screen_description_frame_button_label.add(self.screen_description_frame_button_label_image_hbox)
    self.screen_description_frame_button_label.set_relief(gtk.RELIEF_NONE)
    self.screen_description_frame_button_label.show()
    self.screen_description_frame.set_label_widget(self.screen_description_frame_button_label)
    
    
    self.screen_description_eventbox=gtk.EventBox()
    
    self.screen_description_eventbox.modify_bg(gtk.STATE_NORMAL,self.screen_description_eventbox.get_colormap().alloc_color('#f0f0f0'))
    self.screen_description_eventbox.set_border_width(5)
    
    self.screen_description_label=gtk.Label()
    self.screen_description_label.set_use_markup(True)
    self.screen_description_label.set_markup("\n\t\t\t<big>Superimpose two inverted images on the top of each other:\n\t\t<big>Result = MAX - ((MAX-Image1)  * (MAX-Images2) / MAX)</big>\t\t\n<small>The image are converted to the same size (to the littler image) was is required for screen operation.</small></big>\n")
    self.screen_description_label.show()
    
    self.screen_description_eventbox.add(self.screen_description_label)
    self.screen_description_eventbox.show()
    
    self.screen_description_frame.add(self.screen_description_eventbox)
    self.screen_description_frame.show()
    
    self.screen_input_vbox=gtk.VBox()
    
    self.screen_input_frame=gtk.Frame()
    self.screen_input_frame.set_border_width(5)
    self.screen_input_frame_button_label=gtk.Button()
    self.screen_input_frame_button_label_label=gtk.Label(" Input")
    self.screen_input_frame_button_label_label.show()
    self.screen_input_frame_button_label_image=gtk.image_new_from_stock(gtk.STOCK_SAVE,2)
    self.screen_input_frame_button_label_image.show()
    self.screen_input_frame_button_label_hbox=gtk.HBox()
    self.screen_input_frame_button_label_hbox.pack_start(self.screen_input_frame_button_label_image,False,False,0)
    self.screen_input_frame_button_label_hbox.pack_start(self.screen_input_frame_button_label_label,False,False,0)
    self.screen_input_frame_button_label_hbox.show()
    self.screen_input_frame_button_label.add(self.screen_input_frame_button_label_hbox)
    self.screen_input_frame_button_label.set_relief(gtk.RELIEF_NONE)
    self.screen_input_frame_button_label.show()
    self.screen_input_frame.set_label_widget(self.screen_input_frame_button_label)
    
    self.screen_image1_file_selector_button=gtk.Button()
    self.screen_image1_file_selector_button_label=gtk.Label("    Select input file 1: ")
    self.screen_image1_file_selector_button_label.show()
    self.screen_image1_file_selector_button_space=gtk.Label("                      ")
    self.screen_image1_file_selector_button_space.show()
    self.screen_image1_file_selector_button.set_size_request(796/2-44,32)
    self.screen_image1_file_selector_button_image=gtk.image_new_from_stock(gtk.STOCK_OPEN,2)
    self.screen_image1_file_selector_button_image.show()
    self.screen_image1_file_selector_button_hbox=gtk.HBox()
    self.screen_image1_file_selector_button_hbox.pack_start(self.screen_image1_file_selector_button_space,False,False,0)
    self.screen_image1_file_selector_button_hbox.pack_start(self.screen_image1_file_selector_button_image,False,False,0)
    self.screen_image1_file_selector_button_hbox.pack_start(self.screen_image1_file_selector_button_label,False,False,0)
    self.screen_image1_file_selector_button_hbox.show()
    self.screen_image1_file_selector_button.add(self.screen_image1_file_selector_button_hbox)
    self.screen_image1_file_selector_button.connect("button-press-event",self.get_image1_filepath)
    self.screen_image1_file_selector_button.show()
    
    self.screen_image1_filename_entry=gtk.Entry()
    self.screen_image1_filename_entry.set_size_request(796/2-44,32)
    self.screen_image1_filename_entry.set_can_focus(False)
    self.screen_image1_filename_entry.set_alignment(0.5)
    self.screen_image1_filename_entry.show()
    
    self.screen_image2_file_selector_button=gtk.Button()
    self.screen_image2_file_selector_button_label=gtk.Label("    Select input file 2: ")
    self.screen_image2_file_selector_button_label.show()
    self.screen_image2_file_selector_button_space=gtk.Label("                      ")
    self.screen_image2_file_selector_button_space.show()
    self.screen_image2_file_selector_button.set_size_request(796/2-44,32)
    self.screen_image2_file_selector_button_image=gtk.image_new_from_stock(gtk.STOCK_OPEN,2)
    self.screen_image2_file_selector_button_image.show()
    self.screen_image2_file_selector_button_hbox=gtk.HBox()
    self.screen_image2_file_selector_button_hbox.pack_start(self.screen_image2_file_selector_button_space,False,False,0)
    self.screen_image2_file_selector_button_hbox.pack_start(self.screen_image2_file_selector_button_image,False,False,0)
    self.screen_image2_file_selector_button_hbox.pack_start(self.screen_image2_file_selector_button_label,False,False,0)
    self.screen_image2_file_selector_button_hbox.show()
    self.screen_image2_file_selector_button.add(self.screen_image2_file_selector_button_hbox)
    self.screen_image2_file_selector_button.connect("button-press-event",self.get_image2_filepath)
    self.screen_image2_file_selector_button.show()
    
    self.screen_image2_filename_entry=gtk.Entry()
    self.screen_image2_filename_entry.set_size_request(796/2-44,32)
    self.screen_image2_filename_entry.set_can_focus(False)
    self.screen_image2_filename_entry.set_alignment(0.5)
    self.screen_image2_filename_entry.show()
    
    self.screen_input_toolbar_up=gtk.Toolbar()
    self.screen_input_toolbar_up.set_border_width(5)
    self.screen_input_toolbar_up.modify_bg(gtk.STATE_NORMAL,self.screen_input_toolbar_up.get_colormap().alloc_color('#f0f0f0'))
    self.screen_input_toolbar_up.set_style(gtk.TOOLBAR_BOTH_HORIZ)
    self.screen_input_toolbar_up.append_space()
    self.screen_input_toolbar_up.append_widget(self.screen_image1_file_selector_button,tooltip_text="Select the first image file for screen operation.", tooltip_private_text="")
    self.screen_input_toolbar_up.append_space()
    self.screen_input_toolbar_up.append_widget(self.screen_image2_file_selector_button,tooltip_text="Select the second image file for screen operation.", tooltip_private_text="")
    self.screen_input_toolbar_up.append_space()
    self.screen_input_toolbar_up.show()
    
    
    self.screen_input_toolbar_down=gtk.Toolbar()
    self.screen_input_toolbar_down.set_border_width(5)
    self.screen_input_toolbar_down.set_style(gtk.TOOLBAR_BOTH_HORIZ)
    self.screen_input_toolbar_down.modify_bg(gtk.STATE_NORMAL,self.screen_input_toolbar_down.get_colormap().alloc_color('#f0f0f0'))
    self.screen_input_toolbar_down.append_space()
    self.screen_input_toolbar_down.append_widget(self.screen_image1_filename_entry,tooltip_text="", tooltip_private_text="")
    self.screen_input_toolbar_down.append_space()
    self.screen_input_toolbar_down.append_widget(self.screen_image2_filename_entry,tooltip_text="", tooltip_private_text="")
    self.screen_input_toolbar_down.append_space()
    self.screen_input_toolbar_down.show()
    
    self.screen_input_frame.add(self.screen_input_vbox)
    self.screen_input_frame.show()
    
    self.screen_output_hbox=gtk.HBox(False)
    
    self.screen_output_frame=gtk.Frame(None)
    self.screen_output_frame.set_border_width(5)
    self.screen_output_frame_button=gtk.Button()
    self.screen_output_frame_button_label=gtk.Label(" Ouput")
    self.screen_output_frame_button_label.show()
    self.screen_output_frame_button_image=gtk.image_new_from_stock(gtk.STOCK_SAVE,2)
    self.screen_output_frame_button_image.show()
    self.screen_output_frame_button_hbox=gtk.HBox()
    self.screen_output_frame_button_hbox.pack_start(self.screen_output_frame_button_image,False,False,0)
    self.screen_output_frame_button_hbox.pack_start(self.screen_output_frame_button_label,False,False,0)
    self.screen_output_frame_button_hbox.show()
    self.screen_output_frame_button.add(self.screen_output_frame_button_hbox)
    self.screen_output_frame_button.set_can_focus(False)
    self.screen_output_frame_button.set_relief(gtk.RELIEF_NONE)
    self.screen_output_frame_button.show()
    self.screen_output_frame.set_label_widget(self.screen_output_frame_button)
    
    self.screen_save_as_frame=gtk.Frame(None)
    self.screen_save_as_frame.set_border_width(5)
    self.screen_save_as_frame_button=gtk.Button()
    self.screen_save_as_frame_button_label=gtk.Label(" Save as")
    self.screen_save_as_frame_button_label.show()
    self.screen_save_as_frame_button_image=gtk.image_new_from_stock(gtk.STOCK_SAVE_AS,2)
    self.screen_save_as_frame_button_image.show()
    self.screen_save_as_frame_button_hbox=gtk.HBox()
    self.screen_save_as_frame_button_hbox.pack_start(self.screen_save_as_frame_button_image,False,False,0)
    self.screen_save_as_frame_button_hbox.pack_start(self.screen_save_as_frame_button_label,False,False,0)
    self.screen_save_as_frame_button_hbox.show()
    self.screen_save_as_frame_button.add(self.screen_save_as_frame_button_hbox)
    self.screen_save_as_frame_button.set_relief(gtk.RELIEF_NONE)
    self.screen_save_as_frame_button.show()
    self.screen_save_as_frame.set_label_widget(self.screen_save_as_frame_button)
    
    self.screen_save_as_table=gtk.Table(2,1,True)
    self.screen_save_as_table.set_border_width(5)
    
    self.screen_save_as_file_selector_button=gtk.Button()
    self.screen_save_as_file_selector_button_label=gtk.Label("    Select save as file:    ")
    self.screen_save_as_file_selector_button_label.show()
    self.screen_save_as_file_selector_button_space=gtk.Label("                                ")
    self.screen_save_as_file_selector_button_space.show()
    self.screen_save_as_file_selector_button.set_tooltip_text("Select the result file to save the darker operation as.")
    self.screen_save_as_file_selector_button.set_size_request(796/2+48,32)
    self.screen_save_as_file_selector_button_image=gtk.image_new_from_stock(gtk.STOCK_SAVE_AS,2)
    self.screen_save_as_file_selector_button_image.show()
    self.screen_save_as_file_selector_button_hbox=gtk.HBox()
    self.screen_save_as_file_selector_button_hbox.pack_start(self.screen_save_as_file_selector_button_space,False,False,0)
    self.screen_save_as_file_selector_button_hbox.pack_start(self.screen_save_as_file_selector_button_image,False,False,0)
    self.screen_save_as_file_selector_button_hbox.pack_start(self.screen_save_as_file_selector_button_label,False,False,0)
    self.screen_save_as_file_selector_button_hbox.show()
    self.screen_save_as_file_selector_button.add(self.screen_save_as_file_selector_button_hbox)
    self.screen_save_as_file_selector_button.connect("button-press-event",self.get_result_image_filepath)
    self.screen_save_as_file_selector_button.show()
    
    self.screen_save_as_filename_entry=gtk.Entry()
    self.screen_save_as_filename_entry.set_size_request(796/2+47,32)
    self.screen_save_as_filename_entry.set_can_focus(False)
    self.screen_save_as_filename_entry.set_alignment(0.5)
    self.screen_save_as_filename_entry.show()
    
    self.screen_save_as_table.attach(self.screen_save_as_file_selector_button, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_table.attach(self.screen_save_as_filename_entry, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_table.show()
    
    self.screen_save_as_frame.add(self.screen_save_as_table)
    self.screen_save_as_frame.show()
    
    self.screen_output_eventbox=gtk.EventBox()
    self.screen_output_eventbox.modify_bg(gtk.STATE_NORMAL,self.screen_output_eventbox.get_colormap().alloc_color('#f0f0f0'))
    self.screen_output_eventbox.set_border_width(5)
    
    self.screen_save_as_size_frame=gtk.Frame(None)
    self.screen_save_as_size_frame.set_border_width(5)
    self.screen_save_as_size_frame_button=gtk.Button()
    self.screen_save_as_size_frame_button_label=gtk.Label(" Size")
    self.screen_save_as_size_frame_button_label.show()
    self.screen_save_as_size_frame_button_image=gtk.image_new_from_stock(gtk.STOCK_FULLSCREEN,2)
    self.screen_save_as_size_frame_button_image.show()
    self.screen_save_as_size_frame_button_hbox=gtk.HBox()
    self.screen_save_as_size_frame_button_hbox.pack_start(self.screen_save_as_size_frame_button_image,False,False,0)
    self.screen_save_as_size_frame_button_hbox.pack_start(self.screen_save_as_size_frame_button_label,False,False,0)
    self.screen_save_as_size_frame_button_hbox.show()
    self.screen_save_as_size_frame_button.add(self.screen_save_as_size_frame_button_hbox)
    self.screen_save_as_size_frame_button.set_can_focus(False)
    self.screen_save_as_size_frame_button.set_relief(gtk.RELIEF_NONE)
    self.screen_save_as_size_frame_button.show()
    self.screen_save_as_size_frame.set_label_widget(self.screen_save_as_size_frame_button)
    
    self.screen_save_as_size_table=gtk.Table(2,2,True)
    self.screen_save_as_size_table.set_border_width(5)
    
    self.screen_save_as_width_label_button=gtk.Button()
    self.screen_save_as_width_label_button_label=gtk.Label("  Width")
    self.screen_save_as_width_label_button_label.show()
    self.screen_save_as_width_label_button_space=gtk.Label("  ")
    self.screen_save_as_width_label_button_space.show()
    self.screen_save_as_width_label_button.set_size_request(640/6,32)
    self.screen_save_as_width_label_button_image=gtk.image_new_from_stock(gtk.STOCK_ZOOM_100,2)
    self.screen_save_as_width_label_button_image.show()
    self.screen_save_as_width_label_button_hbox=gtk.HBox()
    self.screen_save_as_width_label_button_hbox.pack_start(self.screen_save_as_width_label_button_space,False,False,0)
    self.screen_save_as_width_label_button_hbox.pack_start(self.screen_save_as_width_label_button_image,False,False,0)
    self.screen_save_as_width_label_button_hbox.pack_start(self.screen_save_as_width_label_button_label,False,False,0)
    self.screen_save_as_width_label_button_hbox.show()
    self.screen_save_as_width_label_button.add(self.screen_save_as_width_label_button_hbox)
    self.screen_save_as_width_label_button.set_can_focus(False)
    self.screen_save_as_width_label_button.show()
    
    
    self.screen_save_as_width_spinner_adjusment=gtk.Adjustment(value=0, lower=0.0, upper=4096*16, step_incr=1, page_incr=0, page_size=0)
    self.screen_save_as_width_spinner=gtk.SpinButton(self.screen_save_as_width_spinner_adjusment,1,0)
    self.screen_save_as_width_spinner.set_tooltip_text("Change the result image width.")
    self.screen_save_as_width_spinner.set_size_request(640/6,32)
    self.screen_save_as_width_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY,gtk.STOCK_ZOOM_100)
    self.screen_save_as_width_spinner.connect("value-changed",self.get_width_value)
    self.screen_save_as_width_spinner.set_alignment(0.5)
    self.screen_save_as_width_spinner.show()
    
    self.screen_save_as_height_label_button=gtk.Button()
    self.screen_save_as_height_label_button_label=gtk.Label("  Height")
    self.screen_save_as_height_label_button_label.show()
    self.screen_save_as_height_label_button_space=gtk.Label("  ")
    self.screen_save_as_height_label_button_space.show()
    self.screen_save_as_height_label_button.set_size_request(640/6,32)
    self.screen_save_as_height_label_button_image=gtk.image_new_from_stock(gtk.STOCK_ZOOM_100,2)
    self.screen_save_as_height_label_button_image.show()
    self.screen_save_as_height_label_button_hbox=gtk.HBox()
    self.screen_save_as_height_label_button_hbox.pack_start(self.screen_save_as_height_label_button_space,False,False,0)
    self.screen_save_as_height_label_button_hbox.pack_start(self.screen_save_as_height_label_button_image,False,False,0)
    self.screen_save_as_height_label_button_hbox.pack_start(self.screen_save_as_height_label_button_label,False,False,0)
    self.screen_save_as_height_label_button_hbox.show()
    self.screen_save_as_height_label_button.add(self.screen_save_as_height_label_button_hbox)
    self.screen_save_as_height_label_button.set_can_focus(False)
    self.screen_save_as_height_label_button.show()
    
    self.screen_save_as_height_spinner_adjusment=gtk.Adjustment(value=0, lower=0.0, upper=4096*16, step_incr=1, page_incr=0, page_size=0)
    self.screen_save_as_height_spinner=gtk.SpinButton(self.screen_save_as_height_spinner_adjusment,1,0)
    self.screen_save_as_height_spinner.set_tooltip_text("Change the result image height.")
    self.screen_save_as_height_spinner.set_size_request(640/6,32)
    self.screen_save_as_height_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY,gtk.STOCK_ZOOM_100)
    self.screen_save_as_height_spinner.connect("value-changed",self.get_height_value)
    self.screen_save_as_height_spinner.set_alignment(0.5)
    self.screen_save_as_height_spinner.show()
    
    self.screen_save_as_size_table.attach(self.screen_save_as_width_label_button, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_size_table.attach(self.screen_save_as_width_spinner, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_size_table.attach(self.screen_save_as_height_label_button, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_size_table.attach(self.screen_save_as_height_spinner, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=5, ypadding=5)
    self.screen_save_as_size_table.show()
    
    self.screen_save_as_size_frame.add(self.screen_save_as_size_table)
    self.screen_save_as_size_frame.show()
    
    self.screen_output_hbox.pack_start(self.screen_save_as_frame,False,False,5)
    self.screen_output_hbox.pack_start(self.screen_save_as_size_frame,False,False,5)
    self.screen_output_hbox.show()
    
    
    self.screen_output_eventbox.add(self.screen_output_hbox)
    self.screen_output_eventbox.show()
    
    self.screen_output_frame.add(self.screen_output_eventbox)
    self.screen_output_frame.show()
    
    self.screen_input_vbox.pack_start(self.screen_input_toolbar_up,False,False,5)
    self.screen_input_vbox.pack_start(self.screen_input_toolbar_down,False,False,5)
    self.screen_input_vbox.show()

    self.screen_area_vbox.pack_start(self.screen_description_frame)
    self.screen_area_vbox.pack_start(self.screen_input_frame)
    self.screen_area_vbox.pack_start(self.screen_output_frame)
    self.screen_area_vbox.show()
    
    self.screen_main_area_vbox.pack_start(self.screen_area_vbox,False,False,5)
    
    self.screen_dialog_action_hbox=gtk.HBox()
    
    self.screen_dialog_action_area_frame=gtk.Frame()
    self.screen_dialog_action_area_frame.set_border_width(5)
    self.screen_dialog_action_area_button=gtk.Button()
    self.screen_dialog_action_area_button_label=gtk.Label(" Actions")
    self.screen_dialog_action_area_button_label.show()
    self.screen_dialog_action_area_button_image=gtk.image_new_from_stock(gtk.STOCK_FLOPPY,2)
    self.screen_dialog_action_area_button_image.show()
    self.screen_dialog_action_area_button.set_can_focus(False)
    self.screen_dialog_action_area_button_hbox=gtk.HBox()
    self.screen_dialog_action_area_button_hbox.pack_start(self.screen_dialog_action_area_button_image,False,False,0)
    self.screen_dialog_action_area_button_hbox.pack_start(self.screen_dialog_action_area_button_label,False,False,0)
    self.screen_dialog_action_area_button_hbox.show()
    self.screen_dialog_action_area_button.add(self.screen_dialog_action_area_button_hbox)
    self.screen_dialog_action_area_button.set_relief(gtk.RELIEF_NONE)
    self.screen_dialog_action_area_button.show()
    self.screen_dialog_action_area_frame.set_label_widget(self.screen_dialog_action_area_button)
    
    self.screen_dialog_action_area_toolbar=gtk.Toolbar()
    self.screen_dialog_action_area_toolbar.set_border_width(5)
    self.screen_dialog_action_area_toolbar.set_size_request(796-45,60)
    self.screen_dialog_action_area_toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)
    self.screen_dialog_action_area_toolbar.modify_bg(gtk.STATE_NORMAL,self.screen_dialog_action_area_toolbar.get_colormap().alloc_color('#f0f0f0'))
    
    self.screen_dialog_action_area_cancel_button=gtk.Button()
    self.screen_dialog_action_area_cancel_button_label=gtk.Label("  Cancel  ")
    self.screen_dialog_action_area_cancel_button_label.show()
    self.screen_dialog_action_area_cancel_button_space=gtk.Label("                  ")
    self.screen_dialog_action_area_cancel_button_space.show()
    self.screen_dialog_action_area_cancel_button.set_border_width(5)
    self.screen_dialog_action_area_cancel_button.set_size_request(796/4+31,32)
    self.screen_dialog_action_area_cancel_button_image=gtk.image_new_from_stock(gtk.STOCK_CANCEL,4)
    self.screen_dialog_action_area_cancel_button_image.show()
    self.screen_dialog_action_area_cancel_button_hbox=gtk.HBox()
    self.screen_dialog_action_area_cancel_button_hbox.pack_start(self.screen_dialog_action_area_cancel_button_space,False,False,0)
    self.screen_dialog_action_area_cancel_button_hbox.pack_start(self.screen_dialog_action_area_cancel_button_image,False,False,0)
    self.screen_dialog_action_area_cancel_button_hbox.pack_start(self.screen_dialog_action_area_cancel_button_label,False,False,0)
    self.screen_dialog_action_area_cancel_button_hbox.show()
    self.screen_dialog_action_area_cancel_button.add(self.screen_dialog_action_area_cancel_button_hbox)
    self.screen_dialog_action_area_cancel_button.connect("button-press-event",self.cancel)
    self.screen_dialog_action_area_cancel_button.show()
    
    self.screen_dialog_action_area_preview_button=gtk.Button()
    self.screen_dialog_action_area_preview_button_label=gtk.Label("  Preview  ")
    self.screen_dialog_action_area_preview_button_label.show()
    self.screen_dialog_action_area_preview_button_space=gtk.Label("                 ")
    self.screen_dialog_action_area_preview_button_space.show()
    self.screen_dialog_action_area_preview_button.set_border_width(5)
    self.screen_dialog_action_area_preview_button.set_size_request(796/4+31,32)
    self.screen_dialog_action_area_preview_button_image=gtk.image_new_from_stock(gtk.STOCK_INDENT,4)
    self.screen_dialog_action_area_preview_button_image.show()
    self.screen_dialog_action_area_preview_button_hbox=gtk.HBox()
    self.screen_dialog_action_area_preview_button_hbox.pack_start(self.screen_dialog_action_area_preview_button_space,False,False,0)
    self.screen_dialog_action_area_preview_button_hbox.pack_start(self.screen_dialog_action_area_preview_button_image,False,False,0)
    self.screen_dialog_action_area_preview_button_hbox.pack_start(self.screen_dialog_action_area_preview_button_label,False,False,0)
    self.screen_dialog_action_area_preview_button_hbox.show()
    self.screen_dialog_action_area_preview_button.add(self.screen_dialog_action_area_preview_button_hbox)
    self.screen_dialog_action_area_preview_button.connect("button-press-event",self.preview)
    self.screen_dialog_action_area_preview_button.show()
    
    self.screen_dialog_action_area_confirm_button=gtk.Button()
    self.screen_dialog_action_area_confirm_button_label=gtk.Label("  Apply  ")
    self.screen_dialog_action_area_confirm_button_label.show()
    self.screen_dialog_action_area_confirm_button_space=gtk.Label("                  ")
    self.screen_dialog_action_area_confirm_button_space.show()
    self.screen_dialog_action_area_confirm_button.set_border_width(5)
    self.screen_dialog_action_area_confirm_button.set_size_request(796/4+31,32)
    self.screen_dialog_action_area_confirm_button_image=gtk.image_new_from_stock(gtk.STOCK_OK,4)
    self.screen_dialog_action_area_confirm_button_image.show()
    self.screen_dialog_action_area_confirm_button_hbox=gtk.HBox()
    self.screen_dialog_action_area_confirm_button_hbox.pack_start(self.screen_dialog_action_area_confirm_button_space,False,False,0)
    self.screen_dialog_action_area_confirm_button_hbox.pack_start(self.screen_dialog_action_area_confirm_button_image,False,False,0)
    self.screen_dialog_action_area_confirm_button_hbox.pack_start(self.screen_dialog_action_area_confirm_button_label,False,False,0)
    self.screen_dialog_action_area_confirm_button_hbox.show()
    self.screen_dialog_action_area_confirm_button.add(self.screen_dialog_action_area_confirm_button_hbox)
    self.screen_dialog_action_area_confirm_button.connect("button-press-event",self.apply_settings)
    self.screen_dialog_action_area_confirm_button.show()
    
    self.screen_dialog_action_area_toolbar.append_space()
    self.screen_dialog_action_area_toolbar.append_widget(self.screen_dialog_action_area_cancel_button,tooltip_text="Cancel the screen operation.", tooltip_private_text="")
    self.screen_dialog_action_area_toolbar.append_space()
    self.screen_dialog_action_area_toolbar.append_widget(self.screen_dialog_action_area_preview_button,tooltip_text="Preview of the result.", tooltip_private_text="")
    self.screen_dialog_action_area_toolbar.append_space()
    self.screen_dialog_action_area_toolbar.append_widget(self.screen_dialog_action_area_confirm_button,tooltip_text="Apply screen operation and save result image.", tooltip_private_text="")
    self.screen_dialog_action_area_toolbar.append_space()
    self.screen_dialog_action_area_toolbar.show()
    
    self.screen_dialog_action_area_frame.add(self.screen_dialog_action_area_toolbar)
    self.screen_dialog_action_area_frame.show()
    
    self.screen_dialog_action_hbox.pack_start(self.screen_dialog_action_area_frame,False,True,5)
    self.screen_dialog_action_hbox.show()
    
    self.screen_main_area_vbox.pack_start(self.screen_dialog_action_hbox,False,False,5)
    self.screen_main_area_vbox.show()
    
    self.screen_dialog.add(self.screen_main_area_vbox)
    
    self.screen_dialog.show()
    
    gtk.main()
    
    img1,img1_format,img2,img2_format,res=self.image1_filepath,self.image1_format_str,self.image2_filepath,self.image2_format_str,(self.result_image_filepath,self.result_image_format,self.result_image_size)
    return img1,img1_format,img2,img2_format,res
    
  def cancel(self,widget,event) :
    closed(self.screen_dialog,False)
  
  def preview(self,widget,event) :
    if self.image1_filepath and  self.image2_filepath and self.size[0] and self.size[1] :
      screen_image1_instance=Image.open(self.image1_filepath)
      screen_image2_instance=Image.open(self.image2_filepath)
      mode=screen_image1_instance.mode
      if screen_image1_instance.mode != screen_image2_instance.mode :
	
	if screen_image1_instance.mode == "RGB" or screen_image1_instance.mode == "P" :
	  format_str=screen_image2_instance.format
	  screen_image2_instance=screen_image2_instance.convert(screen_image1_instance.mode)
	  screen_image2_instance.save("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	  screen_image2_instance=Image.open("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	  mode=screen_image1_instance.mode 
	
	elif screen_image2_instance.mode == "RGB" or screen_image2_instance.mode == "P" :
	  format_str=screen_image1_instance.format
	  screen_image1_instance=screen_image1_instance.convert(screen_image2_instance.mode)
	  screen_image1_instance.save("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	  screen_image1_instance=Image.open("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	  mode=screen_image2_instance.mode
	  
	else :
	  try :
	    screen_image1_instance=screen_image1_instance.convert("RGB")
	    screen_image1_instance.save("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	    screen_image1_instance=Image.open("/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower()))
	    
	    screen_image2_instance=screen_image2_instance.convert("RGB")
	    screen_image2_instance.save("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	    screen_image2_instance=Image.open("/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower()))
	    
	    mode=screen_image1_instance.mode 
	    
	  except :
	    error_file_mergin_message(self.image1_filepath,self.image2_filepath)
	    return 
      
      if screen_image1_instance.size != self.size :
        format_str=screen_image1_instance.format
        screen_image1_instance=screen_image1_instance.resize(self.size)
        screen_image1_path="/tmp/PyImaging/pyimage_screen_image1.{0}".format(format_str.lower())
        screen_image1_instance.save(screen_image1_path,format=format_str,mode=mode)
       
      else :
	screen_image1_path=self.image1_filepath   
       
      if screen_image2_instance.size != self.size :
        format_str=screen_image2_instance.format
        screen_image2_instance=screen_image2_instance.resize(self.size)
        screen_image2_path="/tmp/PyImaging/pyimage_screen_image2.{0}".format(format_str.lower())
        screen_image2_instance.save(screen_image2_path,format=format_str,mode=mode)
        
      else :
	screen_image2_path=self.image2_filepath     
      
        
  
      screen_image1_instance=Image.open(screen_image1_path)
      screen_image2_instance=Image.open(screen_image2_path)  
      
      try :
        screen_output_image_instance=ImageChops.screen(screen_image1_instance, screen_image2_instance)
        screen_output_image_instance.show(title="Screen preview")
      except :
	error_file_mergin_message(self.image1_filepath,self.image2_filepath)
	return   
      
      
      
  
  def apply_settings(self,widget,event) :
    global img1,img2,res
    img1,img1_format,img2,img2_format,res=self.image1_filepath,self.image1_format_str,self.image2_filepath,self.image2_format_str,(self.result_image_filepath,self.result_image_format,self.result_image_size)
    
    closed(self.screen_dialog,False)
    
    
def closed(widget,event) :
  widget.destroy() # Destroy the widget.
  
  gtk.main_quit()  # Leave his mainloop.



