import queue
import threading
import time

from PIL import Image

from pipypixels.controls.shared import Command
from pipypixels.graphics.shared import Matrix


class Screen:
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

class ImageScreen(Screen):
    def __init__(self, refresh_interval_seconds, matrix: Matrix):
        self.__thread = None
        self.__matrix = matrix
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
            self.__matrix.render_image(self.__current_image)

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
        super().__init__(10000000, matrix)
        self.__led_icon = Image.open("./assets/led.png")

    def _render_image(self) ->Image:
        return self.__led_icon

class ScreenController:
    def __init__(self, matrix: Matrix):
        self.__screens = []
        self.__thread = None
        self.__current_screen = None
        self.__current_screen_index = -1
        self.__powered = True
        self.__matrix = matrix

    def add_screen(self, screen:Screen):
        self.__screens.append(screen)

    def receive_command(self, command:Command):
        print(f'ScreenController::receive_command({command})')
        if command == Command.PREVIOUS: self.__previous_screen()
        elif command == Command.NEXT: self.__next_screen()
        elif command == Command.EXIT:
            for screen in self.__screens:
                screen.receive_command(command)
        elif command == Command.POWER: self.__toggle_power()
        elif command == Command.BRIGHTNESS_UP:
            if self.__matrix.increase_brightness():
                self.__current_screen.redraw()
        elif command == Command.BRIGHTNESS_DOWN:
            if self.__matrix.decrease_brightness():
                self.__current_screen.redraw()
        else: self.__current_screen.receive_command(command)

    def __toggle_power(self):
        if self.__powered:
            self.__current_screen.hide()
            while not self.__current_screen.is_paused():
                time.sleep(1/1000)
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

    def begin(self):
        self.__set_screen_by_index(0)