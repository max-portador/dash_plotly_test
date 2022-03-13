import plotly.graph_objs as go
import calendar
import math


def averageScoreFig(df):
    df_avg = df.groupby(['month'])[['score']].mean().round({"score": 1})
    month_name = df_avg.index.map(lambda x: calendar.month_abbr[x])
    score = df_avg['score']

    minimal = score.min()
    maximal = math.ceil(score.max())

    # гененрируем цветовую схему
    color_scheme = ['#90A1B6' if s == minimal else '#ABDDC3' for s in score]
    fig = go.Figure()

    # добавляем горизотальные линии
    for y in range(1, maximal + 1):
        fig.add_hline(y=y, line_width=1, line_dash='dot', line_color='gray')

    fig.add_trace(go.Bar(x=month_name, y=score, text=score,
                          textposition='outside', marker_color=color_scheme,
                          textfont={"family": "Times New Roman", "size": 18, },
                          showlegend=False, hoverinfo='skip'))

    fig.update_layout(autosize=True,
                       dragmode=False,
                       font_family="Times New Roman",
                       plot_bgcolor='white',
                       bargap=0.5,
                       xaxis=dict(showgrid=False),
                       yaxis=dict(nticks=maximal + 1, showgrid=False),
                       margin=dict(l=5, r=5, t=5, b=5))

    return fig