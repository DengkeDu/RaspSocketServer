#!/bin/bash

sudo echo "deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi \n
deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi" > /etc/apt/sources.list

sudo apt-get update

sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav \
	gstreamer1.0-rtsp \
	gstreamer1.0-vaapi \
	libgstreamer1.0-0 \
	libgstreamer1.0-dev \
	libgstreamer-plugins-bad1.0-dev

cd
mkdir workdir0
cd workdir0
git clone https://github.com/GStreamer/gst-rtsp-server.git
cd gst-rtsp-server
git checkout origin/1.4
./autogen.sh
make
sudo make install
