from dash import html
from dash import dcc

from components.common.componetWrapper import componentWrapper
from constants import SELECTED_YEARS, BARS, BARS_GROUPED


def barCharts(unique_values):
    stackBarchart = dcc.Graph(id=BARS_GROUPED, figure={},
                              config={"displayModeBar": False})

    barchart = dcc.Graph(id=BARS, figure={},
                         config={"displayModeBar": False})

    yearsSelector = dcc.Dropdown(id=SELECTED_YEARS,
                                 options=[
                                     {'label': str(year), 'value': year} for year in unique_values
                                 ],
                                 multi=True,
                                 value=[],
                                 placeholder="All",
                                 )
    barChartsWithSelector = html.Div(className='barChartsWithSelector',
                                     children=[
                                         yearsSelector,
                                         barchart
                                     ])

    children = [
        componentWrapper(barChartsWithSelector, 'Average Scores'),
        componentWrapper(stackBarchart, 'Scores')
    ]
    return html.Div(className='barcharts', children=children)
