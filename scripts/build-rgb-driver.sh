#!/bin/bash

pushd ..
# TODO:Get the python version to use when copying later on...
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git rpi-rgb-led-matrix
pushd rpi-rgb-led-matrix/bindings/python
sudo apt-get install make && sudo apt-get install g++ && sudo apt-get install cython3
make build-python
cp -r rgbmatrix ../../../PiPyPixels/lib/python3.11/site-packages/rgbmatrix
popd
popd
