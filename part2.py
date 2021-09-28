import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# reading in file
df = pd.read_csv('naplesCholeraAgeSexData.tsv', sep='\t', comment='#')
UK = pd.read_csv('UKcensus1851.csv', sep=',', comment='#')

app = dash.Dash(__name__)

fig = px.bar(df, x="Age", y=["Male", "Female"], barmode="group")
UK['Total'] = UK['male'] + UK['female']

app.layout = html.Div([
    html.Div(
        dcc.Graph(figure=fig)
    ),
    html.Div(dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'height': '400px', 'width': '300px'},
        style_cell_conditional=[
            {'if': {'column_id': 'Age'}, 'width': '50px'},
            {'if': {'column_id': 'Male'}, 'width': '50px'},
            {'if': {'column_id': 'Female'}, 'width': '50px'}, ]
    )),
    html.Div(dash_table.DataTable(
        id='table2',
        columns=[{"name": a, "id": a} for a in UK.columns],
        data=UK.to_dict('records'),
        style_table={'height': '1000px', 'width': '300px'},
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
        style_cell_conditional=[
            {'if': {'column_id': 'age'}, 'width': '100px'},
            {'if': {'column_id': 'male'}, 'width': '100px'},
            {'if': {'column_id': 'female'}, 'width': '100px'}, ]
    ))
])

if __name__ == '__main__':
    app.run_server(debug=True)
