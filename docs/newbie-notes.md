## Getting Started

Instructions from a fresh, minimal diet-pi install.

```
sudo apt-get install git && sudo apt-get install python3-dev && sudo apt-get install python3.11-venv 
git clone https://github.com/null-loop/PiPyPixels.git PiPyPixels
python3 -m venv PiPyPixels
cd PiPyPixels
./scripts/build-rgb-driver.sh
bin/pip install -r pi-requirements.txt
bin/python3 pi.py
```

## Getting the rgbmatrix module

* Build from https://github.com/hzeller/rpi-rgb-led-matrix
* Copy the contents of `/bindings/python/rgbmatrix` into `~/PiPyPixels/lib/python3.11/site-packages/rgbmatrix`
