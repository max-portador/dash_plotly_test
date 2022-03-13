from dash import dcc
from dash import html

from components.common.componetWrapper import componentWrapper
from constants import SELECTED_PRODUCTS, SELECTED_USERS


def header(unique_products, unique_users):
    children = []
    products_selector = dcc.Dropdown(id=SELECTED_PRODUCTS,
                                     className='select_box',
                                     options=[
                                         {'label': str(uv), 'value': uv} for uv in unique_products
                                     ],
                                     multi=True,
                                     placeholder="All",
                                     value=[])

    users_selector = dcc.Dropdown(id=SELECTED_USERS,
                                  className='select_box',
                                  options=[
                                      {'label': str(uv), 'value': uv} for uv in unique_users
                                  ],
                                  multi=True,
                                  placeholder="All",
                                  value=[])

    children.append(componentWrapper(products_selector, "Products", ['dropdown']))
    children.append(componentWrapper(users_selector, "User", ['component_wrapper_users', 'dropdown']))

    children.append(html.Div(style={'display': 'grid'}))
    return html.Div(className='header', children=children)
