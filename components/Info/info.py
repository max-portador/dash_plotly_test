from dash import html
from dash import dcc

from constants import BULLET_CHART


def info():
    bigTitle = html.Span(className='info_bigTitle', children=['Food Review Scores'])

    span = html.Span(className='info_right_title', children=['Year Avarege Score'])
    bullet = dcc.Graph(id=BULLET_CHART,  figure={},
                  config={"displayModeBar": False})
    yearAverageScore = html.Div(className='info_right', children=[span, bullet])

    children = [bigTitle, yearAverageScore]
    return html.Div(className='info', children=children)