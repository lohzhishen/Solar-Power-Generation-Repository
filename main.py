__author__ = "Loh Zhi Shen"
__version__ = "1.0.0"
__last_updated__ = "25 August 2022"

import datetime
import json

from view import View
from controller import Controller
from model import DataModel

# should be current time
# however, for simulation purposes, a fixed time is used.
START = datetime.datetime(2020, 6, 1, 12, 00)

def main(debug = False):
    """Main function for app."""

    config = json.load(open('assets\config.json', 'r'))

    generation_df = DataModel(config['Plant_1_Generation_Data'])
    weather_df = DataModel(config['Plant_1_Weather_Senor_Data'])

    controller = Controller(generation_df, weather_df)

    view = View(START, controller)

    view.run(debug = debug)

if __name__ == "__main__":
    main(debug = True)