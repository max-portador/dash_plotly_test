from dash import html

from components.Main.LeftBarcharts.barCharts import barCharts
from components.Main.RightCharts.rightCharts import rightCharts


def mainContainer(unique_values):
    children=[
        barCharts(unique_values),
        rightCharts()
    ]
    return html.Div(className='main', children=children)