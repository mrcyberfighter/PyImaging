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
  
from PIL import Image  

class Enhancement_dialog() :
  def __init__(self) :
    self.user_enhancement_choice=1
    
    self.color_enhancement_value=1.0
    self.brightness_enhancement_value=1.0
    self.contrast_enhancement_value=1.0
    self.sharpness_enhancement_value=1.0
    
    self.enhance_value=1.0
    
  def get_user_enhancement_type_choice(self,widget,event=False) :
    if widget.get_name() == "Color" :
      self.user_enhancement_choice=1
    elif widget.get_name() == "Brightness" :
      self.user_enhancement_choice=2
    elif widget.get_name() == "Contrast" :
      self.user_enhancement_choice=3 
    elif widget.get_name() == "Sharpness" :
      self.user_enhancement_choice=4    
    self.update_values()
    
  def get_user_enhancement_color_value_change(self,widget,event=False) :
    self.color_enhancement_value=self.color_adjustment_value_adjustment.get_value()
    self.update_values()
   
  def get_user_enhancement_brightness_value_change(self,widget,event=False) :
    self.brightness_enhancement_value=self.brightness_adjustment_value_adjustment.get_value()  
    self.update_values()
  
  def get_user_enhancement_contrast_value_change(self,widget,event=False) :
    self.contrast_enhancement_value=self.contrast_adjustment_value_adjustment.get_value()
    self.update_values()
   
  def get_user_enhancement_sharpness_value_change(self,widget,event=False) :
    self.sharpness_enhancement_value=self.sharpness_adjustment_value_adjustment.get_value()  
    self.update_values()
  
  def update_values(self) :
    if self.user_enhancement_choice == 1 :
      self.enhance_value=self.color_enhancement_value
    elif self.user_enhancement_choice == 2 :
      self.enhance_value=self.brightness_enhancement_value 
    elif self.user_enhancement_choice == 3 :
      self.enhance_value=self.contrast_enhancement_value
    elif self.user_enhancement_choice == 3 :
      self.enhance_value=self.sharpness_enhancement_value
  
  def create_dialog(self,instance) :
    
    self.enhancement_dialog=gtk.Dialog("Image adjusments.",None,0, None)
    
    self.enhancement_dialog.connect("delete_event",closed)
    self.enhancement_dialog.set_size_request(512-64-24,512+128+32)
    self.enhancement_dialog.modify_bg(gtk.STATE_NORMAL,self.enhancement_dialog.get_colormap().alloc_color('#d0d0d0'))
    
    self.color_adjustment_value_vbox=gtk.VBox()
    self.color_adjustment_value_vbox.set_border_width(5)
    
    self.color_adjustment_container=gtk.EventBox()
    self.color_adjustment_container.modify_bg(gtk.STATE_NORMAL,self.color_adjustment_container.get_colormap().alloc_color('#f0f0f0'))
    
    self.color_adjustment_value_frame=gtk.Frame(None)
    self.color_adjustment_value_frame_label_button=gtk.Button()
    self.color_adjustment_value_frame_label_button_label=gtk.Label(" Color adjustement")
    self.color_adjustment_value_frame_label_button_label.show()
    self.color_adjustment_value_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PREFERENCES,2)
    self.color_adjustment_value_frame_label_button_image.show()
    self.color_adjustment_value_frame_label_button_hbox=gtk.HBox()
    self.color_adjustment_value_frame_label_button_hbox.pack_start(self.color_adjustment_value_frame_label_button_image,False,False,0)
    self.color_adjustment_value_frame_label_button_hbox.pack_start(self.color_adjustment_value_frame_label_button_label,False,False,0)
    self.color_adjustment_value_frame_label_button_hbox.show()
    self.color_adjustment_value_frame_label_button.add(self.color_adjustment_value_frame_label_button_hbox)
    self.color_adjustment_value_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.color_adjustment_value_frame_label_button.set_can_focus(False)
    self.color_adjustment_value_frame_label_button.show()
    self.color_adjustment_value_frame.set_tooltip_text("Used to adjust the color balance of an image in a manner to the controls on a color TV set.\n0.0 = Give an black and white image\n1.0 = Give the original image.")
    self.color_adjustment_value_frame.set_label_widget(self.color_adjustment_value_frame_label_button)
    self.color_adjustment_value_frame.set_border_width(5)
    
    self.color_adjustment_choice_radiobutton_color=gtk.RadioButton(None, label="Apply Color settings")
    self.color_adjustment_choice_radiobutton_color.set_name("Colors")
    self.color_adjustment_choice_radiobutton_color.connect("button-press-event",self.get_user_enhancement_type_choice)
    self.color_adjustment_choice_radiobutton_color.show()
    
    self.color_adjustment_value_adjustment=gtk.Adjustment(value=1.0, lower=0.0, upper=2.0, step_incr=0.001, page_incr=0, page_size=0)
    self.color_adjustment_value_scale=gtk.HScale(adjustment=self.color_adjustment_value_adjustment)
    self.color_adjustment_value_scale.set_digits(3)
    self.color_adjustment_value_scale.set_draw_value(True)
    self.color_adjustment_value_scale.add_mark(1.0, gtk.POS_RIGHT, None)
    self.color_adjustment_value_scale.set_value_pos(gtk.POS_TOP)
    self.color_adjustment_value_scale.set_tooltip_text("Change value of the the color balance of an image.\n0.0 = Give an black and white image\n1.0 = Give the original image.\nYou can use the arrows for accurate setting") 
    self.color_adjustment_value_scale.connect("value-changed",self.get_user_enhancement_color_value_change)
    self.color_adjustment_value_scale.connect("move-slider",self.get_user_enhancement_color_value_change)
    self.color_adjustment_value_scale.show()
    
    self.color_adjustment_table=gtk.Table(rows=2,columns=1)
    self.color_adjustment_table.attach(self.color_adjustment_choice_radiobutton_color, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.color_adjustment_table.attach(self.color_adjustment_value_scale, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.color_adjustment_table.show()
    
    
    
    self.color_adjustment_container.add(self.color_adjustment_table)
    self.color_adjustment_container.show()
    
    self.color_adjustment_value_vbox.pack_start(self.color_adjustment_container,False,False,0)
    self.color_adjustment_value_vbox.show()
    
    self.color_adjustment_value_frame.add(self.color_adjustment_value_vbox)
    self.color_adjustment_value_frame.show()
    
    self.brightness_adjustment_value_vbox=gtk.VBox()
    self.brightness_adjustment_value_vbox.set_border_width(5)
    
    self.brightness_adjustment_container=gtk.EventBox()
    self.brightness_adjustment_container.modify_bg(gtk.STATE_NORMAL,self.brightness_adjustment_container.get_colormap().alloc_color('#f0f0f0'))
    
    self.brightness_adjustment_value_frame=gtk.Frame(None)
    self.brightness_adjustment_value_frame_label_button=gtk.Button()
    self.brightness_adjustment_value_frame_label_button_label=gtk.Label(" Brightness adjustement")
    self.brightness_adjustment_value_frame_label_button_label.show()
    self.brightness_adjustment_value_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PREFERENCES,2)
    self.brightness_adjustment_value_frame_label_button_image.show()
    self.brightness_adjustment_value_frame_label_button_hbox=gtk.HBox()
    self.brightness_adjustment_value_frame_label_button_hbox.pack_start(self.brightness_adjustment_value_frame_label_button_image,False,False,0)
    self.brightness_adjustment_value_frame_label_button_hbox.pack_start(self.brightness_adjustment_value_frame_label_button_label,False,False,0)
    self.brightness_adjustment_value_frame_label_button_hbox.show()
    self.brightness_adjustment_value_frame_label_button.add(self.brightness_adjustment_value_frame_label_button_hbox)
    self.brightness_adjustment_value_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.brightness_adjustment_value_frame_label_button.set_can_focus(False)
    self.brightness_adjustment_value_frame_label_button.show()
    self.brightness_adjustment_value_frame.set_tooltip_text("Used to control the brightness of an image.\n0.0 = Give an black image\n1.0 = Give the original image.")
    self.brightness_adjustment_value_frame.set_label_widget(self.brightness_adjustment_value_frame_label_button)
    self.brightness_adjustment_value_frame.set_border_width(5)
    
    self.brightness_adjustment_choice_radiobutton_color=gtk.RadioButton(self.color_adjustment_choice_radiobutton_color, label="Apply Brightness settings")
    self.brightness_adjustment_choice_radiobutton_color.set_name("Brightness")
    self.brightness_adjustment_choice_radiobutton_color.connect("button-press-event",self.get_user_enhancement_type_choice)
    self.brightness_adjustment_choice_radiobutton_color.show()
    
    self.brightness_adjustment_value_adjustment=gtk.Adjustment(value=1.0, lower=0.0, upper=2.0, step_incr=0.001, page_incr=0, page_size=0)
    self.brightness_adjustment_value_scale=gtk.HScale(adjustment=self.brightness_adjustment_value_adjustment)
    self.brightness_adjustment_value_scale.set_digits(3)
    self.brightness_adjustment_value_scale.set_draw_value(True)
    self.brightness_adjustment_value_scale.add_mark(1.0, gtk.POS_RIGHT, None)
    self.brightness_adjustment_value_scale.set_value_pos(gtk.POS_TOP)
    self.brightness_adjustment_value_scale.set_tooltip_text("Change value of the brightness of an image.\n0.0 = Give an black image\n1.0 = Give the original image.\nYou can use the arrows for accurate setting") 
    self.brightness_adjustment_value_scale.connect("value-changed",self.get_user_enhancement_brightness_value_change)
    self.brightness_adjustment_value_scale.connect("move-slider",self.get_user_enhancement_brightness_value_change)
    self.brightness_adjustment_value_scale.show()
    
    self.brightness_adjustment_table=gtk.Table(rows=2,columns=1)
    self.brightness_adjustment_table.attach(self.brightness_adjustment_choice_radiobutton_color, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.brightness_adjustment_table.attach(self.brightness_adjustment_value_scale, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.brightness_adjustment_table.set_border_width(5)
    self.brightness_adjustment_table.show()
    
    self.brightness_adjustment_container.add(self.brightness_adjustment_table)
    self.brightness_adjustment_container.show()
    
    self.brightness_adjustment_value_vbox.pack_start(self.brightness_adjustment_container,False,False,0)
    self.brightness_adjustment_value_vbox.show()
    
    self.brightness_adjustment_value_frame.add(self.brightness_adjustment_value_vbox)
    self.brightness_adjustment_value_frame.show()
    
    self.contrast_adjustment_value_vbox=gtk.VBox()
    self.contrast_adjustment_value_vbox.set_border_width(5)
    
    self.contrast_adjustment_container=gtk.EventBox()
    self.contrast_adjustment_container.modify_bg(gtk.STATE_NORMAL,self.contrast_adjustment_container.get_colormap().alloc_color('#f0f0f0'))
    
    self.contrast_adjustment_value_frame=gtk.Frame(None)
    self.contrast_adjustment_value_frame_label_button=gtk.Button()
    self.contrast_adjustment_value_frame_label_button_label=gtk.Label(" Contrast adjustement")
    self.contrast_adjustment_value_frame_label_button_label.show()
    self.contrast_adjustment_value_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PREFERENCES,2)
    self.contrast_adjustment_value_frame_label_button_image.show()
    self.contrast_adjustment_value_frame_label_button_hbox=gtk.HBox()
    self.contrast_adjustment_value_frame_label_button_hbox.pack_start(self.contrast_adjustment_value_frame_label_button_image,False,False,0)
    self.contrast_adjustment_value_frame_label_button_hbox.pack_start(self.contrast_adjustment_value_frame_label_button_label,False,False,0)
    self.contrast_adjustment_value_frame_label_button_hbox.show()
    self.contrast_adjustment_value_frame_label_button.add(self.contrast_adjustment_value_frame_label_button_hbox)
    self.contrast_adjustment_value_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.contrast_adjustment_value_frame_label_button.set_can_focus(False)
    self.contrast_adjustment_value_frame_label_button.show()
    self.contrast_adjustment_value_frame.set_tooltip_text("Used to control the contrast of an image. Similar to the controls on a TV set.\n0.0 = Give an solid gray image\n1.0 = Give the original image.")
    self.contrast_adjustment_value_frame.set_label_widget(self.contrast_adjustment_value_frame_label_button)
    self.contrast_adjustment_value_frame.set_border_width(5)
    
    self.contrast_adjustment_choice_radiobutton_color=gtk.RadioButton(self.brightness_adjustment_choice_radiobutton_color, label="Apply Contrast settings")
    self.contrast_adjustment_choice_radiobutton_color.set_name("Contrast")
    self.contrast_adjustment_choice_radiobutton_color.connect("button-press-event",self.get_user_enhancement_type_choice)
    self.contrast_adjustment_choice_radiobutton_color.show()
    
    self.contrast_adjustment_value_adjustment=gtk.Adjustment(value=1.0, lower=0.0, upper=2.0, step_incr=0.001, page_incr=0, page_size=0)
    self.contrast_adjustment_value_scale=gtk.HScale(adjustment=self.contrast_adjustment_value_adjustment)
    self.contrast_adjustment_value_scale.set_digits(3)
    self.contrast_adjustment_value_scale.set_draw_value(True)
    self.contrast_adjustment_value_scale.add_mark(1.0, gtk.POS_RIGHT, None)
    self.contrast_adjustment_value_scale.set_value_pos(gtk.POS_TOP)
    self.contrast_adjustment_value_scale.set_tooltip_text("Change value of the contrast of an image.\n0.0 = Give an solid gray image\n1.0 = Give the original image.\nYou can use the arrows for accurate setting") 
    self.contrast_adjustment_value_scale.connect("value-changed",self.get_user_enhancement_contrast_value_change)
    self.contrast_adjustment_value_scale.connect("move-slider",self.get_user_enhancement_contrast_value_change)
    self.contrast_adjustment_value_scale.show()
    
    self.contrast_adjustment_table=gtk.Table(rows=2,columns=1)
    self.contrast_adjustment_table.attach(self.contrast_adjustment_choice_radiobutton_color, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.contrast_adjustment_table.attach(self.contrast_adjustment_value_scale, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.contrast_adjustment_table.show()
    
    self.contrast_adjustment_container.add(self.contrast_adjustment_table)
    self.contrast_adjustment_container.show()
    
    self.contrast_adjustment_value_vbox.pack_start(self.contrast_adjustment_container,False,False,0)
    self.contrast_adjustment_value_vbox.show()
    
    self.contrast_adjustment_value_frame.add(self.contrast_adjustment_value_vbox)
    self.contrast_adjustment_value_frame.show()
    
    self.sharpness_adjustment_value_vbox=gtk.VBox()
    self.sharpness_adjustment_value_vbox.set_border_width(5)
    
    self.sharpness_adjustment_container=gtk.EventBox()
    self.sharpness_adjustment_container.modify_bg(gtk.STATE_NORMAL,self.sharpness_adjustment_container.get_colormap().alloc_color('#f0f0f0'))
    
    self.sharpness_adjustment_value_frame=gtk.Frame(None)
    self.sharpness_adjustment_value_frame_label_button=gtk.Button()
    self.sharpness_adjustment_value_frame_label_button_label=gtk.Label(" Sharpness adjustement")
    self.sharpness_adjustment_value_frame_label_button_label.show()
    self.sharpness_adjustment_value_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PREFERENCES,2)
    self.sharpness_adjustment_value_frame_label_button_image.show()
    self.sharpness_adjustment_value_frame_label_button_hbox=gtk.HBox()
    self.sharpness_adjustment_value_frame_label_button_hbox.pack_start(self.sharpness_adjustment_value_frame_label_button_image,False,False,0)
    self.sharpness_adjustment_value_frame_label_button_hbox.pack_start(self.sharpness_adjustment_value_frame_label_button_label,False,False,0)
    self.sharpness_adjustment_value_frame_label_button_hbox.show()
    self.sharpness_adjustment_value_frame_label_button.add(self.sharpness_adjustment_value_frame_label_button_hbox)
    self.sharpness_adjustment_value_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.sharpness_adjustment_value_frame_label_button.set_can_focus(False)
    self.sharpness_adjustment_value_frame_label_button.show()
    self.sharpness_adjustment_value_frame.set_tooltip_text("Used to control the sharpness of an image. Similar to the controls on a TV set.\n0.0 = Give an blurred image\n1.0 = Give the original image.\n2.0 = Give an sharpen image.")
    self.sharpness_adjustment_value_frame.set_label_widget(self.sharpness_adjustment_value_frame_label_button)
    self.sharpness_adjustment_value_frame.set_border_width(5)
    
    self.sharpness_adjustment_choice_radiobutton_color=gtk.RadioButton(self.contrast_adjustment_choice_radiobutton_color, label="Apply Sharpness settings")
    self.sharpness_adjustment_choice_radiobutton_color.set_name("Sharpness")
    self.sharpness_adjustment_choice_radiobutton_color.connect("button-press-event",self.get_user_enhancement_type_choice)
    self.sharpness_adjustment_choice_radiobutton_color.show()
    
    self.sharpness_adjustment_value_adjustment=gtk.Adjustment(value=1.0, lower=0.0, upper=2.0, step_incr=0.001, page_incr=0, page_size=0)
    self.sharpness_adjustment_value_scale=gtk.HScale(adjustment=self.sharpness_adjustment_value_adjustment)
    self.sharpness_adjustment_value_scale.set_digits(3)
    self.sharpness_adjustment_value_scale.set_draw_value(True)
    self.sharpness_adjustment_value_scale.add_mark(1.0, gtk.POS_RIGHT, None)
    self.sharpness_adjustment_value_scale.set_value_pos(gtk.POS_TOP)
    self.sharpness_adjustment_value_scale.set_tooltip_text("Change value of the sharpness of an image.\n0.0 = Give an blurred image\n1.0 = Give the original image.\n2.0 = Give an sharpen image.\nYou can use the arrows for accurate setting.") 
    self.sharpness_adjustment_value_scale.connect("value-changed",self.get_user_enhancement_sharpness_value_change)
    self.sharpness_adjustment_value_scale.connect("move-slider",self.get_user_enhancement_sharpness_value_change)
    self.sharpness_adjustment_value_scale.show()
    
    self.sharpness_adjustment_table=gtk.Table(rows=2,columns=1)
    self.sharpness_adjustment_table.attach(self.sharpness_adjustment_choice_radiobutton_color, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.sharpness_adjustment_table.attach(self.sharpness_adjustment_value_scale, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=2, ypadding=2)
    self.sharpness_adjustment_table.show()
    
    self.sharpness_adjustment_container.add(self.sharpness_adjustment_table)
    self.sharpness_adjustment_container.show()
    
    self.sharpness_adjustment_value_vbox.pack_start(self.sharpness_adjustment_container,False,False,0)
    self.sharpness_adjustment_value_vbox.show()
    
    self.sharpness_adjustment_value_frame.add(self.sharpness_adjustment_value_vbox)
    self.sharpness_adjustment_value_frame.show()
    
    self.enhancement_dialog_content_area_vbox=self.enhancement_dialog.get_content_area()
    
    self.enhancement_dialog_content_area_vbox.pack_start(self.color_adjustment_value_frame,False,False,0)
    self.enhancement_dialog_content_area_vbox.pack_start(self.brightness_adjustment_value_frame,False,False,0)
    self.enhancement_dialog_content_area_vbox.pack_start(self.contrast_adjustment_value_frame,False,False,0)
    self.enhancement_dialog_content_area_vbox.pack_start(self.sharpness_adjustment_value_frame,False,False,0)
    self.enhancement_dialog_content_area_vbox.show()
    
    self.enhancement_dialog_action_hbox=self.enhancement_dialog.get_action_area()
    
    self.enhancement_dialog_action_frame=gtk.Frame()
    self.enhancement_dialog_action_frame.set_border_width(5)
    self.enhancement_dialog_action_frame_label_button=gtk.Button()
    self.enhancement_dialog_action_frame_label_button_label=gtk.Label("Action")
    self.enhancement_dialog_action_frame_label_button_label.show()
    self.enhancement_dialog_action_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_EXECUTE,2)
    self.enhancement_dialog_action_frame_label_button_image.show()
    self.enhancement_dialog_action_frame_label_button_hbox=gtk.HBox()
    self.enhancement_dialog_action_frame_label_button_hbox.pack_start(self.enhancement_dialog_action_frame_label_button_image,False,False,0)
    self.enhancement_dialog_action_frame_label_button_hbox.pack_start(self.enhancement_dialog_action_frame_label_button_label,False,False,0)
    self.enhancement_dialog_action_frame_label_button_hbox.show()
    self.enhancement_dialog_action_frame_label_button.add(self.enhancement_dialog_action_frame_label_button_hbox)
    self.enhancement_dialog_action_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.enhancement_dialog_action_frame_label_button.show()
    self.enhancement_dialog_action_frame.set_label_widget(self.enhancement_dialog_action_frame_label_button)
    
    self.enhancement_dialog_action_toolbar=gtk.Toolbar()
    self.enhancement_dialog_action_toolbar.set_border_width(5)
    
    self.enhancement_dialog_action_close_button=gtk.Button()
    self.enhancement_dialog_action_close_button_label=gtk.Label("    Close")
    self.enhancement_dialog_action_close_button_label.show()
    self.enhancement_dialog_action_close_button_space=gtk.Label("          ")
    self.enhancement_dialog_action_close_button_space.show()
    self.enhancement_dialog_action_close_button_image=gtk.image_new_from_stock(gtk.STOCK_CLOSE,4)
    self.enhancement_dialog_action_close_button_image.show()
    self.enhancement_dialog_action_close_button_hbox=gtk.HBox()
    self.enhancement_dialog_action_close_button_hbox.pack_start(self.enhancement_dialog_action_close_button_space,False,False,0)
    self.enhancement_dialog_action_close_button_hbox.pack_start(self.enhancement_dialog_action_close_button_image,False,False,0)
    self.enhancement_dialog_action_close_button_hbox.pack_start(self.enhancement_dialog_action_close_button_label,False,False,0)
    self.enhancement_dialog_action_close_button_hbox.show()
    self.enhancement_dialog_action_close_button.add(self.enhancement_dialog_action_close_button_hbox)
    self.enhancement_dialog_action_close_button.set_size_request((512-128)/2-22,32)
    self.enhancement_dialog_action_close_button.connect("button-press-event",self.cancel)
    self.enhancement_dialog_action_close_button.show()
    
    self.enhancement_dialog_action_apply_button=gtk.Button()
    self.enhancement_dialog_action_apply_button_label=gtk.Label("    Apply")
    self.enhancement_dialog_action_apply_button_label.show()
    self.enhancement_dialog_action_apply_button_space=gtk.Label("          ")
    self.enhancement_dialog_action_apply_button_space.show()
    self.enhancement_dialog_action_apply_button_image=gtk.image_new_from_stock(gtk.STOCK_APPLY,4)
    self.enhancement_dialog_action_apply_button_image.show()
    self.enhancement_dialog_action_apply_button_hbox=gtk.HBox()
    self.enhancement_dialog_action_apply_button_hbox.pack_start(self.enhancement_dialog_action_apply_button_space,False,False,0)
    self.enhancement_dialog_action_apply_button_hbox.pack_start(self.enhancement_dialog_action_apply_button_image,False,False,0)
    self.enhancement_dialog_action_apply_button_hbox.pack_start(self.enhancement_dialog_action_apply_button_label,False,False,0)
    self.enhancement_dialog_action_apply_button_hbox.show()
    self.enhancement_dialog_action_apply_button.add(self.enhancement_dialog_action_apply_button_hbox)
    self.enhancement_dialog_action_apply_button.set_size_request((512-128)/2-22,32)
    self.enhancement_dialog_action_apply_button.connect("button-press-event",instance.apply_adjustment,self.user_enhancement_choice,self.enhance_value)
    self.enhancement_dialog_action_apply_button.show()
    
    self.enhancement_dialog_action_toolbar.append_space()
    self.enhancement_dialog_action_toolbar.append_widget(self.enhancement_dialog_action_close_button,"Close the adjustment editor.","")
    self.enhancement_dialog_action_toolbar.append_space()
    self.enhancement_dialog_action_toolbar.append_widget(self.enhancement_dialog_action_apply_button,"Apply the choosen adjustement with current settings on the image.","")
    self.enhancement_dialog_action_toolbar.append_space()
    
    self.enhancement_dialog_action_toolbar.show()
    
    self.enhancement_dialog_action_frame.add(self.enhancement_dialog_action_toolbar)
    self.enhancement_dialog_action_frame.show()
    
    self.enhancement_dialog_action_hbox.pack_start(self.enhancement_dialog_action_frame,False,False,0)
    self.enhancement_dialog_action_hbox.show()
    
    
    self.enhancement_dialog.set_has_separator(True)
    
    self.enhancement_dialog.show()
    
    self.enhancement_dialog.run()
    
  def cancel(self,widget,event) :
    closed(self.enhancement_dialog,False)
  
  def apply_scaling(self,widget,event) :
    pass
   
def closed(widget,event) :
  widget.destroy() 
 
    




