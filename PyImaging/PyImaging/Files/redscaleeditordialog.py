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
  

class Redscale_dialog() :
  
  def __init__(self) :
    
    self.redscale_base_for_computing_dict={0:"average",1:"minimun",2:"maximum",3:"red",4:"green",5:"blue"}
    
    self.redscale_base_for_computing_value="average"
    
    self.get_other_colors_main_setting=2 
    
    self.get_other_color_percent_green=0
    self.get_other_color_percent_blue=0
    self.get_other_color_percent_alpha=100
    
    self.get_other_color_arbitrary_green=0
    self.get_other_color_arbitrary_blue=0
    self.get_other_color_arbitrary_alpha=255
    
  def get_base_for_redscale(self,widget) :
    self.redscale_base_for_computing_value=self.redscale_base_for_computing_dict.get(widget.get_active())
    
  def get_other_colors_choice_from_radiobutton(self,widget,event) :
    if widget.get_name() == "percent" :
      self.get_other_colors_main_setting=0
    elif widget.get_name() == "arbitrary" :
      self.get_other_colors_main_setting=1
    elif widget.get_name() == "zero" :
      self.get_other_colors_main_setting=2  
  
  def get_other_color_percent(self,widget) :
    if widget.get_name() == "percent green" :
      self.get_other_color_percent_green=widget.get_value()
    elif widget.get_name() == "percent blue" :
      self.get_other_color_percent_blue=widget.get_value()
    elif widget.get_name() == "percent alpha" :
      self.get_other_color_percent_alpha=widget.get_value()  

    
  def get_other_color_arbitrary(self,widget) :
    if widget.get_name() == "arbitrary green" :
      self.get_other_color_arbitrary_green=widget.get_value()
    elif widget.get_name() == "arbitrary blue" :
      self.get_other_color_arbitrary_blue=widget.get_value()
    elif widget.get_name() == "arbitrary alpha" :
      self.get_other_color_arbitrary_alpha=widget.get_value()  
    
  def create_dialog(self) :
    global scaling_setting, colors_setting, percent_green, percent_blue, percent_alpha, arbitrary_green, arbitrary_blue, arbitrary_alpha
    
    scaling_setting, colors_setting, percent_green, percent_blue, percent_alpha, arbitrary_green, arbitrary_blue, arbitrary_alpha=0,0,0,0,0,0,0,0
    
    self.redscale_dialog=gtk.Dialog("Red scale editor.",None,0, None)
    
    self.redscale_dialog.connect("delete_event",closed)
    self.redscale_dialog.set_size_request(512-64-24,512+24)
    self.redscale_dialog.modify_bg(gtk.STATE_NORMAL,self.redscale_dialog.get_colormap().alloc_color('#d0d0d0'))
    
    self.redscale_pixel_value_frame=gtk.Frame(None)
    self.redscale_pixel_value_frame_label_button=gtk.Button()
    self.redscale_pixel_value_frame_label_button_label=gtk.Label("Red scale settings")
    self.redscale_pixel_value_frame_label_button_label.show()
    self.redscale_pixel_value_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PREFERENCES,2)
    self.redscale_pixel_value_frame_label_button_image.show()
    self.redscale_pixel_value_frame_label_button_hbox=gtk.HBox()
    self.redscale_pixel_value_frame_label_button_hbox.pack_start(self.redscale_pixel_value_frame_label_button_image,False,False,0)
    self.redscale_pixel_value_frame_label_button_hbox.pack_start(self.redscale_pixel_value_frame_label_button_label,False,False,0)
    self.redscale_pixel_value_frame_label_button_hbox.show()
    self.redscale_pixel_value_frame_label_button.add(self.redscale_pixel_value_frame_label_button_hbox)
    self.redscale_pixel_value_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_pixel_value_frame_label_button.show()
    self.redscale_pixel_value_frame.set_label_widget(self.redscale_pixel_value_frame_label_button)
    self.redscale_pixel_value_frame.set_border_width(5)
    
    
    self.red_scale_pixel_value_toolbar=gtk.Toolbar()
    self.red_scale_pixel_value_toolbar.set_border_width(5)
    
    self.button_redscale_main_settings_label_button=gtk.Button()
    self.button_redscale_main_settings_label_button_label=gtk.Label("Base for pixels computing")
    self.button_redscale_main_settings_label_button_label.show()
    self.button_redscale_main_settings_label_button.set_size_request((512)/3+36,32)
    self.button_redscale_main_settings_label_button_image=gtk.image_new_from_stock(gtk.STOCK_INDEX,4)
    self.button_redscale_main_settings_label_button_image.show()
    self.button_redscale_main_settings_label_button_hbox=gtk.HBox()
    self.button_redscale_main_settings_label_button_hbox.pack_start(self.button_redscale_main_settings_label_button_image,False,False,0)
    self.button_redscale_main_settings_label_button_hbox.pack_start(self.button_redscale_main_settings_label_button_label,False,False,0)
    self.button_redscale_main_settings_label_button_hbox.show()
    self.button_redscale_main_settings_label_button.add(self.button_redscale_main_settings_label_button_hbox)
    self.button_redscale_main_settings_label_button.set_focus_on_click(True)
    self.button_redscale_main_settings_label_button.set_relief(gtk.RELIEF_NONE)
    self.button_redscale_main_settings_label_button.show()
    
    self.combo_set_redscale=gtk.combo_box_new_text()
    self.combo_set_redscale.set_size_request((512+96)/4+16,32)
    self.combo_set_redscale.set_tooltip_text("Select base the pixel value for red values")
    for idx,v in [(0,"average"),(1,"minimun"),(2,"maximum"),(3,"red"),(4,"green"),(5,"blue")] :
      self.combo_set_redscale.insert_text(idx, v)
    self.combo_set_redscale.show()
    self.combo_set_redscale.set_active(0)
    self.combo_set_redscale.connect("changed",self.get_base_for_redscale)
    
    
    self.red_scale_pixel_value_toolbar.append_space()
    self.red_scale_pixel_value_toolbar.append_widget(self.button_redscale_main_settings_label_button,"","")
    self.red_scale_pixel_value_toolbar.append_widget(self.combo_set_redscale,"Select how to compute the redscale","")
    self.red_scale_pixel_value_toolbar.show()
    
    self.redscale_pixel_value_frame.add(self.red_scale_pixel_value_toolbar)
    self.redscale_pixel_value_frame.show()
    
    self.redscale_other_color_value_selection_frame_event_box=gtk.EventBox()
    self.redscale_other_color_value_selection_frame_event_box.modify_bg(gtk.STATE_NORMAL,self.redscale_other_color_value_selection_frame_event_box.get_colormap().alloc_color('#f0f0f0'))
    
    self.redscale_other_color_value_selection_frame=gtk.Frame(None)
    self.redscale_other_color_value_selection_frame_label_button=gtk.Button()
    self.redscale_other_color_value_selection_frame_label_button_label=gtk.Label("Red scale other colors values")
    self.redscale_other_color_value_selection_frame_label_button_label.show()
    self.redscale_other_color_value_selection_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_COLOR_PICKER,2)
    self.redscale_other_color_value_selection_frame_label_button_image.show()
    self.redscale_other_color_value_selection_frame_label_button_hbox=gtk.HBox()
    self.redscale_other_color_value_selection_frame_label_button_hbox.pack_start(self.redscale_other_color_value_selection_frame_label_button_image,False,False,0)
    self.redscale_other_color_value_selection_frame_label_button_hbox.pack_start(self.redscale_other_color_value_selection_frame_label_button_label,False,False,0)
    self.redscale_other_color_value_selection_frame_label_button_hbox.show()
    self.redscale_other_color_value_selection_frame_label_button.add(self.redscale_other_color_value_selection_frame_label_button_hbox)
    self.redscale_other_color_value_selection_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_other_color_value_selection_frame_label_button.show()
    self.redscale_other_color_value_selection_frame.set_label_widget(self.redscale_other_color_value_selection_frame_label_button)
    self.redscale_other_color_value_selection_frame.set_border_width(5)
    
    self.redscale_padding_main_vbox=gtk.VBox(False,5)
    self.redscale_padding_main_vbox.set_border_width(5)
    
    self.redscale_padding_type_percent_table=gtk.Table(rows=3,columns=2)
    
    self.redscale_padding_type_percent_vbox=gtk.HBox(False)
    
    self.redscale_padding_type_percent_radiobutton=gtk.RadioButton(None,"Percent from red value")
    self.redscale_padding_type_percent_radiobutton.set_name("percent")
    self.redscale_padding_type_percent_radiobutton.set_tooltip_text("Set the other colors on an percent from the red value.")
    self.redscale_padding_type_percent_radiobutton.connect("button-press-event",self.get_other_colors_choice_from_radiobutton)
    self.redscale_padding_type_percent_radiobutton.show()                
    
    self.redscale_padding_type_percent_green_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_percent_green_spinner_label_button=gtk.Button()
    self.redscale_padding_type_percent_green_spinner_label_button_label=gtk.Label("Green value")
    self.redscale_padding_type_percent_green_spinner_label_button_label.show()
    self.redscale_padding_type_percent_green_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_percent_green_spinner_label_button_image.show()
    self.redscale_padding_type_percent_green_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_percent_green_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_green_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_percent_green_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_green_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_percent_green_spinner_label_button_hbox.show()
    self.redscale_padding_type_percent_green_spinner_label_button.add(self.redscale_padding_type_percent_green_spinner_label_button_hbox)
    self.redscale_padding_type_percent_green_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_percent_green_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_percent_green_spinner_label_button.show()
    
    self.redscale_padding_type_percent_green_spinner_adjustment=gtk.Adjustment(value=0, lower=0, upper=100, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_percent_green_spinner=gtk.SpinButton(self.redscale_padding_type_percent_green_spinner_adjustment)
    self.redscale_padding_type_percent_green_spinner.set_name("percent green")
    self.redscale_padding_type_percent_green_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_percent_green_spinner.set_width_chars(8)
    self.redscale_padding_type_percent_green_spinner.set_alignment(0.5)
    self.redscale_padding_type_percent_green_spinner.set_value(0.0)
    self.redscale_padding_type_percent_green_spinner.set_tooltip_text("Set the green color pixel part on an percent from the red value.")
    self.redscale_padding_type_percent_green_spinner.connect("value-changed",self.get_other_color_percent)
    self.redscale_padding_type_percent_green_spinner.show()
    
    self.redscale_padding_type_percent_green_hbox.pack_start(self.redscale_padding_type_percent_green_spinner_label_button,False,False,0)
    self.redscale_padding_type_percent_green_hbox.pack_start(self.redscale_padding_type_percent_green_spinner,False,False,0)
    self.redscale_padding_type_percent_green_hbox.show()
    
    self.redscale_padding_type_percent_blue_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_percent_blue_spinner_label_button=gtk.Button()
    self.redscale_padding_type_percent_blue_spinner_label_button_label=gtk.Label("Blue value  ")
    self.redscale_padding_type_percent_blue_spinner_label_button_label.show()
    self.redscale_padding_type_percent_blue_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_percent_blue_spinner_label_button_image.show()
    self.redscale_padding_type_percent_blue_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_percent_blue_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_blue_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_percent_blue_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_blue_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_percent_blue_spinner_label_button_hbox.show()
    self.redscale_padding_type_percent_blue_spinner_label_button.add(self.redscale_padding_type_percent_blue_spinner_label_button_hbox)
    self.redscale_padding_type_percent_blue_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_percent_blue_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_percent_blue_spinner_label_button.show()
    
    self.redscale_padding_type_percent_blue_spinner_adjustment=gtk.Adjustment(value=0, lower=0, upper=100, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_percent_blue_spinner=gtk.SpinButton(self.redscale_padding_type_percent_blue_spinner_adjustment)
    self.redscale_padding_type_percent_blue_spinner.set_name("percent blue")
    self.redscale_padding_type_percent_blue_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_percent_blue_spinner.set_width_chars(8)
    self.redscale_padding_type_percent_blue_spinner.set_alignment(0.5)
    self.redscale_padding_type_percent_blue_spinner.set_value(0.0)
    self.redscale_padding_type_percent_blue_spinner.set_tooltip_text("Set the blue color pixel part on an percent from the red value.")
    self.redscale_padding_type_percent_blue_spinner.connect("value-changed",self.get_other_color_percent)
    self.redscale_padding_type_percent_blue_spinner.show()
    
    self.redscale_padding_type_percent_blue_hbox.pack_start(self.redscale_padding_type_percent_blue_spinner_label_button,False,False,0)
    self.redscale_padding_type_percent_blue_hbox.pack_start(self.redscale_padding_type_percent_blue_spinner,False,False,0)
    self.redscale_padding_type_percent_blue_hbox.show()
    
    self.redscale_padding_type_percent_alpha_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_percent_alpha_spinner_label_button=gtk.Button()
    self.redscale_padding_type_percent_alpha_spinner_label_button_label=gtk.Label("Alpha value")
    self.redscale_padding_type_percent_alpha_spinner_label_button_label.show()
    self.redscale_padding_type_percent_alpha_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_percent_alpha_spinner_label_button_image.show()
    self.redscale_padding_type_percent_alpha_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_percent_alpha_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_alpha_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_percent_alpha_spinner_label_button_hbox.pack_start(self.redscale_padding_type_percent_alpha_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_percent_alpha_spinner_label_button_hbox.show()
    self.redscale_padding_type_percent_alpha_spinner_label_button.add(self.redscale_padding_type_percent_alpha_spinner_label_button_hbox)
    self.redscale_padding_type_percent_alpha_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_percent_alpha_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_percent_alpha_spinner_label_button.show()
    
    self.redscale_padding_type_percent_alpha_spinner_adjustment=gtk.Adjustment(value=0, lower=0, upper=100, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_percent_alpha_spinner=gtk.SpinButton(self.redscale_padding_type_percent_alpha_spinner_adjustment)
    self.redscale_padding_type_percent_alpha_spinner.set_name("percent alpha")
    self.redscale_padding_type_percent_alpha_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_percent_alpha_spinner.set_width_chars(8)
    self.redscale_padding_type_percent_alpha_spinner.set_alignment(0.5)
    self.redscale_padding_type_percent_alpha_spinner.set_value(100.0)
    self.redscale_padding_type_percent_alpha_spinner.set_tooltip_text("Set the alpha value pixel part on an percent from the red value.")
    self.redscale_padding_type_percent_alpha_spinner.connect("value-changed",self.get_other_color_percent)
    self.redscale_padding_type_percent_alpha_spinner.show()
    
    self.redscale_padding_type_percent_alpha_hbox.pack_start(self.redscale_padding_type_percent_alpha_spinner_label_button,False,False,0)
    self.redscale_padding_type_percent_alpha_hbox.pack_start(self.redscale_padding_type_percent_alpha_spinner,False,False,0)
    self.redscale_padding_type_percent_alpha_hbox.show()
    
    
    self.redscale_padding_type_percent_table.attach(self.redscale_padding_type_percent_radiobutton, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_percent_table.attach(self.redscale_padding_type_percent_green_hbox, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_percent_table.attach(self.redscale_padding_type_percent_blue_hbox, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_percent_table.attach(self.redscale_padding_type_percent_alpha_hbox, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_percent_table.show()
    
    
    self.redscale_padding_type_arbitrary_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_arbitrary_table=gtk.Table(rows=3,columns=2)
    
    self.redscale_padding_type_arbitrary_radiobutton=gtk.RadioButton(self.redscale_padding_type_percent_radiobutton,"Set an arbitrary value  ")
    self.redscale_padding_type_arbitrary_radiobutton.set_name("arbitrary")
    self.redscale_padding_type_arbitrary_radiobutton.set_size_request((512+96)/3-28,32)
    self.redscale_padding_type_arbitrary_radiobutton.set_tooltip_text("Set the others colors on an arbitrary value.")
    self.redscale_padding_type_arbitrary_radiobutton.connect("button-press-event",self.get_other_colors_choice_from_radiobutton)
    self.redscale_padding_type_arbitrary_radiobutton.show()
    
    self.redscale_padding_type_arbitrary_green_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_arbitrary_green_spinner_label_button=gtk.Button()
    self.redscale_padding_type_arbitrary_green_spinner_label_button_label=gtk.Label("Green value")
    self.redscale_padding_type_arbitrary_green_spinner_label_button_label.show()
    self.redscale_padding_type_arbitrary_green_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_arbitrary_green_spinner_label_button_image.show()
    self.redscale_padding_type_arbitrary_green_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_arbitrary_green_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_green_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_arbitrary_green_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_green_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_arbitrary_green_spinner_label_button_hbox.show()
    self.redscale_padding_type_arbitrary_green_spinner_label_button.add(self.redscale_padding_type_arbitrary_green_spinner_label_button_hbox)
    self.redscale_padding_type_arbitrary_green_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_arbitrary_green_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_arbitrary_green_spinner_label_button.show()
   
    self.redscale_padding_type_arbitrary_green_spinner_adjustment=gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_arbitrary_green_spinner=gtk.SpinButton(self.redscale_padding_type_arbitrary_green_spinner_adjustment)
    self.redscale_padding_type_arbitrary_green_spinner.set_name("arbitrary green")
    self.redscale_padding_type_arbitrary_green_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_arbitrary_green_spinner.set_width_chars(8)
    self.redscale_padding_type_arbitrary_green_spinner.set_alignment(0.5)
    self.redscale_padding_type_arbitrary_green_spinner.set_value(0.0)
    self.redscale_padding_type_arbitrary_green_spinner.set_tooltip_text("Set the green color pixel part on an arbitrary value.")
    self.redscale_padding_type_arbitrary_green_spinner.connect("value-changed",self.get_other_color_arbitrary)
    self.redscale_padding_type_arbitrary_green_spinner.show()
    
    self.redscale_padding_type_arbitrary_green_hbox.pack_start(self.redscale_padding_type_arbitrary_green_spinner_label_button,False,False,0)
    self.redscale_padding_type_arbitrary_green_hbox.pack_start(self.redscale_padding_type_arbitrary_green_spinner,False,False,0)
    self.redscale_padding_type_arbitrary_green_hbox.show()
    
    self.redscale_padding_type_arbitrary_blue_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_arbitrary_blue_spinner_label_button=gtk.Button()
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_label=gtk.Label("Blue value  ")
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_label.show()
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_image.show()
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_blue_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_blue_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button_hbox.show()
    self.redscale_padding_type_arbitrary_blue_spinner_label_button.add(self.redscale_padding_type_arbitrary_blue_spinner_label_button_hbox)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_arbitrary_blue_spinner_label_button.show()
    
    self.redscale_padding_type_arbitrary_blue_spinner_adjustment=gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_arbitrary_blue_spinner=gtk.SpinButton(self.redscale_padding_type_arbitrary_blue_spinner_adjustment)
    self.redscale_padding_type_arbitrary_blue_spinner.set_name("arbitrary blue")
    self.redscale_padding_type_arbitrary_blue_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_arbitrary_blue_spinner.set_width_chars(8)
    self.redscale_padding_type_arbitrary_blue_spinner.set_alignment(0.5)
    self.redscale_padding_type_arbitrary_blue_spinner.set_value(0.0)
    self.redscale_padding_type_arbitrary_blue_spinner.set_tooltip_text("Set the blue color pixel part on an arbitrary value.")
    self.redscale_padding_type_arbitrary_blue_spinner.connect("value-changed",self.get_other_color_arbitrary)
    self.redscale_padding_type_arbitrary_blue_spinner.show()
    
    self.redscale_padding_type_arbitrary_blue_hbox.pack_start(self.redscale_padding_type_arbitrary_blue_spinner_label_button,False,False,0)
    self.redscale_padding_type_arbitrary_blue_hbox.pack_start(self.redscale_padding_type_arbitrary_blue_spinner,False,False,0)
    self.redscale_padding_type_arbitrary_blue_hbox.show()
    
    self.redscale_padding_type_arbitrary_alpha_hbox=gtk.HBox(False)
    
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button=gtk.Button()
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_label=gtk.Label("Alpha value")
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_label.show()
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SELECT_COLOR,4)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_image.show()
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_hbox=gtk.HBox()
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_alpha_spinner_label_button_image,False,False,0)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_hbox.pack_start(self.redscale_padding_type_arbitrary_alpha_spinner_label_button_label,False,False,0)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button_hbox.show()
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button.add(self.redscale_padding_type_arbitrary_alpha_spinner_label_button_hbox)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button.set_focus_on_click(False)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button.set_size_request(128-16,32)
    self.redscale_padding_type_arbitrary_alpha_spinner_label_button.show()
    
    self.redscale_padding_type_arbitrary_alpha_spinner_adjustment=gtk.Adjustment(value=255, lower=0, upper=255, step_incr=1, page_incr=0, page_size=0)
    self.redscale_padding_type_arbitrary_alpha_spinner=gtk.SpinButton(self.redscale_padding_type_arbitrary_alpha_spinner_adjustment)
    self.redscale_padding_type_arbitrary_alpha_spinner.set_name("arbitrary alpha")
    self.redscale_padding_type_arbitrary_alpha_spinner.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.redscale_padding_type_arbitrary_alpha_spinner.set_width_chars(8)
    self.redscale_padding_type_arbitrary_alpha_spinner.set_alignment(0.5)
    self.redscale_padding_type_arbitrary_alpha_spinner.set_value(255.0)
    self.redscale_padding_type_arbitrary_alpha_spinner.set_tooltip_text("Set the alpha value pixel part on an arbitrary value.")
    self.redscale_padding_type_arbitrary_alpha_spinner.connect("value-changed",self.get_other_color_arbitrary)
    self.redscale_padding_type_arbitrary_alpha_spinner.show()
    
    self.redscale_padding_type_arbitrary_alpha_hbox.pack_start(self.redscale_padding_type_arbitrary_alpha_spinner_label_button,False,False,0)
    self.redscale_padding_type_arbitrary_alpha_hbox.pack_start(self.redscale_padding_type_arbitrary_alpha_spinner,False,False,0)
    self.redscale_padding_type_arbitrary_alpha_hbox.show()
    
    self.redscale_padding_type_arbitrary_table.attach(self.redscale_padding_type_arbitrary_radiobutton, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_arbitrary_table.attach(self.redscale_padding_type_arbitrary_green_hbox, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_arbitrary_table.attach(self.redscale_padding_type_arbitrary_blue_hbox, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_arbitrary_table.attach(self.redscale_padding_type_arbitrary_alpha_hbox, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
    self.redscale_padding_type_arbitrary_table.show()
    
    self.redscale_padding_main_separator_0=gtk.HSeparator()
    self.redscale_padding_main_separator_0.set_size_request(512-128,16)
    self.redscale_padding_main_separator_0.show()
    
    self.redscale_padding_main_separator_1=gtk.HSeparator()
    self.redscale_padding_main_separator_1.set_size_request(512-128,16)
    self.redscale_padding_main_separator_1.show()
    
    self.redscale_padding_type_original_radiobutton=gtk.RadioButton(self.redscale_padding_type_percent_radiobutton,"Set the others colors on 0 and keep alpha value")
    self.redscale_padding_type_original_radiobutton.set_name("zero")
    self.redscale_padding_type_original_radiobutton.set_tooltip_text("Set the others colors on 0 and keep the pixel alpha value.")
    self.redscale_padding_type_original_radiobutton.set_size_request((512+96)/3-28,32) 
    self.redscale_padding_type_original_radiobutton.set_active(1)
    self.redscale_padding_type_original_radiobutton.connect("button-press-event",self.get_other_colors_choice_from_radiobutton)
    self.redscale_padding_type_original_radiobutton.show()
    
    self.redscale_padding_main_vbox.pack_start(self.redscale_padding_type_percent_table,False,False,0)
    self.redscale_padding_main_vbox.pack_start(self.redscale_padding_main_separator_0,False,False,0)
    self.redscale_padding_main_vbox.pack_start(self.redscale_padding_type_arbitrary_table,False,False,0)
    self.redscale_padding_main_vbox.pack_start(self.redscale_padding_main_separator_1,False,False,0)
    self.redscale_padding_main_vbox.pack_start(self.redscale_padding_type_original_radiobutton,False,False,0)
    self.redscale_padding_main_vbox.show()
    
    
    
    self.redscale_other_color_value_selection_frame_event_box.add(self.redscale_padding_main_vbox)
    self.redscale_other_color_value_selection_frame_event_box.set_border_width(5)
    self.redscale_other_color_value_selection_frame_event_box.show()
    
    self.redscale_other_color_value_selection_frame.add(self.redscale_other_color_value_selection_frame_event_box)
    self.redscale_other_color_value_selection_frame.show()
    
    self.redscale_area_vbox=self.redscale_dialog.get_content_area()
    
    
    self.redscale_area_vbox.pack_start(self.redscale_pixel_value_frame,False,False,0)
    self.redscale_area_vbox.pack_start(self.redscale_other_color_value_selection_frame,False,False)
    
    
    
    self.redscale_dialog_action_hbox=self.redscale_dialog.get_action_area()
    
    self.redscale_dialog_action_frame=gtk.Frame()
    self.redscale_dialog_action_frame.set_border_width(5)
    self.redscale_dialog_action_frame_label_button=gtk.Button()
    self.redscale_dialog_action_frame_label_button_label=gtk.Label("Action")
    self.redscale_dialog_action_frame_label_button_label.show()
    self.redscale_dialog_action_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_EXECUTE,2)
    self.redscale_dialog_action_frame_label_button_image.show()
    self.redscale_dialog_action_frame_label_button_hbox=gtk.HBox()
    self.redscale_dialog_action_frame_label_button_hbox.pack_start(self.redscale_dialog_action_frame_label_button_image,False,False,0)
    self.redscale_dialog_action_frame_label_button_hbox.pack_start(self.redscale_dialog_action_frame_label_button_label,False,False,0)
    self.redscale_dialog_action_frame_label_button_hbox.show()
    self.redscale_dialog_action_frame_label_button.add(self.redscale_dialog_action_frame_label_button_hbox)
    self.redscale_dialog_action_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.redscale_dialog_action_frame_label_button.show()
    self.redscale_dialog_action_frame.set_label_widget(self.redscale_dialog_action_frame_label_button)
    
    self.redscale_dialog_action_toolbar=gtk.Toolbar()
    self.redscale_dialog_action_toolbar.set_border_width(5)
    
    self.redscale_dialog_action_close_button=gtk.Button()
    self.redscale_dialog_action_close_button_label=gtk.Label("    Close")
    self.redscale_dialog_action_close_button_label.show()
    self.redscale_dialog_action_close_button_space=gtk.Label("          ")
    self.redscale_dialog_action_close_button_space.show()
    self.redscale_dialog_action_close_button_image=gtk.image_new_from_stock(gtk.STOCK_CLOSE,4)
    self.redscale_dialog_action_close_button_image.show()
    self.redscale_dialog_action_close_button_hbox=gtk.HBox()
    self.redscale_dialog_action_close_button_hbox.pack_start(self.redscale_dialog_action_close_button_space,False,False,0)
    self.redscale_dialog_action_close_button_hbox.pack_start(self.redscale_dialog_action_close_button_image,False,False,0)
    self.redscale_dialog_action_close_button_hbox.pack_start(self.redscale_dialog_action_close_button_label,False,False,0)
    self.redscale_dialog_action_close_button_hbox.show()
    self.redscale_dialog_action_close_button.add(self.redscale_dialog_action_close_button_hbox)
    self.redscale_dialog_action_close_button.set_size_request((512-128)/2-22,32)
    self.redscale_dialog_action_close_button.connect("button-press-event",self.cancel)
    self.redscale_dialog_action_close_button.show()
    
    self.redscale_dialog_action_apply_button=gtk.Button()
    self.redscale_dialog_action_apply_button_label=gtk.Label("    Apply")
    self.redscale_dialog_action_apply_button_label.show()
    self.redscale_dialog_action_apply_button_space=gtk.Label("          ")
    self.redscale_dialog_action_apply_button_space.show()
    self.redscale_dialog_action_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_APPLY,4)
    self.redscale_dialog_action_apply_button_image.show()
    self.redscale_dialog_action_apply_button_hbox=gtk.HBox()
    self.redscale_dialog_action_apply_button_hbox.pack_start(self.redscale_dialog_action_apply_button_space,False,False,0)
    self.redscale_dialog_action_apply_button_hbox.pack_start(self.redscale_dialog_action_apply_button_image,False,False,0)
    self.redscale_dialog_action_apply_button_hbox.pack_start(self.redscale_dialog_action_apply_button_label,False,False,0)
    self.redscale_dialog_action_apply_button_hbox.show()
    self.redscale_dialog_action_apply_button.add(self.redscale_dialog_action_apply_button_hbox)
    self.redscale_dialog_action_apply_button.set_size_request((512-128)/2-22,32)
    self.redscale_dialog_action_apply_button.connect("button-press-event",self.apply_scaling)
    self.redscale_dialog_action_apply_button.show()
    
    self.redscale_dialog_action_toolbar.append_space()
    self.redscale_dialog_action_toolbar.append_widget(self.redscale_dialog_action_close_button,"Close the redscale editor.","")
    self.redscale_dialog_action_toolbar.append_space()
    self.redscale_dialog_action_toolbar.append_widget(self.redscale_dialog_action_apply_button,"Apply the redscale filter with current settings on the image.","")
    self.redscale_dialog_action_toolbar.append_space()
    
    self.redscale_dialog_action_toolbar.show()
    
    self.redscale_dialog_action_frame.add(self.redscale_dialog_action_toolbar)
    self.redscale_dialog_action_frame.show()
    
    self.redscale_dialog_action_hbox.pack_start(self.redscale_dialog_action_frame,False,False,0)
    
    
    
    self.redscale_dialog.set_has_separator(True)
    
    self.redscale_dialog.show()
    
    self.redscale_dialog.run()
    
    if colors_setting == 0 :
      return scaling_setting,colors_setting,percent_green, percent_blue, percent_alpha
    elif colors_setting == 1 :
      return scaling_setting,colors_setting,arbitrary_green, arbitrary_blue, arbitrary_alpha
    else :
      return scaling_setting,colors_setting,False,False,False
    
  def cancel(self,widget,event) :
    closed(self.redscale_dialog,False)
  
  def apply_scaling(self,widget,event) :
    global scaling_setting, colors_setting, percent_green, percent_blue, percent_alpha, arbitrary_green, arbitrary_blue, arbitrary_alpha
   
    scaling_setting=self.redscale_base_for_computing_value
    
    colors_setting=self.get_other_colors_main_setting 

    percent_green=self.get_other_color_percent_green
    percent_blue=self.get_other_color_percent_blue
    percent_alpha=self.get_other_color_percent_alpha
    

    arbitrary_green=self.get_other_color_arbitrary_green
    arbitrary_blue=self.get_other_color_arbitrary_blue
    arbitrary_alpha=self.get_other_color_arbitrary_alpha
    
    closed(self.redscale_dialog,False)
   
def closed(widget,event) :
  widget.destroy() # Destroy the widget and his children.
 
     
     


    




