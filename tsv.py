import dash
import dash_table
import pandas as pd
from dash import html, Output
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go

app = dash.Dash(__name__)
# reading in tsv file
df = pd.read_csv('choleraDeaths.tsv', sep='\t')
df['Total'] = df['Attack'] + df['Death']

a = []
for i in df['Attack']:
    a.append(i)

b = []
c = 0
for i, elem in enumerate(a):
    if a[i - 1] < len(a):
        c = c + a[i]
    else:
        c = c + a[i - 1]
    b.append(c)

df['Total Attacks'] = b
# data for line chart and title change for y axes
fig = px.line(df, x='Date', y=['Attack', 'Death', 'Total Attacks'], markers=True)
fig.update_yaxes(title_text='Cases', title_font_size=20)
fig.update_xaxes(tickangle=0, dtick=7, title_font_size=20)
# app layout
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            columns=[
                {"name": i, "id": i} for i in df.columns
            ],

            data=df.to_dict('records'),
            fixed_rows={'headers': True, 'data': 0},
            page_action='none',
            style_table={'height': '500px', 'overflowX': 'auto'},
            style_cell_conditional=[
                {'if': {'column_id': 'Total Attacks', },
                 'display': 'None', }]
        )
    ]),
    html.Div([

        dcc.Graph(id="graph", figure=fig,
                  config={
                      'scrollZoom': True,
                      'doubleClick': 'reset',
                      'showTips': True,
                      'displayModeBar': 'hover',
                      'modeBarButtonsToRemove': ['toImage']
                  }
                  )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
