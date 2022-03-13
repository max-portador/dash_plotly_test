import plotly.graph_objs as go
import pandas as pd
import calendar


def stackBarchartFig(df):
    df_count = pd.crosstab(df['month'], df['score'], values=df['score'], aggfunc='count')
    month_name = df_count.index.map(lambda x: calendar.month_abbr[x])
    unique_scores = df_count.columns.tolist()

    color_scheme = ['#F6A198', '#D6D8D8', '#CCD9E5', '#90A1B6', '#ABDDC3']

    # находим максимальную сумму оценок в месяц
    maximal = max(df_count.sum(axis=1).tolist())

    fig = go.Figure()

    for col, color in zip(unique_scores, color_scheme):
        fig.add_trace(go.Bar(x=month_name, y=df_count[col], marker_color=color,
                             textfont={"family": "Times New Roman", "size": 18},
                             showlegend=True, hoverinfo='y', name=col))

    fig.update_layout(autosize=True,
                      barmode='stack',
                      font_family="Times New Roman",
                      dragmode=False,
                      plot_bgcolor='white',
                      bargap=0.5,
                      xaxis=dict(showgrid=False),
                      yaxis=dict(range=[0, maximal + 1], showgrid=False),
                      margin=dict(l=0, r=0, t=15, b=5))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="left",
        x=-0,
        y=1.2,
        title='Score',
        traceorder='normal',
        title_font_family="Times New Roman",
        font=dict(
            family="Times New Roman",
            size=12,
            color="black",
        ),
    ))

    return fig
