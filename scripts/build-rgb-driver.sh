#!/bin/bash

pushd ..
# TODO:Get the python version to use when copying later on...
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git rpi-rgb-led-matrix
pushd rpi-rgb-led-matrix/bindings/python
make build-python
cp bindings/python/rgbmatrix ../../../PiPyPixels/lib/python3.11/site-packages/rgbmatrix
popd
popd
