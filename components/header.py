from dash import dcc
from dash import html

from constants import SELECTED_PRODUCTS, SELECTED_USERS


def get_header(unique_values):
    ids = [SELECTED_PRODUCTS, SELECTED_USERS]
    children = []
    for _id, uvs in zip(ids, unique_values):
        children.append(dcc.Dropdown(id=_id,
                                     className='select_box',
                                     options=[
                                         {'label': str(uv), 'value': uv} for uv in uvs
                                     ],
                                     multi=True,
                                     placeholder="All",
                                     value=[]))
    children.append(html.Div(style={'display': 'grid'}))
    return html.Div(className='header', children=children)
