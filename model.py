from __future__ import annotations

__author__ = "Loh Zhi Shen"
__version__ = "1.0.0"
__last_updated__ = "25 August 2022"

import numpy as np
import pandas as pd
import datetime

from sklearn.linear_model import HuberRegressor
from scipy import stats as st

class DataModel:
    """Model in the MVC Design Pattern.
    
    This serves as the data structure used in storing the data coming
    from the sensors in the solar power plant.

    Args:
        path (str): The path to the csv storing the data.
    """
    def __init__(self: DataModel, path: str) -> None:

        self.path = path
        self.df = pd.read_csv(
            path, 
            parse_dates = ['DATE_TIME'], 
            dayfirst = True
        )
        self.df.set_index('DATE_TIME', inplace = True)

    def get_slice(self: DataModel, start: datetime.datetime, end: datetime.datetime 
            | None = None) -> pd.DataFrame:
        """Returns a slice of the dataframe with timestamps between the 
        start and end specified.

        Args:
            start (datetime) : The date to make the first slice.
            end (datetime | None) : The date to make the second slice. 
                If none, it will default to start.

        Returns:
            DataFrame : A dataframe containing all the rows with timestamp 
                in between start and end (inclusive). 
        """

        if end is None:
            return self.df.loc[start]
        return self.df.loc[start:end]

class PredictionModel:
    """Model in the MVC Design Pattern.
    
    This class serves as the prediction model for the identification of 
    outliers. It consists of a HuberRegressor and uses hypothesis testing
    on distance to the regression line to identify outliers.

    Args:
        confidence_level (float): The confidence level to use for the 
            hypothesis testing.
    """

    def __init__(self: PredictionModel, confidence_level: float = 0.99) -> None:
        
        self.model = HuberRegressor()
        self.significance_level = 1 - confidence_level

    def fit(self: PredictionModel, X: pd.DataFrame, Y: pd.Series) -> None:
        """Fits the model to the data.
        
        This method should be called before predict is called.

        Args:
            X (DataFrame): Dataframe containing the IRRADIATION column.
            Y (Series): Series containing the POWER column.
        """
        assert len(X) == len(Y)

        self.model.fit(X, Y)
        residues = Y - self.model.predict(X)

        self.variance = np.sum(residues**2) / (len(Y) - 1)
        self.threshold = st.t.ppf(self.significance_level, len(Y) - 1)
    
    def predict(self, X, Y):
        """Classifies whether a data point is an outlier or inlier.

        Args:
            X (DataFrame): Dataframe containing the IRRADIATION column.
            Y (Series): Series containing the POWER column.
        
        Returns:
            array: An array equal in length to the data inputted. Each
                entry in the array is whether True or False. True implies
                that that data point is a outlier while False implies
                that it is an inlier.
        """
        assert len(X) == len(Y)
        assert self.threshold is not None
        
        residues = Y - self.model.predict(X)
        test_statistic = residues / self.variance**0.5
        outlier = test_statistic < self.threshold
        return outlier