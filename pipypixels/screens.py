import queue
import threading
import time

from PIL import Image

from pipypixels.controls.shared import Command
from pipypixels.graphics import assets
from pipypixels.graphics.shared import Matrix


class Screen:
    __observer = None
    def show(self):
        pass
    def hide(self):
        pass
    def receive_command(self, command:Command):
        pass
    def is_paused(self):
        pass
    def wait_for_paused(self):
        self.wait_for_paused_state(True)
    def wait_for_playing(self):
        self.wait_for_paused_state(False)
    def wait_for_paused_state(self, is_paused:bool):
        while self.is_paused() != is_paused:
            time.sleep(1/1000)
    def hide_and_wait(self):
        self.hide()
        self.wait_for_paused()
    def show_and_wait(self):
        self.show()
        self.wait_for_playing()
    def set_command_observer(self, observer):
        self.__observer = observer
    def _send_command_to_observer(self, command:Command):
        if self.__observer is not None:
            self.__observer.receive_command(command)


class ImageScreen(Screen):
    def __init__(self, refresh_interval_seconds: int, current_image: Image, matrix: Matrix):
        self.__thread = None
        self._matrix = matrix
        self.__command_queue = queue.Queue()
        self.__refresh_interval_seconds = refresh_interval_seconds
        self.__last_refresh = 0.0
        self.__paused = False
        self.__current_image = current_image
        self.__render_thread = None

    def show(self):
        if self.__thread is None:
            self.__thread = threading.Thread(target=self.__refresh_loop)
            self.__thread.start()
        else:
            self.__render_current_image()
        self.receive_command(Command.PLAY)

    def __render_current_image(self):
        if self.__current_image is not None:
            self._matrix.render_image(self.__current_image)

    def hide(self):
        self.receive_command(Command.PAUSE)

    def receive_command(self, command:Command):
        self.__command_queue.put(command)

    def _render_image(self)->Image:
        pass

    def is_paused(self):
        return self.__paused

    def step_back(self):
        pass

    def step_forward(self):
        pass

    def __refresh_loop(self):
        while True:
            if not self.__command_queue.empty():
                command = self.__command_queue.get()
                if command == Command.EXIT:
                    return
                if command == Command.PAUSE_PLAY:
                    self.__paused = not self.__paused
                if command == Command.PLAY:
                    self.__paused = False
                if command == Command.PAUSE:
                    self.__paused = True
                if command == Command.STEP_BACKWARD:
                    self.step_back()
                    self.__last_refresh = -1
                if command == Command.STEP_FORWARD:
                    self.step_forward()
                    self.__last_refresh = -1
            time_now = time.time()
            if time_now > self.__last_refresh + self.__refresh_interval_seconds and not self.__paused:
                self.__last_refresh = time_now
                if self.__render_thread is None or not self.__render_thread.is_alive():
                    print(f'Starting render thread...')
                    self.__render_thread = threading.Thread(target=self.__do_threaded_render)
                    self.__render_thread.start()
            time.sleep(1/10)
            if not self.__paused:
                self.__render_current_image()

    def __do_threaded_render(self):
        image = self._render_image()
        if image is not None:
            smallest_dimension = self._matrix.config.overall_led_width
            if self._matrix.config.overall_led_height < smallest_dimension:
                smallest_dimension = self._matrix.config.overall_led_height
            if smallest_dimension < image.width:
                image.thumbnail((smallest_dimension, smallest_dimension))
        self.__current_image = image

    def redraw(self):
        self.__render_current_image()

class StartupImageScreen(ImageScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(1, assets.logo, matrix)
        self.__time_to_move_on = time.time() + 2

    def _render_image(self) ->Image:
        if time.time() > self.__time_to_move_on:
            print('Time to move on...')
            self._send_command_to_observer(Command.NEXT_AND_REMOVE)
        return assets.logo

class ArtworkConfiguration:
    path = "./assets/art"

    @staticmethod
    def create_from_json(screen_json_config):
        config = ArtworkConfiguration()
        config.path = screen_json_config["path"]
        return config

class ArtworkScreen(ImageScreen):
    def __init__(self, config: ArtworkConfiguration, matrix: Matrix):
        super().__init__(10000, None, matrix)
        self.__current_artwork_index = 0
        assets.load_artwork(config.path)

    def __overflow_artwork_index(self):
        if self.__current_artwork_index >= len(assets.artwork):
            self.__current_artwork_index = 0
        elif self.__current_artwork_index < 0:
            self.__current_artwork_index = len(assets.artwork) - 1

    def _render_image(self) ->Image:
        return assets.artwork[self.__current_artwork_index]

    def step_back(self):
        self.__current_artwork_index = self.__current_artwork_index - 1
        self.__overflow_artwork_index()

    def step_forward(self):
        self.__current_artwork_index = self.__current_artwork_index + 1
        self.__overflow_artwork_index()

class ScreenController:
    def __init__(self, matrix: Matrix):
        self.__screens = []
        self.__thread = None
        self.__current_screen = None
        self.__current_screen_index = -1
        self.__powered = True
        self.__matrix = matrix
        self.__command_queue = queue.Queue()

    def begin(self):
        self.__set_screen_by_index(0)
        self.__thread = threading.Thread(target=self.__controller_loop)
        self.__thread.start()

    def add_screen(self, screen:Screen):
        self.__screens.append(screen)
        screen.set_command_observer(self)

    def insert_screen(self, index:int, screen:Screen):
        self.__screens.insert(index, screen)
        screen.set_command_observer(self)

    def __controller_loop(self):
        while True:
            if not self.__command_queue.empty():
                command = self.__command_queue.get()
                if command == Command.EXIT:
                    for screen in self.__screens:
                        screen.receive_command(command)
                    return
                if command == Command.PREVIOUS:
                    if type(self.__current_screen) == StartupImageScreen:
                        self.receive_command(Command.PREV_AND_REMOVE)
                    else:
                        self.__previous_screen()
                elif command == Command.NEXT:
                    if type(self.__current_screen) == StartupImageScreen:
                        self.receive_command(Command.NEXT_AND_REMOVE)
                    else:
                        self.__next_screen()
                elif command == Command.BRIGHTNESS_UP:
                    if self.__matrix.increase_brightness():
                        self.__current_screen.redraw()
                elif command == Command.BRIGHTNESS_DOWN:
                    if self.__matrix.decrease_brightness():
                        self.__current_screen.redraw()
                elif command == Command.POWER:
                    self.__toggle_power()
                elif command == Command.NEXT_AND_REMOVE:
                    self.__current_screen.hide_and_wait()
                    self.__current_screen.receive_command(Command.EXIT)
                    self.__screens.remove(self.__current_screen)
                    if self.__current_screen_index >= len(self.__screens):
                        self.__current_screen_index = 0
                    self.__set_screen_by_index(self.__current_screen_index)
                elif command == Command.PREV_AND_REMOVE:
                    self.__current_screen.hide_and_wait()
                    self.__current_screen.receive_command(Command.EXIT)
                    self.__screens.remove(self.__current_screen)
                    if self.__current_screen_index == 0:
                        self.__current_screen_index = len(self.__screens) - 1
                    self.__set_screen_by_index(self.__current_screen_index)

                else:
                    self.__current_screen.receive_command(command)
            time.sleep(1/100)

    def receive_command(self, command:Command):
        self.__command_queue.put(command)

    def __toggle_power(self):
        if self.__powered:
            self.__current_screen.hide_and_wait()
            self.__matrix.clear()
            self.__powered = False
            self.__remove_startup_screen_if_present()
        else:
            self.__current_screen = StartupImageScreen(self.__matrix)
            self.insert_screen(self.__current_screen_index, self.__current_screen)
            self.__powered = True
            self.__current_screen.show()

    def __remove_startup_screen_if_present(self):
        for i in range(len(self.__screens)):
            screen = self.__screens[i]
            if type(screen) == StartupImageScreen:
                self.__screens.remove(screen)
                return

    def __next_screen(self):
        n = self.__current_screen_index + 1
        if n == len(self.__screens):
            n = 0
        self.__set_screen_by_index(n)

    def __previous_screen(self):
        n = self.__current_screen_index - 1
        if n == -1:
            n = len(self.__screens) - 1
        self.__set_screen_by_index(n)

    def __set_screen_by_index(self, index:int):
        self.__current_screen_index = index
        if self.__current_screen is not None:
            self.__current_screen.hide_and_wait()

        self.__current_screen = self.__screens[index]
        self.__current_screen.show_and_wait()
