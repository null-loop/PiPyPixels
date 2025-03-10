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
    def __init__(self, refresh_interval_seconds, matrix: Matrix):
        self.__thread = None
        self._matrix = matrix
        self.__command_queue = queue.Queue()
        self.__refresh_interval_seconds = refresh_interval_seconds
        self.__last_refresh = 0.0
        self.__paused = False
        self.__current_image = None

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
            time_now = time.time()
            if time_now > self.__last_refresh + self.__refresh_interval_seconds and not self.__paused:
                self.__last_refresh = time_now
                self.__current_image = self._render_image()
                self.__render_current_image()
            time.sleep(1/10)

    def redraw(self):
        self.__render_current_image()

class StartupImageScreen(ImageScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(1, matrix)
        self.__time_to_move_on = time.time() + 4

    def _render_image(self) ->Image:
        if time.time() > self.__time_to_move_on:
            self._send_command_to_observer(Command.NEXT_AND_REMOVE)
        image = None
        if self._matrix.config.overall_led_height == 128:
            image = assets.logo_128_by_128
        elif self._matrix.config.overall_led_height == 64:
            image = assets.logo_64_by_64
        elif self._matrix.config.overall_led_height == 32:
            image = assets.logo_32_by_32
        return image

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

    def __controller_loop(self):
        while True:
            if not self.__command_queue.empty():
                command = self.__command_queue.get()
                print(f'ScreenController::{command}')
                if command == Command.EXIT:
                    for screen in self.__screens:
                        screen.receive_command(command)
                    return
                if command == Command.PAUSE_PLAY:
                    self.__paused = not self.__paused
                if command == Command.PLAY:
                    self.__paused = False
                if command == Command.PAUSE:
                    self.__paused = True
                if command == Command.PREVIOUS:
                    self.__previous_screen()
                elif command == Command.NEXT:
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
                    self.__set_screen_by_index(0)
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
        else:
            self.__powered = True
            self.__current_screen.show()

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