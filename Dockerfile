FROM ubuntu:22.10

RUN apt update
RUN apt install -y git wget

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt install -y autoconf automake libtool 
RUN apt install -y make

RUN apt install -y libx11-dev
RUN apt install -y libcfitsio-bin

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \ 
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libbz2-dev \
        wget \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get purge -y imagemagick imagemagick-6-common 

RUN cd /usr/src \
    && wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz \
    && tar -xzf Python-3.11.1.tgz \
    && cd Python-3.11.1 \
    && ./configure --enable-optimizations \
    && make altinstall

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1
RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.11 1

RUN apt install -y python3-pyraf
RUN apt install -y python3-pip

#TO USE GPU unmark below
# RUN apt -y install nvidia-cuda-toolkit
# RUN python3 -m pip install numba

#Sextractor
RUN apt-get -y install libatlas-base-dev liblapack-dev libblas-dev
RUN apt-get -y install -y fftw3-dev
RUN git clone https://github.com/Schwarzam/sextractor.git
RUN cd ./sextractor && sh autogen.sh && ./configure && make && make install

#SCAMP
RUN apt-get install libcurl4-openssl-dev
RUN apt install -y libplplot-dev
RUN git clone https://github.com/Schwarzam/scamp.git
RUN cd scamp && sh autogen.sh && ./configure && make && make install

#CFITSIO
RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.49.tar.gz
RUN tar -xf cfitsio-3.49.tar.gz
RUN cd cfitsio-3.49 && ./configure --prefix=/usr/local && make && make install
RUN ln -s /usr/local/lib/libcfitsio.so.9 /usr/lib/libcfitsio.so.9

#SWARP
RUN git clone https://github.com/Schwarzam/swarp.git
RUN cd swarp && sh autogen.sh && ./configure && make && make install

#PSFEX
RUN git clone https://github.com/Schwarzam/psfex.git
RUN cd psfex && sh autogen.sh && ./configure && make && make install


RUN apt install -y fitspng


WORKDIR /MAR

RUN python3.11 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3.11 -m pip install -r requirements.txt

RUN python3.11 -m pip install numpy
RUN python3.11 -m pip install Cython

RUN python3.11 -m pip install pyraf

COPY . . 

RUN cd mar/mar/reduction/LacosmicsBuild && python3.11 setup.py build
RUN cd mar/mar/reduction/LacosmicsBuild && python3.11 setup.py install --user
RUN cd mar/mar/reduction/LacosmicsBuild/build && rm -rf ./*
#RUN cd mar/mar/reduction/LacosmicsBuild/build && chmod 777 ./* -- removed because docker run as root 

RUN cd mar/mar/reduction/LacosmicsBuild && python3.11 setup.py build
RUN cd mar/mar/reduction/LacosmicsBuild && python3.11 setup.py install
RUN cd mar/mar/reduction/LacosmicsBuild && python3.11 setup.py install --user

RUN python3.11 -m pip install wheel
RUN cd mar && python3.11 setup.py bdist_wheel
RUN cd mar && python3.11 -m pip install dist/mar-0.1-py3-none-any.whl --force-reinstall

# install fitspng
RUN cd packages && tar zxf fitspng-1.4.tar.gz
RUN cd packages/fitspng-1.4 && autoreconf -i && ./configure && make && make install

RUN echo "export USER=mar" >> /etc/bash.bashrc
ENV USER="mar"

RUN export iraf=/usr/lib/iraf
ENV iraf="/usr/lib/iraf"

WORKDIR /MAR/marServer

EXPOSE 8002
