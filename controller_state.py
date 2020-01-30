from enum import Enum


class ControllerState(Enum):
    COOLER = 1
    HEATER = 2
    CORRECT = 3
    ERROR = 4