import random

import pandas as pd
import plotly.graph_objs as go
import dash
import calendar
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from components.Figures.averageBarchart import averageScoreFig
from components.Figures.horizontalBarChart import horizontalBarChart
from components.Figures.stackBarchart import stackBarchartFig
from components.Figures.wordCloudChart import wordCloudChart
from components.Main.mainContainer import mainContainer
from constants import SELECTED_YEARS, SELECTED_USERS, SELECTED_PRODUCTS, BARS_GROUPED, BARS, HORIZONTAL_BARS, WORDLIST, \
    WORDCLOUD
from helpers import apply_filter
from components.header import get_header

app = dash.Dash(__name__)
app.head = [html.Link(rel='stylesheet', href='./static/style.css')]

# Import data
df_original = pd.read_csv("./user_product_data.csv")

unique_products = sorted(df_original['product'].unique())
unique_users = sorted(df_original['user'].unique())
unique_years = sorted(df_original['year'].unique())


epithets = df_original.score.apply(lambda x: random.choice(WORDLIST))
df_original['epithets'] = epithets
# ---------------------------------------
app.layout = html.Div(className='wrapper', children=[
    get_header([unique_products, unique_users]),
    mainContainer(unique_years),
])


# Connect the Plotly graphs with DashComponents
@app.callback(
    [Output(component_id=BARS, component_property='figure'),
     Output(component_id=BARS_GROUPED, component_property='figure'),
     Output(component_id=HORIZONTAL_BARS, component_property='figure'),
     Output(component_id=WORDCLOUD, component_property='src')],
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
    fig3 = horizontalBarChart(dff)
    bytes = wordCloudChart(dff)

    return fig1, fig2, fig3, bytes


if __name__ == '__main__':
    app.run_server(debug=True)
