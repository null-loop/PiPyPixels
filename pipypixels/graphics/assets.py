from os import listdir
from os.path import isfile, join

from PIL import Image, ImageFont

__fonts = {}

def font_custom(size:int)->ImageFont:
    if not size in __fonts:
        __fonts[size] = ImageFont.truetype("./assets/NotoSans-Regular.ttf", size)
    return __fonts[size]

logo = Image.open('./assets/logo-128.png')
github_loading = Image.open('./assets/github-loading-128.png')
spotify_loading = Image.open('./assets/spotify-loading-128.png')

git_branch = Image.open('./assets/git-branch.png')
git_pull_request = Image.open('./assets/git-pull-request.png')

__life_presets_path = './assets/life-presets'

artwork = []
life_presets = {}

def load_life_presets():
    for f in listdir(__life_presets_path):
        fp = join(__life_presets_path, f)
        if isfile(fp):
            life_presets[f] = Image.open(fp)

def load_artwork(path):
    for f in listdir(path):
        fp = join(path, f)
        if isfile(fp):
            artwork.append(Image.open(fp))