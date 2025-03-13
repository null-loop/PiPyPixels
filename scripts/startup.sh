#!/bin/bash

pushd $(dirname "$0")/..
bin/python3 pi.py
popd