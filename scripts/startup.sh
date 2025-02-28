#!/bin/bash

pushd $(dirname "$0")
../bin/python3 ../pipypixels/pi.py
popd