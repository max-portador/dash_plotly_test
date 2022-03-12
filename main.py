import pandas as pd
import plotly.express as px
import math
import os
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from helpers import apply_filter
from layout.header import get_header

app = dash.Dash(__name__)
app.head = [html.Link(rel='stylesheet', href='./static/style.css')]

# Import and clean data
df_original = pd.read_csv("./user_product_data.csv")

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months_dict = {i + 1: month for i, month in enumerate(months)}

unique_products = sorted(df_original['product'].unique())
unique_users = sorted(df_original['user'].unique())
unique_years = sorted(df_original['year'].unique())


SELECTED_PRODUCTS = 'SELECTED_PRODUCTS'
SELECTED_USERS = 'SELECTED_USERS'
SELECTED_YEARS = 'SELECTED_YEARS'
OUTPUT_CONTAINER = 'OUTPUT_CONTAINER'
BARS = 'BARS'

# ---------------------------------------
app.layout = html.Div(className='wrapper', children=[
    get_header([SELECTED_PRODUCTS, SELECTED_USERS], [unique_products, unique_users]),
    html.Div([
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
                  config={"displayModeBar": False},
                  style={'width': '50%'})
    ])

])


# Connect the Plotly graphs with DashComponents

@app.callback(
    Output(component_id=BARS, component_property='figure'),
    [Input(component_id=SELECTED_PRODUCTS, component_property='value'),
     Input(component_id=SELECTED_USERS, component_property='value'),
     Input(component_id=SELECTED_YEARS, component_property='value')]
)
def update_graph(products_selected, users_selected, years_selected):
    dff = df_original.copy()

    dff = apply_filter(dff, products_selected, 'product')
    dff = apply_filter(dff, users_selected, 'user')
    dff = apply_filter(dff, years_selected, 'year')

    # if isinstance(option_slctd, list):
    #     if len(option_slctd):
    #         dff = dff[dff["year"].isin(option_slctd)]
    # else:
    #     dff = dff[dff["year"] == option_slctd]

    dff = dff.groupby(['month'])[['score']].mean().round({"score": 1})
    month_name = dff.index.map(months_dict)
    score = dff['score'].tolist()

    minimal = min(score)
    maximal = math.ceil(max(score))
    print(maximal)

    colors = ['#90A1B6' if s == minimal else "#ABDDC3" for s in score]

    # Plotly Express
    # fig = px.bar(dff, x='month', y='score')

    fig = go.Figure()
    for y in range(1, maximal + 1):
        fig.add_hline(y=y, line_width=1, line_dash="dot", line_color="gray")
    fig.add_trace(go.Bar(x=month_name,
                         y=score,
                         text=score,
                         textposition='outside',
                         marker_color=colors,
                         textfont={
                             "family": "Times New Roman",
                             "size": 18
                         }
                         ))
    fig.update_layout(autosize=True,
                      dragmode=False,
                      plot_bgcolor='white',
                      bargap=0.5,
                      xaxis=dict(showgrid=False),
                      # yaxis=dict(range=[0, maximal], nticks=maximal + 1, gridcolor='gray', line_color='red'),
                      yaxis=dict( nticks=maximal + 1,showgrid=False),
                      margin=dict(l=5, r=5, t=5, b=5))

    fig.update_traces(showlegend=False, hoverinfo='skip')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
