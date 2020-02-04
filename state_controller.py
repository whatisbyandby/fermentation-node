import time
from controller_state import ControllerState
import RPi.GPIO as GPIO

class StateController:
    def __init__(self):
        self.heater_pin = 10
        self.cooler_pin = 12
        self.initialize_pins()

    def set_state(self, state):
        if state == ControllerState.HEATER:
            self.heater_on()
        elif state == ControllerState.COOLER:
            self.cooler_on()
        elif state == ControllerState.CORRECT:
            self.correct_mode()
        elif state == ControllerState.ERROR:
            self.error_mode()

    def heater_on(self):
        GPIO.output(self.heater_pin, GPIO.HIGH)
        GPIO.output(self.cooler_pin, GPIO.LOW)

    def cooler_on(self):
        GPIO.output(self.heater_pin, GPIO.LOW)
        GPIO.output(self.cooler_pin, GPIO.HIGH)

    def correct_mode(self):
        GPIO.output(self.heater_pin, GPIO.LOW)
        GPIO.output(self.cooler_pin, GPIO.LOW)

    def error_mode(self):
        for i in range(10):
            GPIO.output(self.cooler_pin, GPIO.LOW)
            GPIO.output(self.heater_pin, GPIO.LOW)
            time.sleep(.25)
            GPIO.output(self.heater_pin, GPIO.HIGH)
            time.sleep(.25)
            GPIO.output(self.heater_pin, GPIO.LOW)
            

    def initialize_pins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.cooler_pin, self.heater_pin], GPIO.OUT, initial=GPIO.LOW)

if __name__ == "__main__":
    controller = StateController()
    controller.set_state(ControllerState.HEATER)
    time.sleep(1)
    controller.set_state(ControllerState.COOLER)
    time.sleep(1)
    controller.set_state(ControllerState.ERROR)
    GPIO.cleanup()