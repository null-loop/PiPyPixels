from os import listdir
from os.path import isfile, join

from PIL import Image, ImageFont

__fonts = {}

def font_custom(size:int)->ImageFont:
    if not size in __fonts:
        __fonts[size] = ImageFont.truetype("./assets/NotoSans-Regular.ttf", size)
    return __fonts[size]

logo_128_by_128 = Image.open('./assets/logo-128-by-128.png')
logo_64_by_64 = Image.open('./assets/logo-64-by-64.png')
logo_32_by_32 = Image.open('./assets/logo-32-by-32.png')

__art_path = './assets/art'

artwork = []

for f in listdir('./assets/art'):
    fp = join(__art_path, f)
    if isfile(fp):
        artwork.append(Image.open(fp))
