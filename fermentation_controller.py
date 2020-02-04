import time
import datetime
from threading import Thread

from influxdb import InfluxDBClient
from temp_reader import TempReader
from controller_state import ControllerState
from temp_comparer import TempComparer
from state_controller import StateController

class FermentationController:
    def __init__(self, time_units=1):
        self.time_units = time_units
        self.temp_reader = TempReader()
        self.comparer = TempComparer()
        self.state = ControllerState.CORRECT
        self.controller_thread = Thread(target=self.main_loop)
        self.state_controller = StateController()
        self.database_client = InfluxDBClient(host="localhost", port=8086, database="ferm_data")

    def write_to_database(self, current_temp, current_state):
        new_point = [{
            "measurement": "ferm-temp",
            "tags": {
                "recipe-id": 1,
            },
            "time": datetime.datetime.now().isoformat(),
            "fields": {
                "temp-reading": current_temp,
                "hold-temp": self.comparer.get_hold_temp(),
                "state": current_state.name
            }
        }]
        return self.database_client.write_points(new_point)

    def set_step(self, step):
        self.comparer.set_hold_temp(step["hold_temp"])
        self.comparer.set_temp_range(step["temp_range"])
        return self.get_step()

    def update_step(self, update):
        return self.get_step()
    

    def get_step(self):
        return {"hold_temp": self.comparer.get_hold_temp(), "temp_range": self.comparer.get_temp_range()}

    def run(self):
        print("Running")
        try:
            self.controller_thread.start()
            return True
        except RuntimeError:
            return False

    def main_loop(self):
        print("main loop")
        while True:
            current_temp = self.temp_reader.get_current_temp()
            new_state = self.comparer.compare_temps(current_temp, self.state)
            self.state = new_state
            self.state_controller.set_state(self.state)
            self.write_to_database(current_temp, self.state)
            print(current_temp, self.state)
            time.sleep(self.time_units)


if __name__ == "__main__":
    app = FermentationController()
    app.run()