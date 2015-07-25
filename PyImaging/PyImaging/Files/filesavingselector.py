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

from os.path import expanduser,isdir,basename
 
 
 
class File_Saving_Selector() : 
  
  def __init__(self,format_str,mode,size,width_factor,height_factor,processing_instance) :
    self.format_str=format_str
    self.size=size
    
    self.width_factor=width_factor
    self.height_factor=height_factor
    
    self.ratio_factor=width_factor # Default value
    self.ratio_factor_choice="Width"
    self.bool_change_size=False
    
    self.bool_compute_ratio=False
    
    self.mode=mode
    
    self.format_src=format_str
    
    self.processing_instance=processing_instance
    
    
  def select_file(self,filetype="*") :
      self.select_file_toplevel=gtk.Window(type=gtk.WINDOW_TOPLEVEL)
      self.select_file_toplevel.connect("delete_event",self.select_file_operation_toplevel_cancel)
      self.select_file_toplevel.set_title("Save image file as.")
      self.select_file_toplevel.set_size_request(768+128-16-8,256+256+64)
      self.select_file_toplevel.set_resizable(False)
        
      self.select_file_file_chooser=gtk.FileChooserWidget(action=gtk.FILE_CHOOSER_ACTION_SAVE, backend=None)
      self.select_file_file_chooser.connect("selection-changed",self.select_file_operation_update_selection)
      self.select_file_file_chooser.connect("file-activated",self.select_file_operation_update_selection)
      self.select_file_file_chooser.connect("current-folder-changed",self.select_file_operation_update_selection)
      
      self.select_file_file_chooser.connect("key-press-event",self.select_file_operation_update_selection)
      
      self.select_file_file_ok_button=gtk.Button()
      self.select_file_file_ok_button_label=gtk.Label("    Confirm")
      self.select_file_file_ok_button_label.show()
      self.select_file_file_ok_button_space=gtk.Label("        ")
      self.select_file_file_ok_button_space.show()
      self.select_file_file_ok_button_image=gtk.image_new_from_stock(gtk.STOCK_OK,4)
      self.select_file_file_ok_button_image.show()
      self.select_file_file_ok_button_hbox=gtk.HBox()
      self.select_file_file_ok_button_hbox.pack_start(self.select_file_file_ok_button_space,False,False,0)
      self.select_file_file_ok_button_hbox.pack_start(self.select_file_file_ok_button_image,False,False,0)
      self.select_file_file_ok_button_hbox.pack_start(self.select_file_file_ok_button_label,False,False,0)
      self.select_file_file_ok_button_hbox.show()
      self.select_file_file_ok_button.add(self.select_file_file_ok_button_hbox)
      self.select_file_file_ok_button.connect("button-press-event",self.select_file_operation_toplevel_ok)
      self.select_file_file_ok_button.set_size_request(128+16+14,32)
      self.select_file_file_ok_button.show()
      
      self.select_file_file_cancel_button=gtk.Button()
      self.select_file_file_cancel_button_label=gtk.Label("    Cancel")
      self.select_file_file_cancel_button_label.show()
      self.select_file_file_cancel_button_space=gtk.Label("    ")
      self.select_file_file_cancel_button_space.show()
      self.select_file_file_cancel_button_image=gtk.image_new_from_stock(gtk.STOCK_CANCEL,4)
      self.select_file_file_cancel_button_image.show()
      self.select_file_file_cancel_button_hbox=gtk.HBox()
      self.select_file_file_cancel_button_hbox.pack_start(self.select_file_file_cancel_button_space,False,False,0)
      self.select_file_file_cancel_button_hbox.pack_start(self.select_file_file_cancel_button_image,False,False,0)
      self.select_file_file_cancel_button_hbox.pack_start(self.select_file_file_cancel_button_label,False,False,0)
      self.select_file_file_cancel_button_hbox.show()
      self.select_file_file_cancel_button.add(self.select_file_file_cancel_button_hbox)
      self.select_file_file_cancel_button.connect("button-press-event",self.select_file_operation_toplevel_cancel)
      self.select_file_file_cancel_button.set_size_request(128+16,32)
      self.select_file_file_cancel_button.show()
      
      
      self.select_file_file_width_height_hbox=gtk.HBox()

      
      self.select_file_file_width_hbox=gtk.HBox()
      
      self.select_file_file_width_spinner_button=gtk.Button()
      self.select_file_file_width_spinner_button_label=gtk.Label("Width:")
      self.select_file_file_width_spinner_button_label.show()
      self.select_file_file_width_spinner_button_space=gtk.Label(" ")
      self.select_file_file_width_spinner_button_space.show()
      self.select_file_file_width_spinner_image=gtk.image_new_from_stock(gtk.STOCK_ZOOM_FIT,4)
      self.select_file_file_width_spinner_image.show()
      self.select_file_file_width_spinner_hbox=gtk.HBox()
      self.select_file_file_width_spinner_hbox.pack_start(self.select_file_file_width_spinner_button_space,False,False,0)
      self.select_file_file_width_spinner_hbox.pack_start(self.select_file_file_width_spinner_image,False,False,0)
      self.select_file_file_width_spinner_hbox.pack_start(self.select_file_file_width_spinner_button_label,False,False,0)
      self.select_file_file_width_spinner_hbox.show()
      self.select_file_file_width_spinner_button.add(self.select_file_file_width_spinner_hbox)
      self.select_file_file_width_spinner_button.set_relief(gtk.RELIEF_NONE)
      self.select_file_file_width_spinner_button.show()
      
      self.select_file_file_width_spinner_adjustment=gtk.Adjustment(value=self.size[0], lower=0, upper=4096*16, step_incr=1, page_incr=0, page_size=0)
      self.select_file_file_width_spinner=gtk.SpinButton(adjustment=self.select_file_file_width_spinner_adjustment, climb_rate=1, digits=0)
      self.select_file_file_width_spinner.set_tooltip_text("Set the wanted image size width and confirm with Enter.\nYou can apply the ratio width/height to the height value\nby clicking the \"Size ratio\" button.")
      self.select_file_file_width_spinner.set_numeric(True)
      self.select_file_file_width_spinner.set_wrap(False)
      self.select_file_file_width_spinner.connect("value-changed",self.get_width_value)
      self.select_file_file_width_spinner.connect("key-press-event",self.get_width_value)
      self.select_file_file_width_spinner.show()
      
      self.select_file_file_width_hbox.pack_start(self.select_file_file_width_spinner_button)
      self.select_file_file_width_hbox.pack_start(self.select_file_file_width_spinner)
      self.select_file_file_width_hbox.show()
      
      self.select_file_file_height_hbox=gtk.HBox(False,6)
      
      
      self.select_file_file_height_spinner_button=gtk.Button()
      self.select_file_file_height_spinner_button_label=gtk.Label("Height:")
      self.select_file_file_height_spinner_button_label.show()
      self.select_file_file_height_spinner_space=gtk.Label(" ")
      self.select_file_file_height_spinner_space.show()
      self.select_file_file_height_spinner_image=gtk.image_new_from_stock(gtk.STOCK_ZOOM_FIT,4)
      self.select_file_file_height_spinner_image.show()
      self.select_file_file_height_spinner_hbox=gtk.HBox()
      self.select_file_file_height_spinner_hbox.pack_start(self.select_file_file_height_spinner_space,False,False,0)
      self.select_file_file_height_spinner_hbox.pack_start(self.select_file_file_height_spinner_image,False,False,0)
      self.select_file_file_height_spinner_hbox.pack_start(self.select_file_file_height_spinner_button_label,False,False,0)
      self.select_file_file_height_spinner_hbox.show()
      self.select_file_file_height_spinner_button.add(self.select_file_file_height_spinner_hbox)
      self.select_file_file_height_spinner_button.set_relief(gtk.RELIEF_NONE)
      self.select_file_file_height_spinner_button.show()
      
      self.select_file_file_height_spinner_adjustment=gtk.Adjustment(value=self.size[1], lower=0, upper=4096*16, step_incr=1, page_incr=0, page_size=0)
      self.select_file_file_height_spinner=gtk.SpinButton(adjustment=self.select_file_file_height_spinner_adjustment, climb_rate=1, digits=0)
      self.select_file_file_height_spinner.set_tooltip_text("Set the wanted image size height and confirm with Enter.\nYou can apply the ratio height/width to the height value\nby clicking the \"Size ratio\" button.")
      self.select_file_file_height_spinner.set_numeric(True)
      self.select_file_file_height_spinner.set_wrap(False)
      self.select_file_file_height_spinner.connect("value-changed",self.get_height_value)
      self.select_file_file_height_spinner.connect("key-press-event",self.get_height_value)
      self.select_file_file_height_spinner.show()
      
      self.select_file_file_height_hbox.pack_start(self.select_file_file_height_spinner_button)
      self.select_file_file_height_hbox.pack_start(self.select_file_file_height_spinner)
      self.select_file_file_height_hbox.show()
      
      self.select_file_file_width_height_normalize_ratio_button=gtk.Button() 
      self.select_file_file_width_height_normalize_ratio_button_label=gtk.Label(" Size ratio")
      self.select_file_file_width_height_normalize_ratio_button_label.show()
      self.select_file_file_width_height_normalize_ratio_button_space=gtk.Label("")
      self.select_file_file_width_height_normalize_ratio_button_space.show()
      self.select_file_file_width_height_normalize_ratio_image=gtk.image_new_from_stock(gtk.STOCK_ZOOM_100,4)
      self.select_file_file_width_height_normalize_ratio_image.show()
      self.select_file_file_width_height_normalize_ratio_hbox=gtk.HBox()
      self.select_file_file_width_height_normalize_ratio_hbox.pack_start(self.select_file_file_width_height_normalize_ratio_button_space,False,False,0)
      self.select_file_file_width_height_normalize_ratio_hbox.pack_start(self.select_file_file_width_height_normalize_ratio_image,False,False,0)
      self.select_file_file_width_height_normalize_ratio_hbox.pack_start(self.select_file_file_width_height_normalize_ratio_button_label,False,False,0)
      self.select_file_file_width_height_normalize_ratio_hbox.show()
      self.select_file_file_width_height_normalize_ratio_button.add(self.select_file_file_width_height_normalize_ratio_hbox)
      self.select_file_file_width_height_normalize_ratio_button.set_tooltip_text("Compute the ratio width /height in relationship to the given width and height values.\n And in relationship to the selected value to preserve: width or height.")
      self.select_file_file_width_height_normalize_ratio_button.connect("button-press-event",self.ratio_computing)
      self.select_file_file_width_height_normalize_ratio_button.show()
      
      self.select_file_file_width_normalize_ratio_radiobutton=gtk.RadioButton(None, label="Width")
      self.select_file_file_width_normalize_ratio_radiobutton.set_name("Width")
      self.select_file_file_width_normalize_ratio_radiobutton.set_tooltip_text("Preserve the image size width value by ratio computing.")
      self.select_file_file_width_normalize_ratio_radiobutton.connect("button-press-event",self.set_ratio_computing_base)
  
      self.select_file_file_width_normalize_ratio_radiobutton.show()
      
      self.select_file_file_height_normalize_ratio_radiobutton=gtk.RadioButton(self.select_file_file_width_normalize_ratio_radiobutton, label="Height")
      self.select_file_file_height_normalize_ratio_radiobutton.set_name("Height")
      self.select_file_file_height_normalize_ratio_radiobutton.set_tooltip_text("Preserve the image size height value by ratio computing.")
      self.select_file_file_height_normalize_ratio_radiobutton.connect("button-press-event",self.set_ratio_computing_base)
      self.select_file_file_height_normalize_ratio_radiobutton.show()
      
      self.select_file_file_width_height_hbox.pack_start(self.select_file_file_width_hbox, expand=False, fill=True, padding=1)
      self.select_file_file_width_height_hbox.pack_start(self.select_file_file_height_hbox, expand=False, fill=True, padding=1)
      self.select_file_file_width_height_hbox.pack_start(self.select_file_file_width_height_normalize_ratio_button, expand=True, fill=True, padding=1)
      self.select_file_file_width_height_hbox.pack_start(self.select_file_file_width_normalize_ratio_radiobutton, expand=False, fill=True, padding=1)
      self.select_file_file_width_height_hbox.pack_start(self.select_file_file_height_normalize_ratio_radiobutton, expand=False, fill=True, padding=1)
      self.select_file_file_width_height_hbox.show()      
      
      self.select_file_file_buttonbox=gtk.HBox(True,1)
      
      self.select_file_file_buttonbox.set_homogeneous(False)
      self.select_file_file_buttonbox.pack_start(self.select_file_file_cancel_button, expand=False, fill=True, padding=0)
      self.select_file_file_buttonbox.pack_start(self.select_file_file_width_height_hbox, expand=False, fill=True, padding=2)
      self.select_file_file_buttonbox.pack_start(self.select_file_file_ok_button, expand=False, fill=True, padding=0)
      self.select_file_file_buttonbox.show()
      
      
      self.select_file_file_vbox=gtk.VBox(True,4)
      self.select_file_file_vbox.pack_start(self.select_file_file_buttonbox)
      self.select_file_file_vbox.show()
      
      self.select_file_file_chooser.set_extra_widget(self.select_file_file_vbox)
      
      self.select_file_file_chooser.set_do_overwrite_confirmation(True)
      
      
      
      self.select_file_action_file_filter_bmp=gtk.FileFilter()
      self.select_file_action_file_filter_bmp.add_pattern("*.bmp")
      self.select_file_action_file_filter_bmp.add_pattern("*.Bmp")
      self.select_file_action_file_filter_bmp.add_pattern("*.BMP")
      self.select_file_action_file_filter_bmp.set_name("format:       *.bmp (Bitmap image file.)                   ")
      self.select_file_action_file_filter_bmp.set_data("extension",".bmp")
      
        
      self.select_file_action_file_filter_gif=gtk.FileFilter()
      self.select_file_action_file_filter_gif.add_pattern("*.gif")
      self.select_file_action_file_filter_gif.add_pattern("*.Gif")
      self.select_file_action_file_filter_gif.add_pattern("*.GIF")
      self.select_file_action_file_filter_gif.set_name("format:       *.gif (Graphics Interchange Format.)         ")
      self.select_file_action_file_filter_gif.set_data("extension",".gif")
      
      
      self.select_file_action_file_filter_jpeg=gtk.FileFilter()
      self.select_file_action_file_filter_jpeg.add_pattern("*.jpg")
      self.select_file_action_file_filter_jpeg.add_pattern("*.Jpg")
      self.select_file_action_file_filter_jpeg.add_pattern("*.JPG")
      self.select_file_action_file_filter_jpeg.add_pattern("*.jpeg")
      self.select_file_action_file_filter_jpeg.add_pattern("*.Jpeg")
      self.select_file_action_file_filter_jpeg.add_pattern("*.JPEG")
      self.select_file_action_file_filter_jpeg.set_name("format:       *.jpeg (Joint Photographic Experts Group.)   ")
      self.select_file_action_file_filter_jpeg.set_data("extension",".jpeg")
      
      
      self.select_file_action_file_filter_pcx=gtk.FileFilter()
      self.select_file_action_file_filter_pcx.add_pattern("*.pcx")
      self.select_file_action_file_filter_pcx.add_pattern("*.Pcx")
      self.select_file_action_file_filter_pcx.add_pattern("*.PCX")
      self.select_file_action_file_filter_pcx.set_name("format:        *.pcx (Pulse Code Modulation.)               ")
      self.select_file_action_file_filter_pcx.set_data("extension",".pcx")
      
      self.select_file_action_file_filter_pdf=gtk.FileFilter()
      self.select_file_action_file_filter_pdf.add_pattern("*.pdf")
      self.select_file_action_file_filter_pdf.add_pattern("*.Pdf")
      self.select_file_action_file_filter_pdf.add_pattern("*.PDF")
      self.select_file_action_file_filter_pdf.set_name("format:        *.pdf (Windows Bitmap.)                      ")
      self.select_file_action_file_filter_pdf.set_data("extension",".pdf")
      
      self.select_file_action_file_filter_png=gtk.FileFilter()
      self.select_file_action_file_filter_png.add_pattern("*.png")
      self.select_file_action_file_filter_png.add_pattern("*.Png")
      self.select_file_action_file_filter_png.add_pattern("*.PNG")
      self.select_file_action_file_filter_png.set_name("format:        *.png (Portable Network Graphics.)           ")
      self.select_file_action_file_filter_png.set_data("extension",".png")
      
      
      self.select_file_action_file_filter_ppm=gtk.FileFilter()
      self.select_file_action_file_filter_ppm.add_pattern("*.ppm")
      self.select_file_action_file_filter_ppm.add_pattern("*.Ppm")
      self.select_file_action_file_filter_ppm.add_pattern("*.PPM")
      self.select_file_action_file_filter_ppm.set_name("format:        *.ppm (Portable pixmap file format.)         ")
      self.select_file_action_file_filter_ppm.set_data("extension",".ppm")
      
      
      self.select_file_action_file_filter_tiff=gtk.FileFilter()
      self.select_file_action_file_filter_tiff.add_pattern("*.tiff")
      self.select_file_action_file_filter_tiff.add_pattern("*.Tiff")
      self.select_file_action_file_filter_tiff.add_pattern("*.TIFF")
      self.select_file_action_file_filter_tiff.set_name("format:       *.tiff (Tag(ged) Image File Format.)         ")
      self.select_file_action_file_filter_tiff.set_data("extension",".tiff")
      
      
      
      self.select_file_action_file_filter_all=gtk.FileFilter()
      self.select_file_action_file_filter_all.add_pattern('*')
      
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_bmp)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_gif)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_jpeg)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_pcx)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_pdf)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_png)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_ppm)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_tiff)
      
      if self.format_str == "bmp" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_bmp)
      elif self.format_str == "gif" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_gif)
      elif self.format_str == "im" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_im)
      elif self.format_str == "jpeg" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_jpeg)  
      elif self.format_str == "msp" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_msp)
      elif self.format_str == "pdf" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_pdf)
      elif self.format_str == "png" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_png)
      elif self.format_str == "ppm" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_ppm)
      elif self.format_str == "tiff" :
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_tiff)
      else :  
        self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_all)     
        
      self.select_file_file_chooser.set_current_folder(expanduser("~"))
      self.select_file_file_chooser.set_preview_widget_active(True)
      self.select_file_file_chooser.set_use_preview_label(True)
      
      
      self.select_file_file_chooser.connect("update-preview",self.select_file_operation_update_selection)
      
      self.select_file_file_chooser.show()
      
      self.select_file_toplevel.add(self.select_file_file_chooser)
      self.select_file_toplevel.show()
      

      self.filepath_to_return = False
      
      gtk.main()
      
      return self.filepath_to_return

  def get_width_value(self,widget,event=False) :
    self.size[0]=int(widget.get_value())
    self.bool_compute_ratio=False
    
  def get_height_value(self,widget,event=False) :
    self.size[1]=int(widget.get_value())
    self.bool_compute_ratio=False
    
  def set_width_value(self) :
    self.select_file_file_width_spinner.set_value(self.size[0])
    self.bool_change_size=True
    
  def set_height_value(self) :
    self.select_file_file_height_spinner.set_value(self.size[1])
    self.bool_change_size=True
  
  def set_ratio_computing_base(self,widget,event) :
    if widget.get_name() == "Width" :
      
      self.ratio_factor_choice="Width"
      
    elif widget.get_name() == "Height" :
      
      self.ratio_factor_choice="Height"
      
  def ratio_computing(self,widget,event) :
    if not self.bool_compute_ratio :
      if self.ratio_factor_choice == "Width" :
        self.get_width_value(self.select_file_file_width_spinner)
        self.size[1]=int(self.size[0]*self.width_factor)
        self.bool_change_size=True
      elif self.ratio_factor_choice == "Height" :
        self.get_height_value(self.select_file_file_height_spinner)
        self.size[0]=int(self.size[1]*self.height_factor)
        self.bool_change_size=True
      self.bool_compute_ratio=True  
      self.set_height_value()  
      self.set_width_value()
    
    
    
  def select_file_operation_toplevel_ok(self,widget,event) :
    if not self.select_file_file_chooser.get_filename() :
      return 
    if isdir(self.select_file_file_chooser.get_filename()) :
      return False
    
    if self.select_file_file_chooser.get_filename().lower().endswith(".bmp") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_bmp)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".gif") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_gif)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".jpeg") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_jpeg)  
    elif self.select_file_file_chooser.get_filename().lower().endswith(".pcx") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_pcx) 
    elif self.select_file_file_chooser.get_filename().lower().endswith(".pdf") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_pdf)  
    elif self.select_file_file_chooser.get_filename().lower().endswith(".png") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_png)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".ppm") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_ppm)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".tiff") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_tiff)
    
    self.format_str=self.select_file_file_chooser.get_filter().get_data("extension")
    if not self.filepath_to_return :
      
      self.filepath_to_return = self.select_file_file_chooser.get_filename()
      
      if self.bool_change_size :
        self.processing_instance=self.processing_instance.resize((self.size[0],self.size[1]))
      
      if self.format_src != self.format_str :
        self.processing_instance=self.processing_instance.convert(self.mode)
      
      if not self.user_has_set_extension() and not self.filepath_to_return.endswith('.'):
        self.filepath_to_return=self.filepath_to_return+self.select_file_file_chooser.get_filter().get_data("extension") 
      
      elif not self.user_has_set_extension() and self.filepath_to_return.endswith('.') :
        self.filepath_to_return=self.filepath_to_return+self.select_file_file_chooser.get_filter().get_data("extension")[1::]
      
      try :
        self.processing_instance.save(self.filepath_to_return,format=self.format_str[1::].upper())
      except :
	try :
	  self.processing_instance=self.processing_instance.convert("RGB")
	  self.processing_instance.save(self.filepath_to_return,format=self.format_str[1::].upper())
	except :
	  self.create_image_saving_error_dialog(self.filepath_to_return,self.format_str[1::].lower())
	  return False
	  
    else :
      
      self.filepath_to_return = self.select_file_file_chooser.get_filename()
      
      if self.bool_change_size :
        self.processing_instance=self.processing_instance.resize((self.size[0],self.size[1]))
      
      if self.format_src != self.format_str :
        self.processing_instance=self.processing_instance.convert(self.mode)
        
      if not self.user_has_set_extension() and not self.filepath_to_return.endswith('.') :
        self.filepath_to_return=self.filepath_to_return+self.select_file_file_chooser.get_filter().get_data("extension")
      
      elif not self.user_has_set_extension() and self.filepath_to_return.endswith('.') :
        self.filepath_to_return=self.filepath_to_return+self.select_file_file_chooser.get_filter().get_data("extension")[1::]
      
      try :
        self.processing_instance.save(self.filepath_to_return,format=self.format_str[1::].upper())
      except :
	try :
	  self.processing_instance=self.processing_instance.convert("RGB")
	  self.processing_instance.save(self.filepath_to_return,format=self.format_str[1::].upper())
	except :
	  self.create_image_saving_error_dialog(self.filepath_to_return,self.format_str[1::].lower())
	  return False
	
    closed(self.select_file_toplevel,False) 
  
  def user_has_set_extension(self) :
    if self.select_file_file_chooser.get_filename().lower().endswith(".bmp") or self.select_file_file_chooser.get_filename().lower().endswith(".gif") or self.select_file_file_chooser.get_filename().lower().endswith(".jpeg") or self.select_file_file_chooser.get_filename().lower().endswith(".pdf")  or self.select_file_file_chooser.get_filename().lower().endswith(".pcx") or self.select_file_file_chooser.get_filename().lower().endswith(".png") or self.select_file_file_chooser.get_filename().lower().endswith(".ppm") or  self.select_file_file_chooser.get_filename().lower().endswith(".tiff")  :
      return True
    else :
      return False
  
  def select_file_operation_toplevel_cancel(self,widget,event) :
    closed(self.select_file_toplevel,False)
    
  def select_file_operation_update_selection(self,widget,event=False) :
    if not self.select_file_file_chooser.get_filename() :
      return 
    
    if self.select_file_file_chooser.get_filename().lower().endswith(self.select_file_file_chooser.get_filter().get_data("extension")) :
      self.filepath_to_return = self.select_file_file_chooser.get_filename()
    
    elif self.select_file_file_chooser.get_filename().lower().endswith(".bmp") or self.select_file_file_chooser.get_filename().lower().endswith(".gif") or self.select_file_file_chooser.get_filename().lower().endswith(".jpeg") or self.select_file_file_chooser.get_filename().lower().endswith(".pdf")  or self.select_file_file_chooser.get_filename().lower().endswith(".pcx") or self.select_file_file_chooser.get_filename().lower().endswith(".png") or self.select_file_file_chooser.get_filename().lower().endswith(".ppm") or self.select_file_file_chooser.get_filename().lower().endswith(".tiff") :
      self.filepath_to_return = self.select_file_file_chooser.get_filename()
      
    else :
      if self.select_file_file_chooser.get_filename().endswith('.') :
        self.filepath_to_return=self.select_file_file_chooser.get_filename()[::-1]
      else :
        if isdir(self.select_file_file_chooser.get_filename()) :
          if not self.select_file_file_chooser.get_filename().lower().endswith(self.select_file_file_chooser.get_filter().get_data("extension")) :
            self.filepath_to_return=self.select_file_file_chooser.get_filename()
        else :
          self.filepath_to_return=""
    
    
    
    if self.select_file_file_chooser.get_filename().lower().endswith(".bmp") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_bmp)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".gif") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_gif)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".jpeg") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_jpeg)  
    elif self.select_file_file_chooser.get_filename().lower().endswith(".pcx") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_pcx) 
    elif self.select_file_file_chooser.get_filename().lower().endswith(".pdf") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_pdf)    
    elif self.select_file_file_chooser.get_filename().lower().endswith(".png") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_png)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".ppm") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_ppm)
    elif self.select_file_file_chooser.get_filename().lower().endswith(".tiff") :
      self.select_file_file_chooser.set_property("filter",self.select_file_action_file_filter_tiff)
    
    self.format_str=self.select_file_file_chooser.get_filter().get_data("extension")  
    
  def create_image_saving_error_dialog(self,filepath,file_format) :
    self.error_image_saving_image=gtk.MessageDialog(parent=self.select_file_toplevel, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=None)
    self.error_image_saving_image.set_markup("Failed to save image: \n%s\nin format: %s \nUse another file format !!!" % (basename(filepath),file_format) ) 
    self.error_image_saving_image_image=gtk.image_new_from_stock(gtk.STOCK_DIALOG_ERROR,4)
    self.error_image_saving_image_image.show()
    self.error_image_saving_image.set_image(self.error_image_saving_image_image)
    
    
    self.error_image_saving_image.run()    
    self.error_image_saving_image.destroy() 
    
  def get_style(self) :
      style=gtk.Style()
      return  style 
 
def closed(widget,event) :
    widget.destroy() 
    
    gtk.main_quit() 
 
