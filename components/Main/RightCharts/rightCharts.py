from dash import html
from dash import dcc

from components.common.componetWrapper import componentWrapper
from constants import HORIZONTAL_BARS, WORDCLOUD


def rightCharts():
    horizontal_bars = dcc.Graph(id=HORIZONTAL_BARS,
                  figure={},
                  config={"displayModeBar": False})

    children = [
        componentWrapper(horizontal_bars, 'Number of Reviews', ['reviews']),
        componentWrapper(html.Img(id=WORDCLOUD), 'Summary', ['reviews'])
    ]
    return html.Div(className='main_right', children=children)