import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from components.Figures.averageBarchart import averageScoreFig
from components.Figures.stackBarchart import stackBarchartFig
from helpers import apply_filter
from components.header import get_header

app = dash.Dash(__name__)
app.head = [html.Link(rel='stylesheet', href='./static/style.css')]

# Import data
df_original = pd.read_csv("./user_product_data.csv")

unique_products = sorted(df_original['product'].unique())
unique_users = sorted(df_original['user'].unique())
unique_years = sorted(df_original['year'].unique())

SELECTED_PRODUCTS = 'SELECTED_PRODUCTS'
SELECTED_USERS = 'SELECTED_USERS'
SELECTED_YEARS = 'SELECTED_YEARS'
OUTPUT_CONTAINER = 'OUTPUT_CONTAINER'
BARS = 'BARS'
BARS_GROUPED = 'BARS_GROUPED'

# ---------------------------------------
app.layout = html.Div(className='wrapper', children=[
    get_header([SELECTED_PRODUCTS, SELECTED_USERS], [unique_products, unique_users]),
    html.Div(className='main', children=[
        html.Div(className="barcharts", children=[
        dcc.Dropdown(id=SELECTED_YEARS,
                     options=[
                         {'label': str(year), 'value': year} for year in unique_years
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
    ]),
    html.Div(className='main_right')])


])


# Connect the Plotly graphs with DashComponents
@app.callback(
    [Output(component_id=BARS, component_property='figure'),
     Output(component_id=BARS_GROUPED, component_property='figure')],
    [Input(component_id=SELECTED_PRODUCTS, component_property='value'),
     Input(component_id=SELECTED_USERS, component_property='value'),
     Input(component_id=SELECTED_YEARS, component_property='value')]
)
def update_graph(products_selected, users_selected, years_selected):
    dff = df_original.copy()

    dff = apply_filter(dff, products_selected, 'product')
    dff = apply_filter(dff, users_selected, 'user')
    dff = apply_filter(dff, years_selected, 'year')

    fig1 = averageScoreFig(dff)
    fig2 = stackBarchartFig(dff)

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
