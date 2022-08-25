# Welcome to the Solar Power Generation Repository

By: Loh Zhi Shen

Last updated: 25 August 2022

<strong>Summary:</strong>
* Anaylsed solar power generated in Python to identify underperforming solar panels.
* Developed tools in Python to automatically identify underperforming solar panels based on real time data coming from sensors.
* Designed a dashboard using Dash and Python to present real time data and log underperforming solar panels for user to take follow up action on.

For detailed walkthrough, please view the files in the following order:

1. analysis.ipynb

    This notebook contains the exploratory data analysis done on the dataset.

2. model.py
    
    This Python module contains 2 classes. First, the class used as the data model in the dashboard. The other class is the outlier detection model.

3. controller.py

    This Python module contains a single class. It controlls the interaction between the view and the models.

4. view.py

    This Python module contains a single class which produces the dashboard.

5. main.py

    This Python module is the entry point to the dashboard.

6. assets

    This folder contains the CSS for the dashboard and a JSON config file.

---

## <strong>About the Dataset</strong>

This data has been gathered at two solar power plants in India over a 34 day period. It has two pairs of files - each pair has one power generation dataset and one sensor readings dataset. The power generation datasets are gathered at the inverter level - each inverter has multiple lines of solar panels attached to it. The sensor data is gathered at a plant level - single array of sensors optimally placed at the plant.

Link to dataset: https://www.kaggle.com/datasets/anikannal/solar-power-generation-data?datasetId=836676&sortBy=dateRun&tab=profile

## <strong>Problem Definition</strong>

The producer of the dataset gave 3 different questions to answer.

1. Can we predict the power generation for next couple of days? - this allows for better grid management
2. Can we identify the need for panel cleaning/maintenance?
3. Can we identify faulty or suboptimally performing equipment?

The question answered within this repository is the third question. 

---

## <strong>Models Used</strong>

* HuberRegressor
    * A robust linear regressor. It is less influenced by the presence of outliers in the data which makes it possible to use it to identify outliers.

## <strong>Statistical Tools Used</strong>

* Hypothesis Testing
    * The errors of a linear model are normally distributed with population mean 0 and unknown population standard deviation. Thus, by using sample standard deviation to estimate the unknown population standard deviation, it is possible to conduct a test to identify under-performing solar panels.

---

## <strong>End Product</strong>

* A model to identify faulty or suboptimally performing solar panels.
    * This model is a hybrid of machine learning and statistics. It uses a HuberRegressor to estimate the power generated given a irradiation level and uses hypothesis testsing to test if the deviation from the estimate is significant enough to warrant labelling it as an outlier.
    * The confidence interval can be fine-tuned to the meet the need of the solar power plant.

* A dashboard to monitor the power production at the inverter level with alerts about faulty or suboptimally performing solar panels.

<img src = "assets/dashboard image.png" alt = "Image of dash bord" />

The features of this dashboard are as follows:

1. The dashboard is constantly updated in real time.
2. Hovering over the different bars in the bar chart produces a tooltip with the information about that datapoint.
3. The alerts are updated everytime the model identifies an outlier.
4. The most recent alerts are bolded and red in color.
5. Every alert is logged in a text file for archive.

---

## <strong>Learning Points</strong>

* Robust linear regressors - HuberRegressor.
* Hypothesis testsing - Z test.
* Outlier detection.
* Combine different statistical and machine learning tools to cover for each other's weaknesses.
* A new data visualization library - Plotly.
* Dashboarding using Dash.
* Basic HTML and CSS.