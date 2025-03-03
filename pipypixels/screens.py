import queue
import threading
import time

from PIL import Image

from pipypixels.controls import Command
from pipypixels.graphics.shared import Matrix


class Screen:
    def show(self):
        pass
    def hide(self):
        pass
    def receive_command(self, command:Command):
        pass

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

    def __render_current_image(self):
        if self.__current_image is not None:
            self.__matrix.render_image(self.__current_image)

    def hide(self):
        self.receive_command(Command.PAUSE)

    def receive_command(self, command:Command):
        self.__command_queue.put(command)

    def _render_image(self)->Image:
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
            time_now = time.time()
            if time_now > self.__last_refresh + self.__refresh_interval_seconds and not self.__paused:
                self.__last_refresh = time_now
                self.__current_image = self._render_image()
                self.__render_current_image()
            time.sleep(1/10)

class StartupImageScreen(ImageScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(10000000, matrix)
        self.__led_icon = Image.open("./assets/led.png")

    def _render_image(self) ->Image:
        return self.__led_icon

class ScreenController:
    def __init__(self):
        self.__screens = []
        self.__thread = None
        self.__currentScreen = None

    def add_screen(self, screen:Screen):
        self.__screens.append(screen)

    def receive_command(self, command:Command):
        self.__currentScreen.receive_command(command)

    def begin(self):
        self.__currentScreen = self.__screens[0]
        self.__currentScreen.show()