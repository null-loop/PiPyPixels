from pipypixels.controls import Command


class Screen:
    def show(self):
        pass
    def hide(self):
        pass

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