import os
import urllib

import mahotas
from PIL import Image

from pipypixels.graphics.shared import Matrix
from pipypixels.screens import ImageScreen
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyConfiguration:
    denied_artists = []
    client_id = ""
    client_secret = ""

    @staticmethod
    def create_from_json(screen_json_config):
        config = SpotifyConfiguration()
        config.denied_artists = screen_json_config["denied_artists"]
        config.client_id = screen_json_config["client_id"]
        config.client_secret = screen_json_config["client_secret"]
        return config

class SpotifyScreen(ImageScreen):
    def __init__(self, config: SpotifyConfiguration, matrix: Matrix):
        super().__init__(5, matrix)
        self.__config = config
        self.__local_image_cache_dir = '.local-image-cache'

        if not os.path.isdir(self.__local_image_cache_dir):
            os.mkdir(self.__local_image_cache_dir)

        auth_manager = SpotifyOAuth(client_id=self.__config.client_id, client_secret=self.__config.client_secret,
                                    scope='user-read-playback-state',
                                    redirect_uri='http://localhost:8080/spotify/callback')
        self.__spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.__last_image_url = ""

    def _render_image(self) ->Image:
        try:
            current = self.__spotify.current_user_playing_track()
            if current is not None:
                current_album = current['item']['album']
                artists = current['item']['artists']
                # if any artist name is in the deny_artists list we don't update
                denied = False
                for artist in artists:
                    if artist['name'].lower() in self.__config.denied_artists:
                        denied = True

                if denied:
                    current_image_url = self.__last_image_url
                else:
                    current_image_url = current_album['images'][0]['url']

                self.__last_image_url = current_image_url

            if self.__last_image_url:
                image_id = urllib.parse.urlparse(self.__last_image_url).path.split('/')[-1]
                cached_image_path = self.__local_image_cache_dir +'/' + image_id + '.png'

                if not os.path.isfile(cached_image_path):
                    urllib.request.urlretrieve(self.__last_image_url, 'temp-download.jpg')
                    jpg = mahotas.imread('temp-download.jpg')
                    mahotas.imsave(cached_image_path, jpg)
                    image = Image.open(cached_image_path)
                    image.thumbnail((self._matrix.config.overall_led_width, self._matrix.config.overall_led_height))
                    image.save(cached_image_path)
                else:
                    image = Image.open(cached_image_path)

                return image
        except:
            print("Error updating image")