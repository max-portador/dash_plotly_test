from dash import html
from dash import dcc

from constants import SELECTED_YEARS, BARS, BARS_GROUPED


def barCharts(unique_values):
    children = [
        dcc.Dropdown(id=SELECTED_YEARS,
                     options=[
                         {'label': str(year), 'value': year} for year in unique_values
                     ],
                     multi=True,
                     value=[],
                     placeholder="All",
                     style={'width': '40%'},
                     ),

        dcc.Graph(id=BARS,
                  figure={},
                  config={"displayModeBar": False}),

        dcc.Graph(id=BARS_GROUPED,
                  figure={},
                  config={"displayModeBar": False})
    ]
    return html.Div(className='barcharts', children=children)