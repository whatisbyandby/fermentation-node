from controller_state import ControllerState


class TempComparer:
    def __init__(self, hold_temp=75, temp_range=1):
        self.hold_temp = hold_temp
        self.temp_range = temp_range

    def compare_temps(self, current_temp, current_state):
        if self.hold_temp >= current_temp + self.temp_range:
            return ControllerState.HEATER
        elif self.hold_temp <= current_temp - self.temp_range:
            return ControllerState.COOLER
        elif self.hold_temp > current_temp and current_state == ControllerState.HEATER:
            return ControllerState.HEATER
        elif self.hold_temp < current_temp and current_state == ControllerState.COOLER:
            return ControllerState.COOLER
        else:
            return ControllerState.CORRECT

    def get_hold_temp(self):
        return self.hold_temp
    
    def set_hold_temp(self, hold_temp):
        self.hold_temp = hold_temp
    
    def get_temp_range(self):
        return self.temp_range

    def set_temp_range(self, temp_range):
        self.temp_range = temp_range




