import plotly.graph_objs as go


def horizontalBarChart(df):
    df_horizon = df.groupby(['score'])[['score']].count();
    unique_scores = df_horizon.index.tolist()

    color_scheme = ['#F6A198', '#D6D8D8', '#CCD9E5', '#90A1B6', '#ABDDC3']

    # находим максимальную сумму оценок
    maximal = int(df_horizon.max())

    fig = go.Figure()

    fig.add_trace(go.Bar(y=unique_scores, x=df_horizon['score'], marker_color=color_scheme,
                         text=df_horizon['score'], textposition='outside',
                         textfont={"family": "Times New Roman", "size": 20},
                         showlegend=False,  orientation='h'))

    fig.update_layout(autosize=True,
                      font_family="Times New Roman",
                      dragmode=False,
                      plot_bgcolor='white',
                      bargap=0.5,
                      xaxis=dict(range=[0, maximal + 20], showgrid=False),
                      yaxis=dict(showgrid=False),
                      margin=dict(l=20, r=5, t=15, b=5))

    return fig
