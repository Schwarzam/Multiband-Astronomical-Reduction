#!/bin/bash

read -p """
---------- MAR pipeline setup ----------

1 - Run marServer
(remember to adjust ROOTFITS variable at marServer/marServer/settings.py)

2 - Install mar python package
3 - Install all dependencies to mar package

4 - Setup marServer
5 - Build Database
6 - Create super user
Default - postgresql (if change needed adjust in marServer/marServer/settings.py)

Option: """ var

if [[ $var -eq 1 ]]
then
  (cd marServer; python3 manage.py runserver 0:8000$1)
fi

if [[ $var -eq 2 ]]
then
  (sudo python3 -m pip install numpy)
  (pip3 install -r requirements.txt)
  (sudo python3 -m pip install Cython)
  (cd mar/mar/reduction/LacosmicsBuild; sudo python3 setup.py build)
  (cd mar/mar/reduction/LacosmicsBuild; sudo python3 setup.py install --user)

  (python3 -m pip install Cython)
  (cd mar/mar/reduction/LacosmicsBuild/build; sudo rm -rf *)
  (cd mar/mar/reduction/LacosmicsBuild/build; sudo chmod 777 *)

  (cd mar/mar/reduction/LacosmicsBuild; python3 setup.py build)
  (cd mar/mar/reduction/LacosmicsBuild; python3 setup.py install)
  (cd mar/mar/reduction/LacosmicsBuild; python3 setup.py install --user)
  

  (cd mar; python3 setup.py bdist_wheel)
  (cd mar; pip3 install dist/mar-0.1-py3-none-any.whl --force-reinstall)
fi

if [[ $var -eq 3 ]]
then
	sudo apt update
	sudo apt install autoconf automake libtool
  sudo apt install make

	#Pyraf dependencies
  read -p "Install pyraf3? (y/n) " pyrafz
  if [[ "$pyrafz" == "y" ]]
  then
    sudo apt install libx11-dev
    sudo apt install libcfitsio-bin
    sudo apt install python3-pyraf
  fi

  #Install Sextractor
  read -p "Install Sextractor? (y/n) " sextr
  if [[ "$sextr" == "y" ]]
  then
    sudo apt-get install libatlas-base-dev liblapack-dev libblas-dev
    sudo apt-get install -y fftw3-dev
    (cd; git clone https://github.com/Schwarzam/sextractor.git)
    (cd; cd sextractor; sh autogen.sh)
    (cd; cd sextractor; ./configure)
    (cd; cd sextractor; make)
    (cd; cd sextractor; sudo make install)
  fi

  #Install Scamp
  read -p "Install Scamp? (y/n) " scampz
  if [[ "$scampz" == "y" ]]
  then
    sudo apt-get install libcurl4-openssl-dev
    sudo apt install libplplot-dev
    (cd; git clone https://github.com/Schwarzam/scamp.git)
    (cd; cd scamp; sh autogen.sh)
    (cd; cd scamp; ./configure)
    (cd; cd scamp; make)
    (cd; cd scamp; sudo make install)
  fi

  #Install CFITSIO
  read -p "Install CFITSIO? (y/n) " cfitsios
  if [[ "$cfitsios" == "y" ]]
  then
    (cd; wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.49.tar.gz)
    (cd; tar -xf cfitsio-3.49.tar.gz)
    (cd; cd cfitsio-3.49; ./configure --prefix=/usr/local)
    (cd; cd cfitsio-3.49; make)
    (cd; cd cfitsio-3.49; sudo make install)

    sudo ln -s /usr/local/lib/libcfitsio.so.9 /usr/lib/libcfitsio.so.9
  fi

  #Install Swarp
  read -p "Install Swarp? (y/n) " swarpz
  if [[ "$swarpz" == "y" ]]
  then
    (cd; git clone https://github.com/Schwarzam/swarp.git)
    (cd; cd swarp; sh autogen.sh)
    (cd; cd swarp; ./configure)
    (cd; cd swarp; make)
    (cd; cd swarp; sudo make install)
  fi

  ## install fitstopng
  read -p "Install FitsToPNG? (y/n) " fitstopng
  if [[ "$fitstopng" == "y" ]]
  then
    sudo apt install fitspng
  fi

  ## install fitstopng
  read -p "Install postgreSQL? (y/n) " postgres
  if [[ "$postgres" == "y" ]]
  then
    sudo apt update
    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

    echo ''
    echo 'run on postgres command-line: '
    echo ''
    echo 'CREATE DATABASE mar;'
    echo "CREATE USER t80steam WITH PASSWORD 'password';"
    echo "GRANT ALL PRIVILEGES ON DATABASE mar TO t80steam;"
    echo "exit"
    sudo -u postgres psql; 
    
  fi
  

fi

if [[ $var -eq 4 ]]
then
  (cd marServer; pip3 install -r requirements.txt)
fi

if [[ $var -eq 5 ]]
then
  (cd marServer; python3 manage.py makemigrations)
  (cd marServer; python3 manage.py migrate)
fi

if [[ $var -eq 6 ]]
then
  (cd marServer; python3 manage.py createsuperuser)
fi