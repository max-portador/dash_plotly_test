import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Import and clean data
df_original = pd.read_csv("./user_product_data.csv")

df = df_original.groupby(['year', "month"])[['score']].mean().round({"score": 1})
df.reset_index(inplace=True)
unique_years = df['year'].unique()
# print(df[:15])



months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
SELECTED_YEARS = 'SELECTED_YEARS'
OUTPUT_CONTAINER = 'OUTPUT_CONTAINER'
BARS = 'BARS'
# ---------------------------------------
app.layout = html.Div([
    html.H1('My first Dash Plotly App', style={'text-align': 'center'}),
    dcc.Dropdown(id=SELECTED_YEARS,
                 options=[
                     {'label': str(year), 'value': year} for year in unique_years
                 ],
                 multi=False,
                 value=unique_years[-1],
                 style={'width': '40%'},
                 ),
    html.Div(id=OUTPUT_CONTAINER, children=[]),
    html.Br(),
    dcc.Graph(id=BARS, figure={})
])

# Connect the Plotly graphs with DashComponents

@app.callback(
    [Output(component_id=OUTPUT_CONTAINER, component_property='children'),
     Output(component_id=BARS, component_property='figure')],
    [Input(component_id=SELECTED_YEARS, component_property='value')]
)
def update_graph(option_slctd):

    container = f"The year chosen by user was: {option_slctd}"

    dff = df_original.copy()
    dff = dff[dff["year"] == option_slctd]
    dff = dff.groupby(['month'])[['month', 'score']].mean().round({"score": 1})
    score = dff['score'].tolist()
    minimal = min(score)
    colors = [ '#90A1B6' if s == minimal else "#ABDDC3" for s in score]

    # Plotly Express
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months,
                         y=score,
                         text=score,
                         textposition='outside',
                         marker_color=colors,
                         ))
    fig.update_traces(showlegend=False,  hoverinfo='skip')

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)