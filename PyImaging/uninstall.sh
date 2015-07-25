#!/bin/bash -e

sudo echo "Start uninstall of PyImaging from your system..."

if [[ $? != 0 ]] ; then

  echo "You must launch this uninstall script as root."
  return 1 ;

fi  

if [[ -d /usr/share/PyImaging ]] ; then

  sudo rm -R /usr/share/PyImaging
 
fi

if [[ -f /usr/local/bin/PyImaging.py ]] ; then

  sudo unlink /usr/bin/PyImaging
  sudo unlink /usr/bin/pyimaging

  sudo rm /usr/local/bin/PyImaging.py
 
fi

if [[ -d /usr/share/applications && -f /usr/share/applications/PyImaging.desktop ]] ; then    

  sudo rm /usr/share/applications/PyImaging.desktop
 
fi

sudo echo "PyImaging successfull remove from your system !!!"  