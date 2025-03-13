pushd .. >> dev/null
git checkout https://github.com/hzeller/rpi-rgb-led-matrix.git rpi-rgb-led-matrix
pushd rpi-rgb-led-matrix/bindings/python >> dev/null
sudo apt-get update && sudo apt-get install python3-dev
make build-python
cp bindings/python/rgbmatrix ../../../PiPyPixels/lib/python3.11/site-packages/rgbmatrix
popd >> dev/null
popd >> dev/null
