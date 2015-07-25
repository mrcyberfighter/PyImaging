#!/bin/bash -e

sudo echo "Start installation of PyImaging on your system..."

if [[ $? != 0 ]] ; then

  echo "You must launch this installation script as root."
  return 1 ;

fi  

way_prg="$PWD/PyImaging/Source/PyImaging.py"

if [[ ! -d /usr/share/PyImaging ]]
then
  sudo mkdir /usr/share/PyImaging
  sudo cp -R "$PWD/PyImaging" "/usr/share/"
fi



sudo cp "${way_prg}" "/usr/local/bin/"

if [[ -f /usr/local/bin/PyImaging.py ]]
then

  sudo chmod a+x "/usr/local/bin/PyImaging.py"

fi


way_prg="python2 /usr/local/bin/PyImaging.py"
way_icon="/usr/share/PyImaging/Icon/PyImaging_Icon.png"

if [[ -d /usr/share/applications && ! -f /usr/share/applications/PyImaging.desktop ]]
then
  sudo touch /usr/share/applications/PyImaging.desktop
  sudo chmod a+rwx /usr/share/applications/PyImaging.desktop
  sudo echo '[Desktop Entry]' > /usr/share/applications/PyImaging.desktop
  sudo echo 'Type=Application' >> /usr/share/applications/PyImaging.desktop
  sudo echo 'Encoding=UTF-8' >> /usr/share/applications/PyImaging.desktop
  sudo echo 'Name=PyImaging' >> /usr/share/applications/PyImaging.desktop
  sudo echo 'GenericName=PyImaging' >> /usr/share/applications/PyImaging.desktop
  sudo echo "Comment=PyImaging: An image effects processing programme with image files merging functionnalities." >> /usr/share/applications/PyImaging.desktop
  sudo echo "Icon=${way_icon}" >> /usr/share/applications/PyImaging.desktop
  sudo echo "Exec=${way_prg} %F" >> /usr/share/applications/PyImaging.desktop
  sudo echo 'Terminal=false' >> /usr/share/applications/PyImaging.desktop
  sudo echo 'StartupNotify=true' >> /usr/share/applications/PyImaging.desktop
  sudo echo 'Categories=Graphics;2DGraphics;RasterGraphics;GTK;' >> /usr/share/applications/PyImaging.desktop
 
else
 
  sudo echo "Cannot create dekstop shortcut:"
  sudo echo "No folder: /usr/share/applications"
 
  sudo echo
 
fi



if [[ -f /usr/share/PyImaging/Settings/execution_speed.pkl ]]
then

  sudo chmod 0777 "/usr/share/PyImaging/Settings/execution_speed.pkl"

fi

sudo ln -fs "/usr/local/bin/PyImaging.py" "/usr/bin/PyImaging"

sudo ln -fs "/usr/local/bin/PyImaging.py" "/usr/bin/pyimaging"

sudo echo "PyImaging succesfull installed on your system !!!"