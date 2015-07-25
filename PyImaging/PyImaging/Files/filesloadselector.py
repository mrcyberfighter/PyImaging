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

from os.path import expanduser,isfile,isdir,basename
 
class File_Loading_Selector() : 
  
  def __init__(self,load_ext=False,img_mask=False) :
    self.load_file_mergin_supported_extension=load_ext
    self.load_file_mergin_supported_as_mask=img_mask
    
  def select_file(self) :
      
      self.select_file_toplevel=gtk.Window(type=gtk.WINDOW_TOPLEVEL)
      self.select_file_toplevel.connect("delete_event",self.select_file_operation_toplevel_cancel)
      self.select_file_toplevel.set_title("Select image file to load.")
      self.select_file_toplevel.set_size_request(768+128-16-8,256+256+64)
      self.select_file_toplevel.set_resizable(False)
        
      self.select_file_file_chooser=gtk.FileChooserWidget(action=gtk.FILE_CHOOSER_ACTION_OPEN, backend=None)
      self.select_file_file_chooser.connect("selection-changed",self.select_file_operation_update_selection)
      self.select_file_file_chooser.connect("file-activated",self.select_file_operation_update_selection)
      
      self.select_file_file_ok_button=gtk.Button()
      self.select_file_file_ok_button_label=gtk.Label("    Confirm")
      self.select_file_file_ok_button_label.show()
      self.select_file_file_ok_button_space=gtk.Label("      ")
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
      self.select_file_file_ok_button.set_size_request(128+16+4,32)
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
      
      
      self.select_file_file_entry=gtk.Entry(0)
      self.select_file_file_entry.set_can_focus(False)
      self.select_file_file_entry.set_width_chars(62)
      self.select_file_file_entry.set_text("")
      self.select_file_file_entry.set_alignment(0.5)
      self.select_file_file_entry.show()
      
      
      
      self.select_file_file_hbox=gtk.HBox(False,0)
      self.select_file_file_hbox.pack_start(self.select_file_file_cancel_button,False,True,0)
      self.select_file_file_hbox.pack_start(self.select_file_file_entry,False,True,0)
      self.select_file_file_hbox.pack_start(self.select_file_file_ok_button,False,True,4)
      
      self.select_file_file_hbox.set_border_width(4)
      self.select_file_file_hbox.show()
      
      self.select_file_file_chooser.set_extra_widget(self.select_file_file_hbox)
      
      self.select_file_file_chooser.set_do_overwrite_confirmation(True)
      
      
      
      self.select_file_action_file_filter_bmp=gtk.FileFilter()
      self.select_file_action_file_filter_bmp.add_pattern("*.bmp")
      self.select_file_action_file_filter_bmp.add_pattern("*.Bmp")
      self.select_file_action_file_filter_bmp.add_pattern("*.BMP")
      self.select_file_action_file_filter_bmp.set_name("format:       *.bmp (Bitmap image file.)                   ")
      
      
      if self.load_file_mergin_supported_extension :
      
	self.select_file_action_file_filter_gif=gtk.FileFilter()
	self.select_file_action_file_filter_gif.add_pattern("*.gif")
	self.select_file_action_file_filter_gif.add_pattern("*.Gif")
	self.select_file_action_file_filter_gif.add_pattern("*.GIF")
	self.select_file_action_file_filter_gif.set_name("format:       *.gif (Graphics Interchange Format.)         ")
	
      
      
      self.select_file_action_file_filter_jpg=gtk.FileFilter()
      self.select_file_action_file_filter_jpg.add_pattern("*.jpg")
      self.select_file_action_file_filter_jpg.add_pattern("*.Jpg")
      self.select_file_action_file_filter_jpg.add_pattern("*.JPG")
      self.select_file_action_file_filter_jpg.add_pattern("*.jpeg")
      self.select_file_action_file_filter_jpg.add_pattern("*.Jpeg")
      self.select_file_action_file_filter_jpg.add_pattern("*.JPEG")
      self.select_file_action_file_filter_jpg.set_name("format:        *.jpeg (Joint Photographic Experts Group.)  ")
      
      
      self.select_file_action_file_filter_pcx=gtk.FileFilter()
      self.select_file_action_file_filter_pcx.add_pattern("*.pcx")
      self.select_file_action_file_filter_pcx.add_pattern("*.Pcx")
      self.select_file_action_file_filter_pcx.add_pattern("*.PCX")
      self.select_file_action_file_filter_pcx.set_name("format:        *.pcx (Pulse Code Modulation.)              ")
      
      
      self.select_file_action_file_filter_pdf=gtk.FileFilter()
      self.select_file_action_file_filter_pdf.add_pattern("*.pdf")
      self.select_file_action_file_filter_pdf.add_pattern("*.Pdf")
      self.select_file_action_file_filter_pdf.add_pattern("*.PDF")
      self.select_file_action_file_filter_pdf.set_name("format:        *.pdf (Windows Bitmap.)                      ")
      
      self.select_file_action_file_filter_png=gtk.FileFilter()
      self.select_file_action_file_filter_png.add_pattern("*.png")
      self.select_file_action_file_filter_png.add_pattern("*.Png")
      self.select_file_action_file_filter_png.add_pattern("*.PNG")
      self.select_file_action_file_filter_png.set_name("format:        *.png (Portable Network Graphics.)          ")
      
      
      self.select_file_action_file_filter_ppm=gtk.FileFilter()
      self.select_file_action_file_filter_ppm.add_pattern("*.ppm")
      self.select_file_action_file_filter_ppm.add_pattern("*.Ppm")
      self.select_file_action_file_filter_ppm.add_pattern("*.PPM")
      self.select_file_action_file_filter_ppm.set_name("format:        *.ppm (Portable pixmap file format.)         ")
      
      
      self.select_file_action_file_filter_tiff=gtk.FileFilter()
      self.select_file_action_file_filter_tiff.add_pattern("*.tiff")
      self.select_file_action_file_filter_tiff.add_pattern("*.tif")
      self.select_file_action_file_filter_tiff.add_pattern("*.Tiff")
      self.select_file_action_file_filter_tiff.add_pattern("*.Tif")
      self.select_file_action_file_filter_tiff.add_pattern("*.TIFF")
      self.select_file_action_file_filter_tiff.add_pattern("*.TIF")
      self.select_file_action_file_filter_tiff.set_name("format:        *.tiff (Tag(ged) Image File Format.)         ")
      
      
      if self.load_file_mergin_supported_as_mask :
      
	self.select_file_action_file_filter_xbm=gtk.FileFilter()
	self.select_file_action_file_filter_xbm.add_pattern("*.xbm")
	self.select_file_action_file_filter_xbm.add_pattern("*.Xbm")
	self.select_file_action_file_filter_xbm.add_pattern("*.XBM")
	self.select_file_action_file_filter_xbm.set_name("format:        *.xbm (X BitMap.)                             ")
	
      
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_bmp)
      if self.load_file_mergin_supported_extension :
        self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_gif)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_jpg)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_pcx)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_pdf)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_png)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_ppm)
      self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_tiff)
      if self.load_file_mergin_supported_as_mask :
        self.select_file_file_chooser.add_filter(self.select_file_action_file_filter_xbm)
      
      self.select_file_file_chooser.set_current_folder(expanduser("~"))
      self.select_file_file_chooser.set_preview_widget_active(True)
      self.select_file_file_chooser.set_use_preview_label(True)
      self.select_file_file_chooser.show()
      
      self.select_file_toplevel.add(self.select_file_file_chooser)
      self.select_file_toplevel.show()
      
      self.filepath_to_return = False
      
      gtk.main()
      
      return self.filepath_to_return


  def select_file_operation_toplevel_ok(self,widget,event) :
    if isdir(self.select_file_file_chooser.get_filename()) :
      return False
    
    self.filepath_to_return = self.select_file_file_chooser.get_filename()
    closed(self.select_file_toplevel,False) 
    
  def select_file_operation_toplevel_cancel(self,widget,event) :
    closed(self.select_file_toplevel,False)
    
  def select_file_operation_update_selection(self,widget) :
    if not widget.get_filename() :
      return 
    if isfile(widget.get_filename()) :
      self.select_file_file_entry.set_text(basename(widget.get_filename()))
    else :
      self.select_file_file_entry.set_text("")
 
def closed(widget,event) :
    widget.destroy() 
    
    gtk.main_quit() 
 

