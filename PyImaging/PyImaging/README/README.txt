+==============================================================================+
|                                  PyImaging                                   |
+==============================================================================+
+------------------------------------------------------------------------------+
| PyImaging: An image effects processing programme, with severals              |
|            functionnalities to modify the loaded images and images files     |
|            merging functionnalities.                                         |
|                                                                              |
| Writing by: Eddie Brüggemann                                                 |
| Writing programming language: python 2.7.6                                   |
| Contact: mrcyberfighter@gmail.com                                            |
| Credits: Thank's to my beloved mother, my family and to the doctors.         |
|          Stay away from drugs, drugs destroy your brain and your life.       |
|                                                                              |
+------------------------------------------------------------------------------+
+==============================================================================+
|                                  Description                                 |
+==============================================================================+
+------------------------------------------------------------------------------+
|                                                                              |
|  PyImaging support severals images files formats to load into the programm   |
|  for effects applying:                                                       |
|                                                                              |
|    * bmp (Bitmap image file.).                                               |
|    * jpg | jpeg (Joint Photographic Experts Group.).                         |
|    * pcx (Pulse Code Modulation.).                                           |
|    * pdf (Windows Bitmap.).                                                  |
|    * png (Portable Network Graphics.).                                       |
|    * ppm (Portable pixmap file format.).                                     |
|    * tif | tiff (Tag(ged) Image File Format.).                               |
|                                                                              |
|  And support following formats as output:                                    |
|                                                                              |
|    * bmp (Bitmap image file.).                                               |
|    * gif (Graphics Interchange Format.).                                     |
|    * jpeg (Joint Photographic Experts Group.).                               |
|    * pcx (Pulse Code Modulation.).                                           |
|    * pdf (Windows Bitmap.).                                                  |
|    * png (Portable Network Graphics.).                                       |
|    * ppm (Portable pixmap file format.).                                     |
|    * tiff (Tag(ged) Image File Format.).                                     |
|                                                                              |
|    Note that the program can write *.gif files but not load it.              |
|                                                                              |
|    And that only the *.jpeg extension is supported (not the *.jpg)           |
|    for the Joint Photographic Experts Group file format as output.           |
|                                                                              |
|    This is the same for the *.tiff extension (*.tif is not supported)        |
|    for the Tag(ged) Image File Format as output.                             |
|                                                                              |
|  For images files merging you can use as input file formats:                 |
|                                                                              |
|    * bmp (Bitmap image file.).                                               |
|    * gif (Graphics Interchange Format.).                                     |
|    * jpg | jpeg (Joint Photographic Experts Group.).                         |
|    * pcx (Pulse Code Modulation.).                                           |
|    * pdf (Windows Bitmap.).                                                  |
|    * png (Portable Network Graphics.).                                       |
|    * ppm (Portable pixmap file format.).                                     |
|    * tif | tiff (Tag(ged) Image File Format.).                               |
|                                                                              |
|  It is different for the Composite file mergin algorithm mask file which     |
|  must have transparency support.                                             |
|                                                                              |
|  So the image file format:                                                   |
|  * gif (Graphics Interchange Format.).                                       |
|  is exclude from the list.                                                   |
|                                                                              |
|  And the image file format:                                                  |
|  * xbm (X Bitmap.).                                                          |
|  is added to the list.                                                       |
|                                                                              |
|  For images files merging you can use as output file formats:                |
|                                                                              |
|    * bmp (Bitmap image file.).                                               |
|    * gif (Graphics Interchange Format.).                                     |
|    * jpeg (Joint Photographic Experts Group.).                               |
|    * pcx (Pulse Code Modulation.).                                           |
|    * pdf (Windows Bitmap.).                                                  |
|    * png (Portable Network Graphics.).                                       |
|    * ppm (Portable pixmap file format.).                                     |
|    * tiff (Tag(ged) Image File Format.).                                     |
|                                                                              |
|  Note that only the \*.jpeg extension is supported (not the \*.jpg)          |
|  for the Joint Photographic Experts Group file format.                       |
|                                                                              |
|  This is the same for the \*.tiff extension (\*.tif is not supported)        |
|  for the Tag(ged) Image File Format.                                         |
|                                                                              |
|  For effects processing of an loaded file you can:                           |
|                                                                              |
|  * Rotate the image from 90°.                                                |
|                                                                              |
|  * Flipping the image (mirroring.                                            |
|                                                                              |
|  * Apply an grayscale.                                                       |
|                                                                              |
|  * Apply an predefine filter.                                                |
|                                                                              |
|  * Use the colors inverter matrix.                                           |
|                                                                              |
|  * Use the colors intensity tools.                                           |
|                                                                              |
|  * Use the colors scale matrix.                                              |
|                                                                              |
|  * Use the red, green and blue scale editor.                                 |
|                                                                              |
|  * Additionnaly you can get some informations and statistics about the       |
|    current image (The current loaded image with the processing effects).     |
|                                                                              |
|  You can set the processing speed (To set in relationship to your computer   |
|  performance. which influence the effect processing by setting the number of |
|  pixels to compute per millisecond.                                          |
|  Everytime you change this value, this will be register as persistent        |
|  settings so that you don't have to change it everytime you launch the       |
|  programme.                                                                  |
|                                                                              |
|  Enjoy to process effects on your favorites images and generate mixing       |
|  images from your favorites images.                                          |
|                                                                              |
|  For an accurate usage description look at the documentation *.pdf file:     |
|                                                                              |
|  PyImaging_Documentation.pdf                                                 |
|                                                                              |
|  Locate at /usr/share/PyImaging/Documentation/PyImaging_Documentation.pdf    |
|                                                                              |
+------------------------------------------------------------------------------+
+==============================================================================+
|                                  Launching                                   |
+==============================================================================+
+------------------------------------------------------------------------------+
|                                                                              |
| You can run the programme by simply clicking on his icon.                    |
|                                                                              |
| Else:                                                                        |
|                                                                              |
| you can run the programme with trough the commandline:                       |
| $ PyImaging image_filepath                                                   |
| or                                                                           |
| $ pyimaging image_filepath                                                   |
|                                                                              |
| or by open an image file supported with PyImaging trough you file navigator  |
| and his 'Open with' option.                                                  |
|                                                                              |
+------------------------------------------------------------------------------+
+==============================================================================+
|                                Installation                                  |
+==============================================================================+
+------------------------------------------------------------------------------+
|                                                                              |
| You can install the programm with the commandline:                           |
| $ su root                                                                    |
| $ password:                                                                  |
| $                                                                            |
| # ./install.sh                                                               |
|                                                                              |
| You can uninstall the the program with the commandline:                      |
| $ su root                                                                    |
| $ password:                                                                  |
| $                                                                            |
| # ./uninstall.sh                                                             |
|                                                                              |
+------------------------------------------------------------------------------+
+==============================================================================+
|                                  Copyright                                   |
+==============================================================================+
+------------------------------------------------------------------------------+
|                                                                              |
| PyImaging an image treatment programme with severals effects.                |
| And image files mergin capabilities.                                         |
| Copyright (C) 2014 Eddie Bruggemann                                          |
|                                                                              |
| This file is part of PyImaging.                                              |
| PyImaging is free software: you can redistribute it and/or modify            |
| it under the terms of the GNU General Public License as published by         |
| the Free Software Foundation, either version 3 of the License, or            |
| (at your option) any later version.                                          |
|                                                                              |
| PyImaging is distributed in the hope that it will be useful,                 |
| but WITHOUT ANY WARRANTY; without even the implied warranty of               |
| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 |
| GNU General Public License for more details.                                 |
|                                                                              |
| You should have received a copy of the GNU General Public License            |
| along with PyImaging. If not, see <http://www.gnu.org/licenses/>             |
|                                                                              |
+------------------------------------------------------------------------------+
+==============================================================================+
