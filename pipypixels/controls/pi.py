import keyboard

from pipypixels.controls.shared import Command
from pipypixels.screens import ScreenController

class RemoteKeyboardCommandSource:
    def __init__(self, screen_controller: ScreenController):
        self.__screen_controller = screen_controller
        keyboard.on_press(lambda key_event: self.__key_pressed(key_event.scan_code, key_event.name))

    def __key_pressed(self, scan_code, name):
        command = Command.NONE
        if scan_code == 116: command = Command.POWER
        elif scan_code == 168: command = Command.STEP_BACKWARD
        elif scan_code == 208: command = Command.STEP_FORWARD
        elif scan_code == 165: command = Command.PREVIOUS
        elif scan_code == 163: command = Command.NEXT
        elif scan_code == 164: command = Command.PAUSE_PLAY
        elif scan_code == 2: command = Command.PRESET_1
        elif scan_code == 3: command = Command.PRESET_2
        elif scan_code == 4: command = Command.PRESET_3
        elif scan_code == 5: command = Command.PRESET_4
        elif scan_code == 6: command = Command.PRESET_5
        elif scan_code == 7: command = Command.PRESET_6
        elif scan_code == 8: command = Command.PRESET_7
        elif scan_code == 9: command = Command.PRESET_8
        elif scan_code == 10: command = Command.PRESET_9
        elif scan_code == 11: command = Command.PRESET_10
        elif scan_code == 113: command = Command.RESET
        elif scan_code == 115: command = Command.BRIGHTNESS_UP
        elif scan_code == 114: command = Command.BRIGHTNESS_DOWN
        elif scan_code == 104: command = Command.FRAMERATE_UP
        elif scan_code == 109: command = Command.FRAMERATE_DOWN
        elif scan_code == 418: command = Command.ZOOM_IN
        elif scan_code == 419: command = Command.ZOOM_OUT

        if command != Command.NONE:
            self.__screen_controller.receive_command(command)