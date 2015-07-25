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

class Color_matrix_dialog() :
  def __init__(self) :
    
    self.red_red=100.0
    self.red_green=0.0
    self.red_blue=0.0
    
    self.green_red=0.0
    self.green_green=100.0
    self.green_blue=0.0
    
    self.blue_red=0.0
    self.blue_green=0.0
    self.blue_blue=100.0
    
    self.alpha=100.0
    
  def get_reds_value(self,widget) :
    if widget.get_name() == 'red red' :
      self.red_red=widget.get_value()
    elif widget.get_name() == 'red green' :
      self.red_green=widget.get_value() 
    elif widget.get_name() == 'red blue' :
      self.red_blue=widget.get_value()  
    
  def get_greens_value(self,widget) :
    if widget.get_name() == 'green red' :
      self.green_red=widget.get_value()
    elif widget.get_name() == 'green green' :
      self.green_green=widget.get_value() 
    elif widget.get_name() == 'green blue' :
      self.green_blue=widget.get_value()  
    
  def get_blues_value(self,widget) :
    if widget.get_name() == 'blue red' :
      self.blue_red=widget.get_value()
    elif widget.get_name() == 'blue green' :
      self.blue_green=widget.get_value() 
    elif widget.get_name() == 'blue blue' :
      self.blue_blue=widget.get_value()       
  
  def get_alpha(self,widget) :
    self.alpha=widget.get_value()
  
  def create_dialog(self) :
    global red,green,blue,alpha
    
    red,green,blue,alpha=False,False,False,False
    
    self.color_matrix_dialog=gtk.Dialog("Colors scaling matrix editor.",None,0, None)
    
    self.color_matrix_dialog.connect("delete_event",closed)
    self.color_matrix_dialog.set_size_request(512-40,512-128-32)
    self.color_matrix_dialog.modify_bg(gtk.STATE_NORMAL,self.color_matrix_dialog.get_colormap().alloc_color('#d0d0d0'))
    
    self.color_matrix_area_vbox=self.color_matrix_dialog.get_content_area()
    
    self.color_matrix_frame=gtk.Frame()
    self.color_matrix_frame.set_border_width(5)
    self.color_matrix_frame_title_button=gtk.Button()
    self.color_matrix_frame_title_button_label=gtk.Label("  Colors scaling matrix")
    self.color_matrix_frame_title_button_label.show()
    self.color_matrix_frame_title_button.set_can_focus(False)
    self.color_matrix_frame_title_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,2)
    self.color_matrix_frame_title_button_image.show()
    
    self.color_matrix_frame_title_button_hbox=gtk.HBox()
    self.color_matrix_frame_title_button_hbox.pack_start(self.color_matrix_frame_title_button_image,False,False,0)
    self.color_matrix_frame_title_button_hbox.pack_start(self.color_matrix_frame_title_button_label,False,False,0)
    self.color_matrix_frame_title_button_hbox.show()
    self.color_matrix_frame_title_button.add(self.color_matrix_frame_title_button_hbox)
    self.color_matrix_frame_title_button.set_relief(gtk.RELIEF_NONE)
    self.color_matrix_frame_title_button.show()
    self.color_matrix_frame.set_label_widget(self.color_matrix_frame_title_button)
    
    
    self.color_matrix_table=gtk.Table(rows=7,columns=9,homogeneous=False)
    self.color_matrix_table.set_border_width(5)
    
    self.rows_0_separator_0=gtk.HSeparator()
    self.rows_0_separator_0.set_size_request(44,2)
    self.rows_0_separator_0.show()
    
    self.rows_0_separator_1=gtk.HSeparator()
    self.rows_0_separator_1.set_size_request(112,2)
    self.rows_0_separator_1.show()
    
    self.rows_0_separator_2=gtk.HSeparator()
    self.rows_0_separator_2.set_size_request(112,2)
    self.rows_0_separator_2.show()
    
    self.rows_0_separator_3=gtk.HSeparator()
    self.rows_0_separator_3.set_size_request(112,2)
    self.rows_0_separator_3.show()
    
    self.rows_0_separator_4=gtk.HSeparator()
    self.rows_0_separator_4.set_size_request(112,2)
    self.rows_0_separator_4.show()
    
    
    self.color_matrix_red_title_button_event_box=gtk.EventBox()
    self.color_matrix_red_title_button_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_red_title_button_event_box.get_colormap().alloc_color('#ff0000'))
    self.color_matrix_red_title_button_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_red_title_button_event_box.get_colormap().alloc_color('#ff0000'))
    
    self.color_matrix_red_title_label=gtk.Label("R")
    self.color_matrix_red_title_label.show()
    
    self.color_matrix_red_title_button_event_box.add(self.color_matrix_red_title_label)
    self.color_matrix_red_title_button_event_box.show()
    
    self.color_matrix_red_title_button=gtk.Button(None)
    self.color_matrix_red_title_button.set_can_focus(False)
    self.color_matrix_red_title_button.set_tooltip_text("Configure the red value from the pixels")
    self.color_matrix_red_title_button.set_size_request(44,38)
    
    self.color_matrix_red_column_separator_0=gtk.VSeparator()
    self.color_matrix_red_column_separator_0.show()
    
    self.color_matrix_red_title_button.add(self.color_matrix_red_title_button_event_box)
    
    self.color_matrix_red_title_button.show()
    
    self.color_matrix_red_red_container=gtk.HBox(False,0)
    
    self.color_matrix_red_red_label=gtk.Label("R")
    self.color_matrix_red_red_label.show()
    
    self.color_matrix_red_red_title_event_box=gtk.EventBox()
    self.color_matrix_red_red_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_red_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    self.color_matrix_red_red_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_red_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    
    self.color_matrix_red_red_title_event_box.add(self.color_matrix_red_red_label)
    self.color_matrix_red_red_title_event_box.show()
    
    self.color_matrix_red_red_title_button=gtk.Button(None)
    self.color_matrix_red_red_title_button.set_can_focus(False)
    self.color_matrix_red_red_title_button.set_size_request(44,38)
    self.color_matrix_red_red_title_button.add(self.color_matrix_red_red_title_event_box)
    self.color_matrix_red_red_title_button.show()
    
    
    self.color_matrix_red_column_separator_1=gtk.VSeparator()
    self.color_matrix_red_column_separator_1.show()
    
    self.color_matrix_red_red_spinner_adjustment=gtk.Adjustment(value=100.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_red_red_spinner=gtk.SpinButton(self.color_matrix_red_red_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_red_red_spinner.set_size_request(64+16,34)
    self.color_matrix_red_red_spinner.set_tooltip_text("Set the red color percent to compute the red pixel color component for every pixel.")
    self.color_matrix_red_red_spinner.set_name('red red')
    self.color_matrix_red_red_spinner.connect("value-changed",self.get_reds_value)
    self.color_matrix_red_red_spinner.show()
    
    self.color_matrix_red_red_container.pack_start(self.color_matrix_red_red_title_button,False,False)
    self.color_matrix_red_red_container.pack_start(self.color_matrix_red_red_spinner,False,False)
    self.color_matrix_red_red_container.show()
    
    
    self.color_matrix_red_green_container=gtk.HBox(False,0)
    
    self.color_matrix_red_green_label=gtk.Label("G")
    self.color_matrix_red_green_label.show()
    
    self.color_matrix_red_green_title_event_box=gtk.EventBox()
    self.color_matrix_red_green_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_red_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    self.color_matrix_red_green_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_red_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    
    self.color_matrix_red_green_title_event_box.add(self.color_matrix_red_green_label)
    self.color_matrix_red_green_title_event_box.show()
    
    self.color_matrix_red_green_title_button=gtk.Button(None)
    self.color_matrix_red_green_title_button.set_can_focus(False)
    self.color_matrix_red_green_title_button.set_size_request(44,38)
    self.color_matrix_red_green_title_button.add(self.color_matrix_red_green_title_event_box)
    self.color_matrix_red_green_title_button.show()
    
    
    self.color_matrix_red_column_separator_2=gtk.VSeparator()
    self.color_matrix_red_column_separator_2.show()
    
    
    self.color_matrix_red_green_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_red_green_spinner=gtk.SpinButton(self.color_matrix_red_green_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_red_green_spinner.set_size_request(64+16,34)
    self.color_matrix_red_green_spinner.set_tooltip_text("Set the green color percent to compute the red pixel color component for every pixel.")
    self.color_matrix_red_green_spinner.set_name('red green')
    self.color_matrix_red_green_spinner.connect("value-changed",self.get_reds_value)
    self.color_matrix_red_green_spinner.show()
    
    self.color_matrix_red_green_container.pack_start(self.color_matrix_red_green_title_button,False,False)
    self.color_matrix_red_green_container.pack_start(self.color_matrix_red_green_spinner,False,False)
    self.color_matrix_red_green_container.show()
    
    
    
    self.color_matrix_red_blue_container=gtk.HBox(False,0)
    
    self.color_matrix_red_blue_label=gtk.Label("B")
    self.color_matrix_red_blue_label.show()
    
    self.color_matrix_red_blue_title_event_box=gtk.EventBox()
    self.color_matrix_red_blue_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_red_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    self.color_matrix_red_blue_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_red_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    
    self.color_matrix_red_blue_title_event_box.add(self.color_matrix_red_blue_label)
    self.color_matrix_red_blue_title_event_box.show()
    
    self.color_matrix_red_blue_title_button=gtk.Button(None)
    self.color_matrix_red_blue_title_button.set_can_focus(False)
    self.color_matrix_red_blue_title_button.set_size_request(44,38)
    self.color_matrix_red_blue_title_button.add(self.color_matrix_red_blue_title_event_box)
    self.color_matrix_red_blue_title_button.show()
    
    
    self.color_matrix_red_column_separator_3=gtk.VSeparator()
    self.color_matrix_red_column_separator_3.show()
    
    
    self.color_matrix_red_blue_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_red_blue_spinner=gtk.SpinButton(self.color_matrix_red_blue_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_red_blue_spinner.set_size_request(64+16,34)
    self.color_matrix_red_blue_spinner.set_tooltip_text("Set the blue color percent to compute the red pixel color component for every pixel.")
    self.color_matrix_red_blue_spinner.set_name('red blue')
    self.color_matrix_red_blue_spinner.connect("value-changed",self.get_reds_value)
    self.color_matrix_red_blue_spinner.show()
    
    self.color_matrix_red_blue_container.pack_start(self.color_matrix_red_blue_title_button,False,False)
    self.color_matrix_red_blue_container.pack_start(self.color_matrix_red_blue_spinner,False,False)
    self.color_matrix_red_blue_container.show()
    
    self.color_matrix_red_column_separator_4=gtk.VSeparator()
    self.color_matrix_red_column_separator_4.show()
    
    self.rows_1_separator_0=gtk.HSeparator()
    self.rows_1_separator_0.set_size_request(44,2)
    self.rows_1_separator_0.show()
    
    self.rows_1_separator_1=gtk.HSeparator()
    self.rows_1_separator_1.set_size_request(112,2)
    self.rows_1_separator_1.show()
    
    self.rows_1_separator_2=gtk.HSeparator()
    self.rows_1_separator_2.set_size_request(112,2)
    self.rows_1_separator_2.show()
    
    self.rows_1_separator_3=gtk.HSeparator()
    self.rows_1_separator_3.set_size_request(112,2)
    self.rows_1_separator_3.show()
    
    self.rows_1_separator_4=gtk.HSeparator()
    self.rows_1_separator_4.set_size_request(112,2)
    self.rows_1_separator_4.show()
    
    
    
    self.color_matrix_green_title_button_event_box=gtk.EventBox()
    self.color_matrix_green_title_button_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_green_title_button_event_box.get_colormap().alloc_color('#00ff00'))
    self.color_matrix_green_title_button_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_green_title_button_event_box.get_colormap().alloc_color('#00ff00'))
    
    self.color_matrix_green_title_label=gtk.Label("G")
    self.color_matrix_green_title_label.show()
    
    self.color_matrix_green_title_button_event_box.add(self.color_matrix_green_title_label)
    self.color_matrix_green_title_button_event_box.show()
    
    self.color_matrix_green_title_button=gtk.Button(None)
    self.color_matrix_green_title_button.set_can_focus(False)
    self.color_matrix_green_title_button.set_tooltip_text("Configure the green value from the pixels")
    self.color_matrix_green_title_button.set_size_request(44,38)
    
    self.color_matrix_green_column_separator_0=gtk.VSeparator()
    self.color_matrix_green_column_separator_0.show()
    
    self.color_matrix_green_title_button.add(self.color_matrix_green_title_button_event_box)
    
    self.color_matrix_green_title_button.show()
    
    self.color_matrix_green_red_container=gtk.HBox(False,0)
    
    self.color_matrix_green_red_label=gtk.Label("R")
    self.color_matrix_green_red_label.show()
    
    self.color_matrix_green_red_title_event_box=gtk.EventBox()
    self.color_matrix_green_red_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_green_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    self.color_matrix_green_red_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_green_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    
    self.color_matrix_green_red_title_event_box.add(self.color_matrix_green_red_label)
    self.color_matrix_green_red_title_event_box.show()
    
    self.color_matrix_green_red_title_button=gtk.Button(None)
    self.color_matrix_green_red_title_button.set_can_focus(False)
    self.color_matrix_green_red_title_button.set_size_request(44,38)
    self.color_matrix_green_red_title_button.add(self.color_matrix_green_red_title_event_box)
    self.color_matrix_green_red_title_button.show()
    
    
    self.color_matrix_green_column_separator_1=gtk.VSeparator()
    self.color_matrix_green_column_separator_1.show()
    
    self.color_matrix_green_red_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_green_red_spinner=gtk.SpinButton(self.color_matrix_green_red_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_green_red_spinner.set_size_request(64+16,34)
    self.color_matrix_green_red_spinner.set_tooltip_text("Set the red color percent to compute the green pixel color component for every pixel.")
    self.color_matrix_green_red_spinner.set_name('green red')
    self.color_matrix_green_red_spinner.connect("value-changed",self.get_greens_value)
    self.color_matrix_green_red_spinner.show()
    
    self.color_matrix_green_red_container.pack_start(self.color_matrix_green_red_title_button,False,False)
    self.color_matrix_green_red_container.pack_start(self.color_matrix_green_red_spinner,False,False)
    self.color_matrix_green_red_container.show()
    
    
    self.color_matrix_green_green_container=gtk.HBox(False,0)
    
    self.color_matrix_green_green_label=gtk.Label("G")
    self.color_matrix_green_green_label.show()
    
    self.color_matrix_green_green_title_event_box=gtk.EventBox()
    self.color_matrix_green_green_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_green_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    self.color_matrix_green_green_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_green_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    
    self.color_matrix_green_green_title_event_box.add(self.color_matrix_green_green_label)
    self.color_matrix_green_green_title_event_box.show()
    
    self.color_matrix_green_green_title_button=gtk.Button(None)
    self.color_matrix_green_green_title_button.set_can_focus(False)
    self.color_matrix_green_green_title_button.set_size_request(44,38)
    self.color_matrix_green_green_title_button.add(self.color_matrix_green_green_title_event_box)
    self.color_matrix_green_green_title_button.show()
    
    
    self.color_matrix_green_column_separator_2=gtk.VSeparator()
    self.color_matrix_green_column_separator_2.show()
     
    self.color_matrix_green_green_spinner_adjustment=gtk.Adjustment(value=100.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_green_green_spinner=gtk.SpinButton(self.color_matrix_green_green_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_green_green_spinner.set_size_request(64+16,34)
    self.color_matrix_green_green_spinner.set_tooltip_text("Set the green color percent to compute the green pixel color component for every pixel.")
    self.color_matrix_green_green_spinner.set_name('green green')
    self.color_matrix_green_green_spinner.connect("value-changed",self.get_greens_value)
    self.color_matrix_green_green_spinner.show()
    
    self.color_matrix_green_green_container.pack_start(self.color_matrix_green_green_title_button,False,False)
    self.color_matrix_green_green_container.pack_start(self.color_matrix_green_green_spinner,False,False)
    self.color_matrix_green_green_container.show()
    
    
    
    self.color_matrix_green_blue_container=gtk.HBox(False,0)
    
    self.color_matrix_green_blue_label=gtk.Label("B")
    self.color_matrix_green_blue_label.show()
    
    self.color_matrix_green_blue_title_event_box=gtk.EventBox()
    self.color_matrix_green_blue_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_green_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    self.color_matrix_green_blue_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_green_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    
    self.color_matrix_green_blue_title_event_box.add(self.color_matrix_green_blue_label)
    self.color_matrix_green_blue_title_event_box.show()
    
    self.color_matrix_green_blue_title_button=gtk.Button(None)
    self.color_matrix_green_blue_title_button.set_can_focus(False)
    self.color_matrix_green_blue_title_button.set_size_request(44,38)
    self.color_matrix_green_blue_title_button.add(self.color_matrix_green_blue_title_event_box)
    self.color_matrix_green_blue_title_button.show()
    
    
    self.color_matrix_green_column_separator_3=gtk.VSeparator()
    self.color_matrix_green_column_separator_3.show()
   
    
    self.color_matrix_green_blue_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_green_blue_spinner=gtk.SpinButton(self.color_matrix_green_blue_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_green_blue_spinner.set_size_request(64+16,34)
    self.color_matrix_green_blue_spinner.set_tooltip_text("Set the blue color percent to compute the green pixel color component for every pixel.")
    self.color_matrix_green_blue_spinner.set_name('green blue')
    self.color_matrix_green_blue_spinner.connect("value-changed",self.get_greens_value)
    self.color_matrix_green_blue_spinner.show()
    
    self.color_matrix_green_blue_container.pack_start(self.color_matrix_green_blue_title_button,False,False)
    self.color_matrix_green_blue_container.pack_start(self.color_matrix_green_blue_spinner,False,False)
    self.color_matrix_green_blue_container.show()
    
    self.color_matrix_green_column_separator_4=gtk.VSeparator()
    self.color_matrix_green_column_separator_4.show()
    
    
    self.rows_2_separator_0=gtk.HSeparator()
    self.rows_2_separator_0.set_size_request(44,2)
    self.rows_2_separator_0.show()
    
    self.rows_2_separator_1=gtk.HSeparator()
    self.rows_2_separator_1.set_size_request(112,2)
    self.rows_2_separator_1.show()
    
    self.rows_2_separator_2=gtk.HSeparator()
    self.rows_2_separator_2.set_size_request(112,2)
    self.rows_2_separator_2.show()
    
    self.rows_2_separator_3=gtk.HSeparator()
    self.rows_2_separator_3.set_size_request(112,2)
    self.rows_2_separator_3.show()
    
    self.rows_2_separator_4=gtk.HSeparator()
    self.rows_2_separator_4.set_size_request(112,2)
    self.rows_2_separator_4.show()
    
    
    
    self.color_matrix_blue_title_button_event_box=gtk.EventBox()
    self.color_matrix_blue_title_button_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_blue_title_button_event_box.get_colormap().alloc_color('#0000ff'))
    self.color_matrix_blue_title_button_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_blue_title_button_event_box.get_colormap().alloc_color('#0000ff'))
    
    self.color_matrix_blue_title_label=gtk.Label("B")
    self.color_matrix_blue_title_label.show()
    
    self.color_matrix_blue_title_button_event_box.add(self.color_matrix_blue_title_label)
    self.color_matrix_blue_title_button_event_box.show()
    
    self.color_matrix_blue_title_button=gtk.Button(None)
    self.color_matrix_blue_title_button.set_can_focus(False)
    self.color_matrix_blue_title_button.set_tooltip_text("Configure the blue value from the pixels")
    self.color_matrix_blue_title_button.set_size_request(44,38)
    
    self.color_matrix_blue_column_separator_0=gtk.VSeparator()
    self.color_matrix_blue_column_separator_0.show()
    
    self.color_matrix_blue_title_button.add(self.color_matrix_blue_title_button_event_box)
    
    self.color_matrix_blue_title_button.show()
    
    self.color_matrix_blue_red_container=gtk.HBox(False,0)
    
    self.color_matrix_blue_red_label=gtk.Label("R")
    self.color_matrix_blue_red_label.show()
    
    self.color_matrix_blue_red_title_event_box=gtk.EventBox()
    self.color_matrix_blue_red_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_blue_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    self.color_matrix_blue_red_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_blue_red_title_event_box.get_colormap().alloc_color('#ff0000'))
    
    self.color_matrix_blue_red_title_event_box.add(self.color_matrix_blue_red_label)
    self.color_matrix_blue_red_title_event_box.show()
    
    self.color_matrix_blue_red_title_button=gtk.Button(None)
    self.color_matrix_blue_red_title_button.set_can_focus(False)
    self.color_matrix_blue_red_title_button.set_size_request(44,38)
    self.color_matrix_blue_red_title_button.add(self.color_matrix_blue_red_title_event_box)
    self.color_matrix_blue_red_title_button.show()
    
    
    self.color_matrix_blue_column_separator_1=gtk.VSeparator()
    self.color_matrix_blue_column_separator_1.show()
     
    self.color_matrix_blue_red_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_blue_red_spinner=gtk.SpinButton(self.color_matrix_blue_red_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_blue_red_spinner.set_size_request(64+16,34)
    self.color_matrix_blue_red_spinner.set_tooltip_text("Set the red color percent to compute the blue pixel color component for every pixel.")
    self.color_matrix_blue_red_spinner.set_name('blue red')
    self.color_matrix_blue_red_spinner.connect("value-changed",self.get_blues_value)
    self.color_matrix_blue_red_spinner.show()
    
    self.color_matrix_blue_red_container.pack_start(self.color_matrix_blue_red_title_button,False,False)
    self.color_matrix_blue_red_container.pack_start(self.color_matrix_blue_red_spinner,False,False)
    self.color_matrix_blue_red_container.show()
    
    
    self.color_matrix_blue_green_container=gtk.HBox(False,0)
    
    self.color_matrix_blue_green_label=gtk.Label("G")
    self.color_matrix_blue_green_label.show()
    
    self.color_matrix_blue_green_title_event_box=gtk.EventBox()
    self.color_matrix_blue_green_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_blue_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    self.color_matrix_blue_green_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_blue_green_title_event_box.get_colormap().alloc_color('#00ff00'))
    
    self.color_matrix_blue_green_title_event_box.add(self.color_matrix_blue_green_label)
    self.color_matrix_blue_green_title_event_box.show()
    
    self.color_matrix_blue_green_title_button=gtk.Button(None)
    self.color_matrix_blue_green_title_button.set_can_focus(False)
    self.color_matrix_blue_green_title_button.set_size_request(44,38)
    self.color_matrix_blue_green_title_button.add(self.color_matrix_blue_green_title_event_box)
    self.color_matrix_blue_green_title_button.show()
    
    
    self.color_matrix_blue_column_separator_2=gtk.VSeparator()
    self.color_matrix_blue_column_separator_2.show()
     
    self.color_matrix_blue_green_spinner_adjustment=gtk.Adjustment(value=0.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_blue_green_spinner=gtk.SpinButton(self.color_matrix_blue_green_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_blue_green_spinner.set_size_request(64+16,34)
    self.color_matrix_blue_green_spinner.set_tooltip_text("Set the green color percent to compute the blue pixel color component for every pixel.")
    self.color_matrix_blue_green_spinner.set_name('blue green')
    self.color_matrix_blue_green_spinner.connect("value-changed",self.get_blues_value)
    self.color_matrix_blue_green_spinner.show()
    
    self.color_matrix_blue_green_container.pack_start(self.color_matrix_blue_green_title_button,False,False)
    self.color_matrix_blue_green_container.pack_start(self.color_matrix_blue_green_spinner,False,False)
    self.color_matrix_blue_green_container.show()
    
    
    
    self.color_matrix_blue_blue_container=gtk.HBox(False,0)
    
    self.color_matrix_blue_blue_label=gtk.Label("B")
    self.color_matrix_blue_blue_label.show()
    
    self.color_matrix_blue_blue_title_event_box=gtk.EventBox()
    self.color_matrix_blue_blue_title_event_box.modify_bg(gtk.STATE_NORMAL,self.color_matrix_blue_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    self.color_matrix_blue_blue_title_event_box.modify_bg(gtk.STATE_PRELIGHT,self.color_matrix_blue_blue_title_event_box.get_colormap().alloc_color('#0000ff'))
    
    self.color_matrix_blue_blue_title_event_box.add(self.color_matrix_blue_blue_label)
    self.color_matrix_blue_blue_title_event_box.show()
    
    self.color_matrix_blue_blue_title_button=gtk.Button(None)
    self.color_matrix_blue_blue_title_button.set_can_focus(False)
    self.color_matrix_blue_blue_title_button.set_size_request(44,38)
    self.color_matrix_blue_blue_title_button.add(self.color_matrix_blue_blue_title_event_box)
    self.color_matrix_blue_blue_title_button.show()
    
    
    self.color_matrix_blue_column_separator_3=gtk.VSeparator()
    self.color_matrix_blue_column_separator_3.show()
    
    self.color_matrix_blue_blue_spinner_adjustment=gtk.Adjustment(value=100.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_blue_blue_spinner=gtk.SpinButton(self.color_matrix_blue_blue_spinner_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_blue_blue_spinner.set_size_request(64+16,34)
    self.color_matrix_blue_blue_spinner.set_tooltip_text("Set the blue color percent to compute the blue pixel color component for every pixel.")
    self.color_matrix_blue_blue_spinner.set_name('blue green')
    self.color_matrix_blue_blue_spinner.connect("value-changed",self.get_blues_value)
    self.color_matrix_blue_blue_spinner.show()
    
    self.color_matrix_blue_blue_container.pack_start(self.color_matrix_blue_blue_title_button,False,False)
    self.color_matrix_blue_blue_container.pack_start(self.color_matrix_blue_blue_spinner,False,False)
    self.color_matrix_blue_blue_container.show()
    
    self.color_matrix_blue_column_separator_4=gtk.VSeparator()
    self.color_matrix_blue_column_separator_4.show()
    
    self.rows_3_separator_0=gtk.HSeparator()
    self.rows_3_separator_0.set_size_request(44,2)
    self.rows_3_separator_0.show()
    
    self.rows_3_separator_1=gtk.HSeparator()
    self.rows_3_separator_1.set_size_request(112,2)
    self.rows_3_separator_1.show()
    
    self.rows_3_separator_2=gtk.HSeparator()
    self.rows_3_separator_2.set_size_request(112,2)
    self.rows_3_separator_2.show()
    
    self.rows_3_separator_3=gtk.HSeparator()
    self.rows_3_separator_3.set_size_request(112,2)
    self.rows_3_separator_3.show()
    
    self.rows_3_separator_4=gtk.HSeparator()
    self.rows_3_separator_4.set_size_request(112,2)
    self.rows_3_separator_4.show()
    
    self.color_matrix_table.attach(self.rows_0_separator_0, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_0_separator_1, left_attach=3, right_attach=4, top_attach=0, bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_0_separator_2, left_attach=5, right_attach=6, top_attach=0, bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_0_separator_3, left_attach=7, right_attach=8, top_attach=0, bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.color_matrix_red_column_separator_0,left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_title_button, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_column_separator_1,left_attach=2, right_attach=3, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_red_container, left_attach=3, right_attach=4, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_column_separator_2,left_attach=4, right_attach=5, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_green_container, left_attach=5, right_attach=6, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_column_separator_3,left_attach=6, right_attach=7, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_blue_container, left_attach=7, right_attach=8, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_red_column_separator_4,left_attach=8, right_attach=9, top_attach=1, bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.rows_1_separator_0, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_1_separator_1, left_attach=3, right_attach=4, top_attach=2, bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_1_separator_2, left_attach=5, right_attach=6, top_attach=2, bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_1_separator_3, left_attach=7, right_attach=8, top_attach=2, bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.color_matrix_green_column_separator_0,left_attach=0, right_attach=1, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_title_button, left_attach=1, right_attach=2, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_column_separator_1,left_attach=2, right_attach=3, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_red_container, left_attach=3, right_attach=4, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_column_separator_2,left_attach=4, right_attach=5, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_green_container, left_attach=5, right_attach=6, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_column_separator_3,left_attach=6, right_attach=7, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_blue_container, left_attach=7, right_attach=8, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_green_column_separator_4,left_attach=8, right_attach=9, top_attach=3, bottom_attach=4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.rows_2_separator_0, left_attach=1, right_attach=2, top_attach=4, bottom_attach=5, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_2_separator_1, left_attach=3, right_attach=4, top_attach=4, bottom_attach=5, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_2_separator_2, left_attach=5, right_attach=6, top_attach=4, bottom_attach=5, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_2_separator_3, left_attach=7, right_attach=8, top_attach=4, bottom_attach=5, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.color_matrix_blue_column_separator_0,left_attach=0, right_attach=1, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_title_button, left_attach=1, right_attach=2, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_column_separator_1,left_attach=2, right_attach=3, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_red_container, left_attach=3, right_attach=4, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_column_separator_2,left_attach=4, right_attach=5, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_green_container, left_attach=5, right_attach=6, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_column_separator_3,left_attach=6, right_attach=7, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_blue_container, left_attach=7, right_attach=8, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.color_matrix_blue_column_separator_4,left_attach=8, right_attach=9, top_attach=5, bottom_attach=6, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table.attach(self.rows_3_separator_0, left_attach=1, right_attach=2, top_attach=6, bottom_attach=7, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_3_separator_1, left_attach=3, right_attach=4, top_attach=6, bottom_attach=7, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_3_separator_2, left_attach=5, right_attach=6, top_attach=6, bottom_attach=7, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table.attach(self.rows_3_separator_3, left_attach=7, right_attach=8, top_attach=6, bottom_attach=7, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    

    
    self.color_matrix_table.show()
    
    self.color_matrix_table_buttons=gtk.Table(rows=3,columns=7,homogeneous=False)
    self.color_matrix_table_buttons.set_border_width(5)
    
    self.rows_4_separator_0=gtk.HSeparator()
    self.rows_4_separator_0.set_size_request(44,2)
    self.rows_4_separator_0.show()
    
    self.rows_4_separator_1=gtk.HSeparator()
    self.rows_4_separator_1.set_size_request(112,2)
    self.rows_4_separator_1.show()
    
    self.rows_4_separator_2=gtk.HSeparator()
    self.rows_4_separator_2.set_size_request(109,2)
    self.rows_4_separator_2.show()
    
    
    self.color_matrix_buttons_separator_0=gtk.VSeparator()
    self.color_matrix_buttons_separator_0.show()
    
    self.color_matrix_apply_button=gtk.Button()
    self.color_matrix_apply_button_label=gtk.Label(" Apply multiply matrix")
    self.color_matrix_apply_button_label.show()
    self.color_matrix_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_APPLY,1)
    self.color_matrix_apply_button_image.show()
    self.color_matrix_apply_button_hbox=gtk.HBox()
    self.color_matrix_apply_button_hbox.pack_start(self.color_matrix_apply_button_image,False,False,0)
    self.color_matrix_apply_button_hbox.pack_start(self.color_matrix_apply_button_label,False,False,0)
    self.color_matrix_apply_button_hbox.show()
    self.color_matrix_apply_button.add(self.color_matrix_apply_button_hbox)
    self.color_matrix_apply_button.connect("button-press-event",self.apply_matrix)
    self.color_matrix_apply_button.show()
    
    self.color_matrix_buttons_separator_1=gtk.VSeparator()
    self.color_matrix_buttons_separator_1.show()
    
    self.color_matrix_reset_button=gtk.Button()
    self.color_matrix_reset_button_label=gtk.Label(" Reset matrix  ")
    self.color_matrix_reset_button_label.show()
    self.color_matrix_reset_button_image=gtk.image_new_from_stock(gtk.STOCK_REFRESH,1)
    self.color_matrix_reset_button_image.show()
    self.color_matrix_reset_button_hbox=gtk.HBox()
    self.color_matrix_reset_button_hbox.pack_start(self.color_matrix_reset_button_image,False,False)
    self.color_matrix_reset_button_hbox.pack_start(self.color_matrix_reset_button_label,False,False)
    self.color_matrix_reset_button_hbox.show()
    self.color_matrix_reset_button.add(self.color_matrix_reset_button_hbox)
    self.color_matrix_reset_button.connect("button-press-event",self.reset_matrix)
    self.color_matrix_reset_button.show()
    
    self.color_matrix_buttons_separator_2=gtk.VSeparator()
    self.color_matrix_buttons_separator_2.show()
    
    self.color_matrix_alpha_container=gtk.HBox(False,0)
    
    
    self.color_matrix_alpha_button=gtk.Button("Alpha")
    self.color_matrix_alpha_button.set_can_focus(False)
    self.color_matrix_alpha_button.show()
    
    self.color_matrix_alpha_adjustment=gtk.Adjustment(value=100.0, lower=0.0, upper=100.0, step_incr=0.1, page_incr=0, page_size=0)
    self.color_matrix_alpha_spinner=gtk.SpinButton(self.color_matrix_alpha_adjustment,climb_rate=0.25, digits=1)
    self.color_matrix_alpha_spinner.set_size_request(58+14,34)
    self.color_matrix_alpha_spinner.set_tooltip_text("Set the alpha percent value from the alpha value (opacity) from the pixel color component.")
    self.color_matrix_alpha_spinner.connect("value-changed",self.get_alpha)
    self.color_matrix_alpha_spinner.show()
    
    self.color_matrix_alpha_container.pack_start(self.color_matrix_alpha_button,False,False,0)
    self.color_matrix_alpha_container.pack_start(self.color_matrix_alpha_spinner,False,False,0)
    self.color_matrix_alpha_container.show()
    
    self.color_matrix_buttons_separator_3=gtk.VSeparator()
    self.color_matrix_buttons_separator_3.show()
    
    self.rows_5_separator_0=gtk.HSeparator()
    self.rows_5_separator_0.set_size_request(44,2)
    self.rows_5_separator_0.show()
    
    self.rows_5_separator_1=gtk.HSeparator()
    self.rows_5_separator_1.set_size_request(112,2)
    self.rows_5_separator_1.show()
    
    self.rows_5_separator_2=gtk.HSeparator()
    self.rows_5_separator_2.set_size_request(109,2)
    self.rows_5_separator_2.show()
    
    
    
    self.color_matrix_table_buttons.attach(self.rows_4_separator_0,left_attach=1,right_attach=2,top_attach=0,bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.rows_4_separator_1,left_attach=3,right_attach=4,top_attach=0,bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.rows_4_separator_2,left_attach=5,right_attach=6,top_attach=0,bottom_attach=1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    self.color_matrix_table_buttons.attach(self.color_matrix_buttons_separator_0,left_attach=0,right_attach=1,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_apply_button,left_attach=1,right_attach=2,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_buttons_separator_1,left_attach=2,right_attach=3,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_reset_button,left_attach=3,right_attach=4,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_buttons_separator_2,left_attach=4,right_attach=5,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_alpha_container,left_attach=5,right_attach=6,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.color_matrix_buttons_separator_3,left_attach=6,right_attach=7,top_attach=1,bottom_attach=2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.show()
    
    self.color_matrix_table_buttons.attach(self.rows_5_separator_0,left_attach=1,right_attach=2,top_attach=2,bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.rows_5_separator_1,left_attach=3,right_attach=4,top_attach=2,bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    self.color_matrix_table_buttons.attach(self.rows_5_separator_2,left_attach=5,right_attach=6,top_attach=2,bottom_attach=3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=1, ypadding=1)
    
    
    self.color_matrix_main_vbox=gtk.VBox()
    
    self.color_matrix_main_vbox.pack_start(self.color_matrix_table,False,False,5)
    self.color_matrix_main_vbox.pack_start(self.color_matrix_table_buttons,False,False,5)
    self.color_matrix_main_vbox.show()
    
    
    self.color_matrix_frame.add(self.color_matrix_main_vbox)
    self.color_matrix_frame.show()
    
    self.color_matrix_area_vbox.pack_start(self.color_matrix_frame,False,False)
    
    self.color_matrix_dialog_action_frame=gtk.Frame(None)
    
    self.color_matrix_dialog_action_frame.set_border_width(5)
    self.color_matrix_dialog_action_frame_title_button=gtk.Button()
    self.color_matrix_dialog_action_frame_title_button_label=gtk.Label("  Actions color scaling matrix")
    self.color_matrix_dialog_action_frame_title_button_label.show()
    self.color_matrix_dialog_action_frame_title_button.set_can_focus(False)
    self.color_matrix_dialog_action_frame_title_button_image=gtk.image_new_from_stock(gtk.STOCK_PROPERTIES,2)
    self.color_matrix_dialog_action_frame_title_button_image.show()
    self.color_matrix_dialog_action_frame_title_button_hbox=gtk.HBox()
    self.color_matrix_dialog_action_frame_title_button_hbox.pack_start(self.color_matrix_dialog_action_frame_title_button_image,False,False,0)
    self.color_matrix_dialog_action_frame_title_button_hbox.pack_start(self.color_matrix_dialog_action_frame_title_button_label,False,False,0)
    self.color_matrix_dialog_action_frame_title_button_hbox.show()
    self.color_matrix_dialog_action_frame_title_button.add(self.color_matrix_dialog_action_frame_title_button_hbox)
    self.color_matrix_dialog_action_frame_title_button.set_relief(gtk.RELIEF_NONE)
    self.color_matrix_dialog_action_frame_title_button.show()
    self.color_matrix_dialog_action_frame.set_label_widget(self.color_matrix_dialog_action_frame_title_button)
    
    self.color_matrix_dialog_action_close_button=gtk.Button()
    self.color_matrix_dialog_action_close_button_label=gtk.Label("  Close      ")
    self.color_matrix_dialog_action_close_button_label.show()
    self.color_matrix_dialog_action_close_button_space=gtk.Label("               ")
    self.color_matrix_dialog_action_close_button_space.show()
    self.color_matrix_dialog_action_close_button.set_size_request((512-160)/2+22,32)
    self.color_matrix_dialog_action_close_button_image=gtk.image_new_from_stock(gtk.STOCK_CLOSE,2)
    self.color_matrix_dialog_action_close_button_image.show()
    self.color_matrix_dialog_action_close_button_hbox=gtk.HBox()
    self.color_matrix_dialog_action_close_button_hbox.pack_start(self.color_matrix_dialog_action_close_button_space,False,False,0)
    self.color_matrix_dialog_action_close_button_hbox.pack_start(self.color_matrix_dialog_action_close_button_image,False,False,0)
    self.color_matrix_dialog_action_close_button_hbox.pack_start(self.color_matrix_dialog_action_close_button_label,False,False,0)
    self.color_matrix_dialog_action_close_button_hbox.show()
    self.color_matrix_dialog_action_close_button.add(self.color_matrix_dialog_action_close_button_hbox)
    self.color_matrix_dialog_action_close_button.connect("button-press-event",self.close)
    self.color_matrix_dialog_action_close_button.show()
    
    self.color_matrix_dialog_action_apply_button=gtk.Button()
    self.color_matrix_dialog_action_apply_button_label=gtk.Label("  Apply      ")
    self.color_matrix_dialog_action_apply_button_label.show()
    self.color_matrix_dialog_action_apply_button_space=gtk.Label("               ")
    self.color_matrix_dialog_action_apply_button_space.show()
    self.color_matrix_dialog_action_apply_button.set_size_request((512-160)/2+22,32)
    self.color_matrix_dialog_action_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_APPLY,2)
    self.color_matrix_dialog_action_apply_button_image.show()
    self.color_matrix_dialog_action_apply_button_hbox=gtk.HBox()
    self.color_matrix_dialog_action_apply_button_hbox.pack_start(self.color_matrix_dialog_action_apply_button_space,False,False,0)
    self.color_matrix_dialog_action_apply_button_hbox.pack_start(self.color_matrix_dialog_action_apply_button_image,False,False,0)
    self.color_matrix_dialog_action_apply_button_hbox.pack_start(self.color_matrix_dialog_action_apply_button_label,False,False,0)
    self.color_matrix_dialog_action_apply_button_hbox.show()
    self.color_matrix_dialog_action_apply_button.add(self.color_matrix_dialog_action_apply_button_hbox)
    self.color_matrix_dialog_action_apply_button.connect("button-press-event",self.apply_matrix)
    self.color_matrix_dialog_action_apply_button.show()
    
    self.color_matrix_dialog_action_toolbar=gtk.Toolbar()
    self.color_matrix_dialog_action_toolbar.set_border_width(5)
    self.color_matrix_dialog_action_toolbar.set_size_request(512-70,48)
    self.color_matrix_dialog_action_toolbar.modify_bg(gtk.STATE_NORMAL,self.color_matrix_dialog_action_toolbar.get_colormap().alloc_color('#f0f0f0'))
    self.color_matrix_dialog_action_toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)
    
    self.color_matrix_dialog_action_toolbar.append_space()
    self.color_matrix_dialog_action_toolbar.append_widget(self.color_matrix_dialog_action_close_button,tooltip_text="", tooltip_private_text="")
    self.color_matrix_dialog_action_toolbar.append_space()
    self.color_matrix_dialog_action_toolbar.append_widget(self.color_matrix_dialog_action_apply_button,tooltip_text="", tooltip_private_text="")
    self.color_matrix_dialog_action_toolbar.append_space()
    
    self.color_matrix_dialog_action_toolbar.show()
    
    self.color_matrix_dialog_action_frame.add(self.color_matrix_dialog_action_toolbar)
    self.color_matrix_dialog_action_frame.show()
    
    self.color_matrix_dialog_action_hbox=self.color_matrix_dialog.get_action_area()
    
    self.color_matrix_dialog_action_hbox.pack_start(self.color_matrix_dialog_action_frame,False,False,0)
    
    
    
    self.color_matrix_dialog.set_has_separator(True)
    
    self.color_matrix_dialog.show()
    
    self.color_matrix_dialog.run()
    
    return red,green,blue,alpha
  
  def reset_matrix(self,widget,event) :
    self.red_red=100.0
    self.red_green=0.0
    self.red_blue=0.0
    
    self.green_red=0.0
    self.green_green=100.0
    self.green_blue=0.0
    
    self.blue_red=0.0
    self.blue_green=0.0
    self.blue_blue=100.0
    
    self.alpha=100.0
    
    self.color_matrix_red_red_spinner.set_value(100.0)
    self.color_matrix_red_green_spinner.set_value(0.0)
    self.color_matrix_red_blue_spinner.set_value(0.0)
    
    self.color_matrix_green_red_spinner.set_value(0.0)
    self.color_matrix_green_green_spinner.set_value(100.0)
    self.color_matrix_green_blue_spinner.set_value(0.0)
    
    self.color_matrix_blue_red_spinner.set_value(0.0)
    self.color_matrix_blue_green_spinner.set_value(0.0)
    self.color_matrix_blue_blue_spinner.set_value(100.0)
    
    self.color_matrix_alpha_spinner.set_value(100.0)
     
    
  def close(self,widget,event) :
    global red,green,blue,alpha
    red=False
    green=False
    blue=False
    alpha=False
    closed(self.color_matrix_dialog,False)
  
  def apply_matrix(self,widget,event) :
    global red,green,blue,alpha
    red=(self.red_red,self.red_green,self.red_blue)
    green=(self.green_red,self.green_green,self.green_blue)
    blue=(self.blue_red,self.blue_green,self.blue_blue)
    alpha=self.alpha
    closed(self.color_matrix_dialog,False)
    
    
    
def closed(widget,event) :
  widget.destroy() # Destroy widget.
  
  #gtk.main_quit() 

    




