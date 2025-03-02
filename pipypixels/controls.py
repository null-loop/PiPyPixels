from enum import IntEnum


class Command(IntEnum):
    NONE = -1
    RESET = 0
    POWER = 1
    REWIND = 2
    FAST_FORWARD = 3
    PREVIOUS = 4
    NEXT = 5
    PAUSE_PLAY = 6
    BRIGHTNESS_UP = 7
    BRIGHTNESS_DOWN = 8
    PROGRAM_UP = 9
    PROGRAM_DOWN = 10
    ZOOM_IN = 11
    ZOOM_OUT = 12
    PRESET_1 = 100
    PRESET_2 = 101
    PRESET_3 = 102
    PRESET_4 = 103
    PRESET_5 = 104
    PRESET_6 = 105
    PRESET_7 = 106
    PRESET_8 = 107
    PRESET_9 = 108
    PRESET_10 = 109
    EXIT = 999
