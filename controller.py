from __future__ import annotations

__author__ = "Loh Zhi Shen"
__version__ = "1.0.0"
__last_updated__ = "25 August 2022"

import pandas as pd
import datetime

from model import PredictionModel, DataModel

class Controller:
    """Controller in the MVC Design Pattern.
    
    This class controls the business logic between View and 
    the Model in the MVC Model.
    
    Args:
        generation_df (DataModel): A Model containing the 
            power generation data.
        weather_df (DataModel): A Model containing the weather
             sensor data.
        prediction_model (PredictionModel): A Model to classify
             outliers in the data.
        confidence_level (float): The confidence level to use 
            for the hypothesis testing in the prediction model.
    """

    def __init__(self: Controller, generation_df: DataModel, 
        weather_df: DataModel, confidence_level: float = 0.99) -> None:

        self.confidence_level = confidence_level
        self.generation_df = generation_df
        self.weather_df = weather_df
        self.model = PredictionModel(self.confidence_level)

        past_generation_df = self.generation_df.get_slice(
            datetime.datetime(2020, 5, 15, 0, 0), 
            datetime.datetime(2020, 5, 30, 23, 59)
        )
        past_weather_df = self.weather_df.get_slice(
            datetime.datetime(2020, 5, 15, 0, 0), 
            datetime.datetime(2020, 5, 30, 23, 59)
        )

        past_data = past_generation_df.merge(
            past_weather_df, 
            how = 'left', 
            left_index = True, 
            right_index = True, 
            suffixes = ('', '_WEATHER')
            ).dropna()
        past_data['POWER'] = past_data['DC_POWER'] + past_data['AC_POWER']

        self.model.fit(past_data[['IRRADIATION']], past_data['POWER'])

    def identify_outliers(self: Controller, 
        current_date: datetime.datetime) -> pd.DataFrame:
        """Returns the lastest data collected and their classification.
        
        Args:
            current_date (datetime): The time which the controller
                should look up for data.

        Returns:
            DataFrame: A DataFrame containing the lastest data collected 
                and whether it is an outlier or inlier. 
        """     
        current_generation_df = self.generation_df.get_slice(current_date)
        current_weather_df = self.weather_df.get_slice(current_date)

        present_data = current_generation_df.copy()
        present_data['IRRADIATION'] = current_weather_df['IRRADIATION']
        present_data['POWER'] = present_data['DC_POWER'] + present_data['AC_POWER']

        present_data['RESULT'] = self.model.predict(present_data[['IRRADIATION']], present_data['POWER'])
        
        return present_data