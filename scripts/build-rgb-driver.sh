pushd .. >> dev/null
# TODO:Get the python version to use when copying later on...
git checkout https://github.com/hzeller/rpi-rgb-led-matrix.git rpi-rgb-led-matrix
pushd rpi-rgb-led-matrix/bindings/python >> dev/null
make build-python
cp bindings/python/rgbmatrix ../../../PiPyPixels/lib/python3.11/site-packages/rgbmatrix
popd >> dev/null
popd >> dev/null
