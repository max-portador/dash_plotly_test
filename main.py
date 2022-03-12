import pandas as pd
import math
import calendar
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from helpers import apply_filter
from layout.header import get_header

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
                  style={'width': '50%'}),

        dcc.Graph(id=BARS_GROUPED,
                  figure={},
                  config={"displayModeBar": False},
                  style={'width': '50%'})
    ])

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

    df_count = pd.crosstab(dff['month'], dff['score'], values=dff['score'], aggfunc='count')
    unique_scores = df_count.columns.tolist()

    df_avg = dff.groupby(['month'])[['score']].mean().round({"score": 1})

    # маппим номера месяцев с их названиями
    month_name = df_avg.index.map(lambda x: calendar.month_abbr[x])
    score = df_avg['score'].tolist()

    minimal = min(score)
    maximal = math.ceil(max(score))
    colors_fig1 = ['#90A1B6' if s == minimal else '#ABDDC3' for s in score]
    colors_fig2 = ['#F6A198', '#D6D8D8', '#CCD9E5', '#90A1B6', '#ABDDC3']

    fig1 = go.Figure()
    fig2 = go.Figure()

    # добавляем горизотальные линии
    for y in range(1, maximal + 1):
        fig1.add_hline(y=y, line_width=1, line_dash='dot', line_color='gray')

    fig1.add_trace(go.Bar(x=month_name, y=score, text=score,
                          textposition='outside', marker_color=colors_fig1,
                          textfont={"family": "Times New Roman", "size": 18, },
                          showlegend=False, hoverinfo='skip'))

    fig1.update_layout(autosize=True,
                       dragmode=False,
                       plot_bgcolor='white',
                       bargap=0.5,
                       xaxis=dict(showgrid=False),
                       yaxis=dict(nticks=maximal + 1, showgrid=False),
                       margin=dict(l=5, r=5, t=5, b=5))

    max2 = max(df_count.sum(axis=1).tolist())

    for col, color in zip(unique_scores, colors_fig2):
        fig2.add_trace(go.Bar(x=month_name, y=df_count[col], marker_color=color,
                              textfont={"family": "Times New Roman", "size": 18},
                              showlegend=False, hoverinfo='y'))
    fig2.update_layout(autosize=True,
                       barmode='stack',
                       dragmode=False,
                       plot_bgcolor='white',
                       bargap=0.5,
                       xaxis=dict(showgrid=False),
                       yaxis=dict(range=[0, max2 + 1], showgrid=False),
                       margin=dict(l=5, r=5, t=5, b=5))

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
