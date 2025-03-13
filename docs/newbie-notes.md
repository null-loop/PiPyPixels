## Getting Started

Instructions from a fresh, minimal diet-pi install.

```
sudo apt-get install git python3-dev python3.11-venv libjpeg-dev zlib1g-dev 
git clone https://github.com/null-loop/PiPyPixels.git PiPyPixels
python3 -m venv PiPyPixels
cd PiPyPixels
./scripts/build-rgb-driver.sh
bin/pip install -r pi-requirements.txt
bin/python3 pi.py
```

## Running at startup

Run: `crontab -e` to add a new entry of:

`@reboot /root/PiPyPixels/scripts/startup.sh`
