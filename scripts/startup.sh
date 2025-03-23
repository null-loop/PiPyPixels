#!/bin/bash

pushd $(dirname "$0")/..
git pull
bin/python3 pi.py
popd