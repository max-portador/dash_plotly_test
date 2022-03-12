from dash import html
from dash import dcc

from constants import HORIZONTAL_BARS, WORDCLOUD


def rightCharts():
    children = [
        dcc.Graph(id=HORIZONTAL_BARS,
                  figure={},
                  config={"displayModeBar": False}),
    html.Img(id=WORDCLOUD),
    ]
    return html.Div(className='main_right', children=children)