from dash import dcc
from dash import html


def get_header(ids, unique_values):
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

