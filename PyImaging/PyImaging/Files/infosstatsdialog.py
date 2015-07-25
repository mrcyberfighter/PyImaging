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
  
from PIL import Image,ImageStat  
  

class Informations_dialog() :
  def __init__(self,instance,filename) :
    self.image_instance=instance
    
    self.image_name=basename(filename)
    
    self.user_home=expanduser("~")
  
  
  def get_pixels_info(self) :
    
    if not self.image_instance.mode =="RGB" and not self.image_instance.mode =="RGBA" :
      try :
        self.image_instance=self.image_instance.convert("RGBA")
      except :
        try :
          self.image_instance=self.image_instance.convert("RGB")
        except :
          self.informations_pixels_info_liststore.append(['Bands',"No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Count', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Extrema', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Average', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Median', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['RMS', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Deviation', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Summe', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Square', "No datas", "No datas", "No datas", "No datas"])
          self.informations_pixels_info_liststore.append(['Variance', "No datas", "No datas", "No datas", "No datas"])
          return
        
    pixels_stats=ImageStat.Stat(self.image_instance) 
    
    if self.image_instance.mode =="RGB" :
      self.informations_pixels_info_liststore.append(['Bands',str(pixels_stats.bands[0]), str(pixels_stats.bands[1]), str(pixels_stats.bands[2]),"0"])
      self.informations_pixels_info_liststore.append(['Count', str(pixels_stats._getcount()[0]), str(pixels_stats._getcount()[1]), str(pixels_stats._getcount()[2]),"0"])
      self.informations_pixels_info_liststore.append(['Extrema', str(pixels_stats._getextrema()[0]), str(pixels_stats._getextrema()[1]), str(pixels_stats._getextrema()[2]),"0"])
      self.informations_pixels_info_liststore.append(['Average', str(pixels_stats._getmean()[0]), str(pixels_stats._getmean()[1]), str(pixels_stats._getmean()[2]),"0.0"])
      self.informations_pixels_info_liststore.append(['Median', str(pixels_stats._getmedian()[0]), str(pixels_stats._getmedian()[1]), str(pixels_stats._getmedian()[2]),"0"])
      self.informations_pixels_info_liststore.append(['RMS', str(pixels_stats._getrms()[0]), str(pixels_stats._getrms()[1]), str(pixels_stats._getrms()[2]),"0.0"])
      self.informations_pixels_info_liststore.append(['Deviation', str(pixels_stats._getstddev()[0]), str(pixels_stats._getstddev()[1]), str(pixels_stats._getstddev()[2]),"0.0"])
      self.informations_pixels_info_liststore.append(['Summe', str(pixels_stats._getsum()[0]), str(pixels_stats._getsum()[1]), str(pixels_stats._getsum()[2]),"0"])
      self.informations_pixels_info_liststore.append(['Square', str(pixels_stats._getsum2()[0]), str(pixels_stats._getsum2()[1]), str(pixels_stats._getsum2()[2]),"0"])
      self.informations_pixels_info_liststore.append(['Variance', str(pixels_stats._getvar()[0]), str(pixels_stats._getvar()[1]), str(pixels_stats._getvar()[2]),"0"])

    elif self.image_instance.mode =="RGBA" :
      self.informations_pixels_info_liststore.append(['Bands',str(pixels_stats.bands[0]), str(pixels_stats.bands[1]), str(pixels_stats.bands[2]), str(pixels_stats.bands[3])])
      self.informations_pixels_info_liststore.append(['Count', str(pixels_stats._getcount()[0]), str(pixels_stats._getcount()[1]), str(pixels_stats._getcount()[2]), str(pixels_stats._getcount()[3])])
      self.informations_pixels_info_liststore.append(['Extrema', str(pixels_stats._getextrema()[0]), str(pixels_stats._getextrema()[1]), str(pixels_stats._getextrema()[2]), str(pixels_stats._getextrema()[3])])
      self.informations_pixels_info_liststore.append(['Average', str(pixels_stats._getmean()[0]), str(pixels_stats._getmean()[1]), str(pixels_stats._getmean()[2]), str(pixels_stats._getmean()[3])])
      self.informations_pixels_info_liststore.append(['Median', str(pixels_stats._getmedian()[0]), str(pixels_stats._getmedian()[1]), str(pixels_stats._getmedian()[2]), str(pixels_stats._getmedian()[3])])
      self.informations_pixels_info_liststore.append(['RMS', str(pixels_stats._getrms()[0]), str(pixels_stats._getrms()[1]), str(pixels_stats._getrms()[2]), str(pixels_stats._getrms()[3])])
      self.informations_pixels_info_liststore.append(['Deviation', str(pixels_stats._getstddev()[0]), str(pixels_stats._getstddev()[1]), str(pixels_stats._getstddev()[2]), str(pixels_stats._getstddev()[3])])
      self.informations_pixels_info_liststore.append(['Summe', str(pixels_stats._getsum()[0]), str(pixels_stats._getsum()[1]), str(pixels_stats._getsum()[2]), str(pixels_stats._getsum()[3])])
      self.informations_pixels_info_liststore.append(['Square', str(pixels_stats._getsum2()[0]), str(pixels_stats._getsum2()[1]), str(pixels_stats._getsum2()[2]), str(pixels_stats._getsum2()[3])])
      self.informations_pixels_info_liststore.append(['Variance', str(pixels_stats._getvar()[0]), str(pixels_stats._getvar()[1]), str(pixels_stats._getvar()[2]), str(pixels_stats._getvar()[3])])
      
          
    
          
        
    
  def create_dialog(self) :
    
    self.informations_dialog=gtk.Dialog("Image file informations.",None,0, None)
    
    self.informations_dialog.connect("delete_event",closed)
    
    self.informations_dialog.set_size_request(512+128,512+128-40)
    self.informations_dialog.modify_bg(gtk.STATE_NORMAL,self.informations_dialog.get_colormap().alloc_color('#d0d0d0'))
    
    self.informations_area_vbox=self.informations_dialog.get_content_area()
    
    self.informations_main_info_frame=gtk.Frame()
    self.informations_main_info_frame.set_border_width(5)
    self.informations_main_info_frame_label_button=gtk.Button()
    self.informations_main_info_frame_label_button_label=gtk.Label("  Main informations")
    self.informations_main_info_frame_label_button_label.show()
    self.informations_main_info_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_INFO,2)
    self.informations_main_info_frame_label_button_image.show()
    self.informations_main_info_frame_label_button_hbox=gtk.HBox()
    self.informations_main_info_frame_label_button_hbox.pack_start(self.informations_main_info_frame_label_button_image,False,False,0)
    self.informations_main_info_frame_label_button_hbox.pack_start(self.informations_main_info_frame_label_button_label,False,False,0)
    self.informations_main_info_frame_label_button_hbox.show()
    self.informations_main_info_frame_label_button.add(self.informations_main_info_frame_label_button_hbox)
    self.informations_main_info_frame_label_button.set_can_focus(False)
    self.informations_main_info_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.informations_main_info_frame_label_button.show()
    self.informations_main_info_frame.set_label_widget(self.informations_main_info_frame_label_button)
    
    self.informations_main_info_vbox=gtk.VBox()
    self.informations_main_info_vbox.set_border_width(5)
    
    self.informations_main_info_filename_hbox=gtk.HBox()
    
    self.informations_main_info_filename_label_button=gtk.Button()
    self.informations_main_info_filename_label_button_label=gtk.Label("  Filename ")
    self.informations_main_info_filename_label_button_label.show()
    self.informations_main_info_filename_label_button_space=gtk.Label(" ")
    self.informations_main_info_filename_label_button_space.show()
    self.informations_main_info_filename_label_button_image=gtk.image_new_from_stock(gtk.STOCK_FILE,2)
    self.informations_main_info_filename_label_button_image.show()
    self.informations_main_info_filename_label_button_hbox=gtk.HBox()
    self.informations_main_info_filename_label_button_hbox.pack_start(self.informations_main_info_filename_label_button_space,False,False,0)
    self.informations_main_info_filename_label_button_hbox.pack_start(self.informations_main_info_filename_label_button_image,False,False,0)
    self.informations_main_info_filename_label_button_hbox.pack_start(self.informations_main_info_filename_label_button_label,False,False,0)
    self.informations_main_info_filename_label_button_hbox.show()
    self.informations_main_info_filename_label_button.add(self.informations_main_info_filename_label_button_hbox)
    self.informations_main_info_filename_label_button.show()
    
    self.informations_main_info_filename_entry=gtk.Entry()
    self.informations_main_info_filename_entry.set_alignment(0.5)
    self.informations_main_info_filename_entry.set_text(self.image_name)
    self.informations_main_info_filename_entry.show()
    
    self.informations_main_info_filename_hbox.pack_start(self.informations_main_info_filename_label_button,False,False,5)
    self.informations_main_info_filename_hbox.pack_start(self.informations_main_info_filename_entry,True,True,5)
    self.informations_main_info_filename_hbox.show()
    
    self.informations_main_info_format_hbox=gtk.HBox()
    
    
    
    self.informations_main_info_format_label_button=gtk.Button()
    self.informations_main_info_format_label_button_label=gtk.Label("  Format    ")
    self.informations_main_info_format_label_button_label.show()
    self.informations_main_info_format_label_button_space=gtk.Label(" ")
    self.informations_main_info_format_label_button_space.show()
    self.informations_main_info_format_label_button_image=gtk.image_new_from_stock(gtk.STOCK_LEAVE_FULLSCREEN,2)
    self.informations_main_info_format_label_button_image.show()
    self.informations_main_info_format_label_button_hbox=gtk.HBox()
    self.informations_main_info_format_label_button_hbox.pack_start(self.informations_main_info_format_label_button_space,False,False,0)
    self.informations_main_info_format_label_button_hbox.pack_start(self.informations_main_info_format_label_button_image,False,False,0)
    self.informations_main_info_format_label_button_hbox.pack_start(self.informations_main_info_format_label_button_label,False,False,0)
    self.informations_main_info_format_label_button_hbox.show()
    self.informations_main_info_format_label_button.add(self.informations_main_info_format_label_button_hbox)
    self.informations_main_info_format_label_button.show()
    
    self.informations_main_info_format_entry=gtk.Entry()
    self.informations_main_info_format_entry.set_alignment(0.5)
    self.informations_main_info_format_entry.set_text(basename(self.image_instance.format.lower()))
    self.informations_main_info_format_entry.show()
    
    self.informations_main_info_format_description_entry=gtk.Entry()
    self.informations_main_info_format_description_entry.set_alignment(0.5)
    self.informations_main_info_format_description_entry.set_text(self.image_instance.format_description)
    self.informations_main_info_format_description_entry.show()
    
    self.informations_main_info_format_hbox.pack_start(self.informations_main_info_format_label_button,False,False,5)
    self.informations_main_info_format_hbox.pack_start(self.informations_main_info_format_entry,False,False,5)
    self.informations_main_info_format_hbox.pack_start(self.informations_main_info_format_description_entry,True,True,5)
    self.informations_main_info_format_hbox.show()
    
    self.informations_main_info_size_hbox=gtk.HBox()
    
    self.informations_main_info_size_label_button=gtk.Button()
    self.informations_main_info_size_label_button_label=gtk.Label("  Size         ")
    self.informations_main_info_size_label_button_label.show()
    self.informations_main_info_size_label_button_space=gtk.Label(" ")
    self.informations_main_info_size_label_button_space.show()
    self.informations_main_info_size_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PAGE_SETUP,2)
    self.informations_main_info_size_label_button_image.show()
    self.informations_main_info_size_label_button_hbox=gtk.HBox()
    self.informations_main_info_size_label_button_hbox.pack_start(self.informations_main_info_size_label_button_space,False,False,0)
    self.informations_main_info_size_label_button_hbox.pack_start(self.informations_main_info_size_label_button_image,False,False,0)
    self.informations_main_info_size_label_button_hbox.pack_start(self.informations_main_info_size_label_button_label,False,False,0)
    self.informations_main_info_size_label_button_hbox.show()
    self.informations_main_info_size_label_button.add(self.informations_main_info_size_label_button_hbox)
    self.informations_main_info_size_label_button.show()
    
    self.informations_main_info_size_width_label_button=gtk.Button()
    self.informations_main_info_size_width_label_button_label=gtk.Label(" Width")
    self.informations_main_info_size_width_label_button_label.show()
    self.informations_main_info_size_width_label_button_space=gtk.Label(" ")
    self.informations_main_info_size_width_label_button_space.show()
    self.informations_main_info_size_width_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PAGE_SETUP,2)
    self.informations_main_info_size_width_label_button_image.show()
    self.informations_main_info_size_width_label_button_hbox=gtk.HBox()
    self.informations_main_info_size_width_label_button_hbox.pack_start(self.informations_main_info_size_width_label_button_space,False,False,0)
    self.informations_main_info_size_width_label_button_hbox.pack_start(self.informations_main_info_size_width_label_button_image,False,False,0)
    self.informations_main_info_size_width_label_button_hbox.pack_start(self.informations_main_info_size_width_label_button_label,False,False,0)
    self.informations_main_info_size_width_label_button_hbox.show()
    self.informations_main_info_size_width_label_button.add(self.informations_main_info_size_width_label_button_hbox)
    self.informations_main_info_size_width_label_button.show()
    
    self.informations_main_info_size_width_entry=gtk.Entry()
    self.informations_main_info_size_width_entry.set_alignment(0.5)
    self.informations_main_info_size_width_entry.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.informations_main_info_size_width_entry.set_text(str(self.image_instance.size[0])+" px")
    self.informations_main_info_size_width_entry.show()
    
    self.informations_main_info_size_height_label_button=gtk.Button()
    self.informations_main_info_size_height_label_button_label=gtk.Label(" Height")
    self.informations_main_info_size_height_label_button_label.show()
    self.informations_main_info_size_height_label_button_space=gtk.Label(" ")
    self.informations_main_info_size_height_label_button_space.show()
    self.informations_main_info_size_height_label_button_image=gtk.image_new_from_stock(gtk.STOCK_PAGE_SETUP,2)
    self.informations_main_info_size_height_label_button_image.show()
    self.informations_main_info_size_height_label_button_hbox=gtk.HBox()
    self.informations_main_info_size_height_label_button_hbox.pack_start(self.informations_main_info_size_height_label_button_space,False,False,0)
    self.informations_main_info_size_height_label_button_hbox.pack_start(self.informations_main_info_size_height_label_button_image,False,False,0)
    self.informations_main_info_size_height_label_button_hbox.pack_start(self.informations_main_info_size_height_label_button_label,False,False,0)
    self.informations_main_info_size_height_label_button_hbox.show()
    self.informations_main_info_size_height_label_button.add(self.informations_main_info_size_height_label_button_hbox)
    self.informations_main_info_size_height_label_button.show()
    
    self.informations_main_info_size_height_entry=gtk.Entry()
    self.informations_main_info_size_height_entry.set_alignment(0.5)
    self.informations_main_info_size_height_entry.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_PAGE_SETUP)
    self.informations_main_info_size_height_entry.set_text(str(self.image_instance.size[1])+" px")
    self.informations_main_info_size_height_entry.show()
    
    self.informations_main_info_size_hbox.pack_start(self.informations_main_info_size_label_button,False,False,5)
    self.informations_main_info_size_hbox.pack_start(self.informations_main_info_size_width_label_button,True,False,5)
    self.informations_main_info_size_hbox.pack_start(self.informations_main_info_size_width_entry,True,False,5)
    self.informations_main_info_size_hbox.pack_start(self.informations_main_info_size_height_label_button,True,False,5)
    self.informations_main_info_size_hbox.pack_start(self.informations_main_info_size_height_entry,True,False,5)
    self.informations_main_info_size_hbox.show()
    
    self.informations_main_info_vbox.pack_start(self.informations_main_info_filename_hbox,False,False,5)
    self.informations_main_info_vbox.pack_start(self.informations_main_info_format_hbox,False,False,5)
    self.informations_main_info_vbox.pack_start(self.informations_main_info_size_hbox,False,False,5)
    self.informations_main_info_vbox.show()
    
    self.informations_main_info_frame.add(self.informations_main_info_vbox)
    self.informations_main_info_frame.show()
    
    self.informations_pixels_info_frame=gtk.Frame()
    self.informations_pixels_info_frame.set_border_width(5)
    self.informations_pixels_info_frame_label_button=gtk.Button()
    self.informations_pixels_info_frame_label_button_label=gtk.Label("  Pixels informations")
    self.informations_pixels_info_frame_label_button_label.show()
    self.informations_pixels_info_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_LEAVE_FULLSCREEN,2)
    self.informations_pixels_info_frame_label_button_image.show()
    self.informations_pixels_info_frame_label_button_hbox=gtk.HBox()
    self.informations_pixels_info_frame_label_button_hbox.pack_start(self.informations_pixels_info_frame_label_button_image,False,False,0)
    self.informations_pixels_info_frame_label_button_hbox.pack_start(self.informations_pixels_info_frame_label_button_label,False,False,0)
    self.informations_pixels_info_frame_label_button_hbox.show()
    self.informations_pixels_info_frame_label_button.add(self.informations_pixels_info_frame_label_button_hbox)
    self.informations_pixels_info_frame_label_button.set_can_focus(False)
    self.informations_pixels_info_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.informations_pixels_info_frame_label_button.show()
    self.informations_pixels_info_frame.set_label_widget(self.informations_pixels_info_frame_label_button)
    
    self.informations_pixels_info_adjustment=gtk.Adjustment(value=0,lower=0.0,upper=1.0,step_incr=0.1,page_incr=0,page_size=0) 
    self.informations_pixels_info_scrolled_window=gtk.ScrolledWindow(hadjustment=self.informations_pixels_info_adjustment)
    self.informations_pixels_info_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    self.informations_pixels_info_scrolled_window.set_size_request(512-128,128+32) 
    self.informations_pixels_info_scrolled_window.set_border_width(5)
    
    self.informations_pixels_info_liststore=gtk.ListStore(str,str,str,str,str)
    
    self.informations_pixels_info_treeview=gtk.TreeView(self.informations_pixels_info_liststore)
    
    
    
    self.get_pixels_info()
    
    self.informations_pixels_info_tvcolumn0 = gtk.TreeViewColumn('Data')
    self.informations_pixels_info_tvcolumn1 = gtk.TreeViewColumn('Red')
    self.informations_pixels_info_tvcolumn2 = gtk.TreeViewColumn('Green')
    self.informations_pixels_info_tvcolumn3 = gtk.TreeViewColumn('Blue')
    self.informations_pixels_info_tvcolumn4 = gtk.TreeViewColumn('Alpha')
    
    self.informations_pixels_info_tvcolumn0.set_resizable(True)
    self.informations_pixels_info_tvcolumn1.set_resizable(True)
    self.informations_pixels_info_tvcolumn2.set_resizable(True)
    self.informations_pixels_info_tvcolumn3.set_resizable(True)
    self.informations_pixels_info_tvcolumn4.set_resizable(True)
    
    self.informations_pixels_info_treeview.append_column(self.informations_pixels_info_tvcolumn0)
    self.informations_pixels_info_treeview.append_column(self.informations_pixels_info_tvcolumn1)
    self.informations_pixels_info_treeview.append_column(self.informations_pixels_info_tvcolumn2)
    self.informations_pixels_info_treeview.append_column(self.informations_pixels_info_tvcolumn3)
    self.informations_pixels_info_treeview.append_column(self.informations_pixels_info_tvcolumn4)

    

    self.informations_pixels_info_cell0 = gtk.CellRendererText()
    self.informations_pixels_info_cell1 = gtk.CellRendererText()
    self.informations_pixels_info_cell2 = gtk.CellRendererText()
    self.informations_pixels_info_cell3 = gtk.CellRendererText()
    self.informations_pixels_info_cell4 = gtk.CellRendererText()

    self.informations_pixels_info_cell0.set_property('cell-background', '#c0c0c0')
    self.informations_pixels_info_cell1.set_property('cell-background', '#ff0000')
    self.informations_pixels_info_cell2.set_property('cell-background', '#00ff00')
    self.informations_pixels_info_cell3.set_property('cell-background', '#0000ff')
    self.informations_pixels_info_cell4.set_property('cell-background', '#f0f0f0')

    self.informations_pixels_info_tvcolumn0.pack_start(self.informations_pixels_info_cell0, False)
    self.informations_pixels_info_tvcolumn1.pack_start(self.informations_pixels_info_cell1, True)
    self.informations_pixels_info_tvcolumn2.pack_start(self.informations_pixels_info_cell2, True)
    self.informations_pixels_info_tvcolumn3.pack_start(self.informations_pixels_info_cell3, True)
    self.informations_pixels_info_tvcolumn4.pack_start(self.informations_pixels_info_cell4, True)

    self.informations_pixels_info_tvcolumn0.set_attributes(self.informations_pixels_info_cell0, text=0)
    self.informations_pixels_info_tvcolumn1.set_attributes(self.informations_pixels_info_cell1, text=1)
    self.informations_pixels_info_tvcolumn2.set_attributes(self.informations_pixels_info_cell2, text=2)
    self.informations_pixels_info_tvcolumn3.set_attributes(self.informations_pixels_info_cell3, text=3)
    self.informations_pixels_info_tvcolumn4.set_attributes(self.informations_pixels_info_cell4, text=4)

    self.informations_pixels_info_treeview.show()

    self.informations_pixels_info_scrolled_window.add_with_viewport(self.informations_pixels_info_treeview)

    self.informations_pixels_info_scrolled_window.show()
    
    self.informations_pixels_info_frame.add(self.informations_pixels_info_scrolled_window)
    self.informations_pixels_info_frame.show()
    
    self.informations_miscellaneous_textview_frame=gtk.Frame()
    
    self.informations_miscellaneous_textview_frame.set_border_width(5)
    self.informations_miscellaneous_textview_frame_label_button=gtk.Button()
    self.informations_miscellaneous_textview_frame_label_button_label=gtk.Label("  Miscellaneous informations")
    self.informations_miscellaneous_textview_frame_label_button_label.show()
    self.informations_miscellaneous_textview_frame_label_button_image=gtk.image_new_from_stock(gtk.STOCK_SORT_ASCENDING,2)
    self.informations_miscellaneous_textview_frame_label_button_image.show()
    self.informations_miscellaneous_textview_frame_label_button_hbox=gtk.HBox()
    self.informations_miscellaneous_textview_frame_label_button_hbox.pack_start(self.informations_miscellaneous_textview_frame_label_button_image,False,False,0)
    self.informations_miscellaneous_textview_frame_label_button_hbox.pack_start(self.informations_miscellaneous_textview_frame_label_button_label,False,False,0)
    self.informations_miscellaneous_textview_frame_label_button_hbox.show()
    self.informations_miscellaneous_textview_frame_label_button.add(self.informations_miscellaneous_textview_frame_label_button_hbox)
    self.informations_miscellaneous_textview_frame_label_button.set_can_focus(False)
    self.informations_miscellaneous_textview_frame_label_button.set_relief(gtk.RELIEF_NONE)
    self.informations_miscellaneous_textview_frame_label_button.show()
    self.informations_miscellaneous_textview_frame.set_label_widget(self.informations_miscellaneous_textview_frame_label_button)
    
    self.informations_miscellaneous_textview_adjustment=gtk.Adjustment(value=0,lower=0.0,upper=1.0,step_incr=1,page_incr=0,page_size=0) 
    self.informations_miscellaneous_textview_scrolled_window=gtk.ScrolledWindow(hadjustment=self.informations_miscellaneous_textview_adjustment)
    self.informations_miscellaneous_textview_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    self.informations_miscellaneous_textview_scrolled_window.set_size_request(512-128,96) 
    self.informations_miscellaneous_textview_scrolled_window.set_border_width(5)
   
    self.informations_miscellaneous_textview=gtk.TextView()
    self.informations_miscellaneous_textview.set_wrap_mode(gtk.WRAP_WORD) 
    
    self.informations_miscellaneous_textview_text_buffer=self.informations_miscellaneous_textview.get_buffer()
    
    self.informations_miscellaneous_textview_text_buffer_iter=self.informations_miscellaneous_textview_text_buffer.get_start_iter()
    
    stop_linefeed=len(self.image_instance.info.keys())
    i=0
    for v in self.image_instance.info.keys() :
      self.informations_miscellaneous_textview_text_buffer.insert(self.informations_miscellaneous_textview_text_buffer_iter," "+unicode(str(v),encoding="utf-8",errors="ignore")+" : "+unicode(str(self.image_instance.info.get(v)),encoding="utf-8",errors="ignore"))
      if not i+1 == stop_linefeed :
	self.informations_miscellaneous_textview_text_buffer.insert(self.informations_miscellaneous_textview_text_buffer_iter,"\n")
      i += 1
      
    self.informations_miscellaneous_textview.show()
    self.informations_miscellaneous_textview_scrolled_window.add_with_viewport(self.informations_miscellaneous_textview) 
    self.informations_miscellaneous_textview_scrolled_window.show()
    
    self.informations_miscellaneous_textview_frame.add(self.informations_miscellaneous_textview_scrolled_window)
    self.informations_miscellaneous_textview_frame.show()
    
    
    self.informations_area_vbox.pack_start(self.informations_main_info_frame)
    self.informations_area_vbox.pack_start(self.informations_pixels_info_frame)
    self.informations_area_vbox.pack_start(self.informations_miscellaneous_textview_frame)
    
    self.informations_dialog_action_hbox=self.informations_dialog.get_action_area()
    
    self.informations_dialog_action_area_cancel_button=gtk.Button()
    self.informations_dialog_action_area_cancel_button_label=gtk.Label("  Close")
    self.informations_dialog_action_area_cancel_button_label.show()
    self.informations_dialog_action_area_cancel_button_space=gtk.Label("  ")
    self.informations_dialog_action_area_cancel_button_space.show()
    self.informations_dialog_action_area_cancel_button.set_border_width(5)
    self.informations_dialog_action_area_cancel_button_image=gtk.image_new_from_stock(gtk.STOCK_CLOSE,4)
    self.informations_dialog_action_area_cancel_button_image.show()
    self.informations_dialog_action_area_cancel_button_hbox=gtk.HBox()
    self.informations_dialog_action_area_cancel_button_hbox.pack_start(self.informations_dialog_action_area_cancel_button_space,False,False,0)
    self.informations_dialog_action_area_cancel_button_hbox.pack_start(self.informations_dialog_action_area_cancel_button_image,False,False,0)
    self.informations_dialog_action_area_cancel_button_hbox.pack_start(self.informations_dialog_action_area_cancel_button_label,False,False,0)
    self.informations_dialog_action_area_cancel_button_hbox.show()
    self.informations_dialog_action_area_cancel_button.add(self.informations_dialog_action_area_cancel_button_hbox)
    self.informations_dialog_action_area_cancel_button.connect("button-press-event",self.close)
    self.informations_dialog_action_area_cancel_button.show()
    
    self.informations_dialog_action_hbox.pack_start(self.informations_dialog_action_area_cancel_button,False,True,5)
    self.informations_dialog_action_hbox.show()
    
    self.informations_dialog.set_has_separator(True)
    
    self.informations_dialog.show()
    
    gtk.main()
    
    
  def close(self,widget,event) :
    closed(self.informations_dialog,False)
  
  
    
    
def closed(widget,event) :
  widget.destroy() # Destroy the widget.
  
  gtk.main_quit()  # Leave his mainloop.
  