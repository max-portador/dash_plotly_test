import pandas as pd
import dash
from dash import html
from dash.dependencies import Input, Output
import random

from Figures.averageBarchart import averageScoreFig
from Figures.bulletChart import bulletChartFig
from Figures.horizontalBarChart import horizontalBarChart
from Figures.stackBarchart import stackBarchartFig
from Figures.wordCloudChart import wordCloudChart
from components.Info.info import info
from components.Main.mainContainer import mainContainer
from constants import SELECTED_YEARS, SELECTED_USERS, SELECTED_PRODUCTS, BARS_GROUPED, BARS, HORIZONTAL_BARS, WORDLIST, \
    WORDCLOUD, BULLET_CHART
from helpers import apply_filter
from components.Header.header import header

app = dash.Dash(__name__)
# set css-file for our app
app.head = [html.Link(rel='stylesheet', href='./static/style.css')]
app.head = [html.Link(rel='stylesheet', href='./static/dropdown_redifine.css')]
app.head = [html.Link(rel='stylesheet', href='./static/component_wrapper_style.css')]

# Import data
df_original = pd.read_csv("./user_product_data.csv")

unique_products = sorted(df_original['product'].unique())
unique_users = sorted(df_original['user'].unique())
unique_years = sorted(df_original['year'].unique())

# Create epithets for each line in dataframe
epithets = df_original.score.apply(lambda x: random.choice(WORDLIST))
df_original['epithets'] = epithets

# ---------------------------------------

# set our html-markup
app.layout = html.Div(className='wrapper', children=[
    header(unique_products, unique_users),
    info(),
    mainContainer(unique_years),
])


# Connect the Plotly graphs with DashComponents
@app.callback(
    [Output(component_id=BARS, component_property='figure'),
     Output(component_id=BARS_GROUPED, component_property='figure'),
     Output(component_id=HORIZONTAL_BARS, component_property='figure'),
     Output(component_id=BULLET_CHART, component_property='figure'),
     Output(component_id=WORDCLOUD, component_property='src')],
    [Input(component_id=SELECTED_PRODUCTS, component_property='value'),
     Input(component_id=SELECTED_USERS, component_property='value'),
     Input(component_id=SELECTED_YEARS, component_property='value')]
)
def update_graph(products_selected, users_selected, years_selected):
    df = df_original.copy()

    # filter our dataframe
    df = apply_filter(df, products_selected, 'product')
    df = apply_filter(df, users_selected, 'user')
    df = apply_filter(df, years_selected, 'year')

    # get content for our dash-components
    fig1 = averageScoreFig(df)
    fig2 = stackBarchartFig(df)
    fig3 = horizontalBarChart(df)
    fig4 = bulletChartFig(df)
    img_like_bytes = wordCloudChart(df)

    return fig1, fig2, fig3, fig4, img_like_bytes


if __name__ == '__main__':
    app.run_server(debug=True)
