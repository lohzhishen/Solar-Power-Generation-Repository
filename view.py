from __future__ import annotations

__author__ = "Loh Zhi Shen"
__version__ = "1.0.0"
__last_updated__ = "25 August 2022"

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import datetime 

from controller import Controller

class View:
    """View in the MVC Design Pattern.
    
    This class controls the running of the dashboard.
    
    Args:
        START (datetime): The time which the server should start.
        Controller (Controller): The controller class in the MVC 
            model which the view will call upon to pull an update.
        minutes (int): The between data collection in minutes.
    """
    def __init__(self: View, START: datetime.datetime, 
            controller: Controller, minutes: int = 5) -> None:

        # create the dashboard
        self.app = dash.Dash(__name__)

        # customize the layout
        self.app.layout = html.Div(
            children = [
                dcc.Interval(
                    id = 'timer',
                    interval = 1000 * minutes,  # should be 15 minutes
                    n_intervals = 0
                ),
                dcc.Store(
                    id = 'session',
                    storage_type = 'session',
                    data = START
                ),
                html.Div(
                    className = 'header',
                    children = [
                        html.H1(
                            className = 'header-icon',
                            children = '🌤️'
                        ),
                        html.H1(
                            className = 'header-title',
                            children = 'SOLAR POWER GENERATION'
                        ),
                        html.H1(
                            className = 'header-subtitle',
                            children = 'Equipment Performance'
                        )
                    ]
                ), 

                html.Div(
                    className = 'main',
                    children = [
                        html.Div(
                            className = 'left-body',
                            children = [
                                dcc.Graph(
                                    id = 'data-visualization',
                                    className = 'graph',
                                    figure = go.Figure()
                                )
                            ]
                        ),
                        html.Div(
                            className = 'right-body',
                            children = [
                                html.P(
                                    className = 'alert-title',
                                    children = 'Alerts'
                                ),
                                html.P(
                                    id = 'null-alert',
                                    className = 'alert-null',
                                    children = 'There are no alerts.'
                                ),
                                html.P(
                                    id = 'alerts',
                                    className = 'alert-body',
                                    children = []
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        @self.app.callback([
            Output('data-visualization', 'figure'), 
            Output('alerts', 'children'), 
            Output('null-alert', 'children'),
            Output('session', 'data'), 
            Output('timer', 'n_intervals')
            ], [
            Input('timer', 'n_intervals'), 
            Input('session', 'data'), 
            Input('alerts', 'children')
            ]
        )
        def pull_update(n_intervals, server_time, old):
            """This callback updates the dashboard with the most 
            update to date information.
            """
            # convert sever_time from str to datetime
            time_details = {
                'year': int(server_time[0:4]),
                'month': int(server_time[5:7]),
                'day': int(server_time[8:10]),
                'hour': int(server_time[11:13]),
                'minute': int(server_time[14:16])
            }
            server_time = datetime.datetime(**time_details)

            # get the last time which data was recoreded
            if time_details['minute'] >= 45:
                time_details['minute'] = 45
            elif time_details['minute'] >= 30:
                time_details['minute'] = 30
            elif time_details['minute'] >= 15:
                time_details['minute'] = 15
            else:
                time_details['minute'] = 0
            time = datetime.datetime(**time_details)

            # alert controller to update event
            df = controller.identify_outliers(time)

            # order for colors
            order = df['RESULT'].unique()
            if order[0] == 0:
                color = ['rgb(27, 158, 119)', 'rgb(217, 95, 2)']
            else:
                color = ['rgb(217, 95, 2)', 'rgb(27, 158, 119)']
            
            # creating the figure
            figure = px.bar(
                df, x = 'SOURCE_KEY', y = 'POWER', color = 'RESULT', 
                title = 'Live Power Generation', 
                labels = {
                    'RESULT': 'Outlier', 
                    "SOURCE_KEY": "Inverter ID", 
                    'POWER': 'Power'
                }, 
                color_discrete_sequence = color)
            figure.update_layout(margin_autoexpand = True)

            # creating and logging new alerts
            alerts = []
            underperforming = df.loc[df['RESULT'], 'SOURCE_KEY'].to_numpy()
            with open(
                f'Log/{time.year}-{time.month}-{time.day} Log file.txt', 'a+'
                ) as file:
                for key in underperforming:
                    alerts.append(
                        html.P(
                            className = 'alert-new', 
                            children = f"[{time}] {key} triggered performance alert!",
                            style = {'font-weight': 'bold'}
                            )
                        )
                    file.write(f"[{time}] {key} triggered performance alert!" + '\n')
            
            # unbold past alerts
            if time.day == (time - datetime.timedelta(minutes = 15)).day:
                for text in old:
                    alerts.append(
                        html.P(
                            className = 'alert-old',
                            children = text['props']['children']
                        )
                    )

            # default text if no alerts
            if alerts == []:
                null_alert = 'There are no alerts.'
            else:
                null_alert = ''

            # update the server_time
            next_time = server_time + datetime.timedelta(minutes = 15)

            return (figure, alerts, null_alert, next_time, n_intervals + 1)
    
    def run(self, debug = False):
        """Runs the app.
        
        Args:
            debug (bool): A bool to indicate whether to run the app in 
                debug mode.    
        """
        self.app.run(debug = debug)