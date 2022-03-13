import plotly.graph_objs as go


def bulletChartFig(df):
    average_score = round(df['score'].mean(), 2)
    maximal = round(df['score'].max(), 2)
    fig = go.Figure()

    fig.add_trace(go.Bar(y=[1], x=[average_score], marker_color='#ABDDC3', width=[0.7],
                         text=[f'    {average_score}'], textposition='outside',
                         textfont={"family": "Times New Roman", "size": 20},
                         showlegend=False, orientation='h'))

    fig.update_layout(autosize=True,
                      font_family="Times New Roman",
                      dragmode=False,
                      plot_bgcolor='#ececec',
                      xaxis=dict(range=[0, maximal], showgrid=False, zeroline=False, visible=False),
                      yaxis=dict(showgrid=False, zeroline=False, visible=False),
                      margin=dict(l=0, r=0, t=0, b=0))

    return fig
