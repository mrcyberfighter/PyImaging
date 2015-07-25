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

from os.path import basename

def error_file_mergin_message(filepath1,filepath2) :
  error_file_mergin_message_dialog=gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=None)
  
  error_file_mergin_message_dialog.set_markup("<big>File merging operation failure, cannot merge files:</big>\n<big>file:</big> %s\n<big>and</big>\n<big>file:</big> %s" %(basename(filepath1),basename(filepath2)) )
  error_file_mergin_message_dialog.show()
  error_file_mergin_message_dialog.run()
  error_file_mergin_message_dialog.destroy()
  