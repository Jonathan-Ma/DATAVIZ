import dash
import dash_table
import pandas as pd
from dash import html
import dash_core_components as dcc
import plotly.express as px

app = dash.Dash(__name__)
# reading in tsv file
df = pd.read_csv('choleraDeaths.tsv', sep='\t')
df['Total'] = df['Attack'] + df['Death']

# loop through attack append in new list
attack = []
for i in df['Attack']:
    attack.append(i)
# make another list and enumerate list a to access prev elem
a = []
c = 0
for i, elem in enumerate(attack):
    if attack[i - 1] < len(attack):
        c = c + attack[i]
    else:
        c = c + attack[i - 1]
    a.append(c)
df['Total Attacks'] = a
# same procedure for total deaths
c = 0
deaths = []
for i in df['Death']:
    deaths.append(i)
b = []
for i, elem in enumerate(deaths):
    if deaths[i - 1] < len(deaths):
        c += deaths[i]
    else:
        c += deaths[i - 1]
    b.append(c)
df['Total Deaths'] = b

# data for line chart and title change for y axes
fig = px.line(df, x='Date', y=['Attack', 'Death', 'Total Attacks', 'Total Deaths'], markers=True)
fig.update_yaxes(title_text='Cases', title_font_size=20)
fig.update_xaxes(tickangle=0, dtick=7, title_font_size=20)
# app layout
app.layout = html.Div([
    html.Div(
        html.H1('Attack on Cholera', style={'textAlign': 'center', 'color': '#7FDBFF'})
    ),
    html.Div(
        html.H1('About', style={'textAlign': 'left'})
    ),
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
                 'display': 'None', },
                {'if': {'column_id': 'Total Deaths', },
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
