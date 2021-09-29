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
# uk census
UK['Total'] = UK['male'] + UK['female']
male = UK['male'].sum()
female = UK['female'].sum()
labels = ['Male', 'Female']
values = [male,female]
# uk census piechart for men
pieMale = px.pie(UK, values='male', names='age')
pieFemale = px.pie(UK, values='female', names='age')
pieMf = go.Figure(data=[go.Pie(values=values, labels=labels)])
barUK = px.bar(UK, x="age", y=["male", "female"], barmode="group")
###################################

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
    ), style={'border': '1px solid black'}),
    html.Div(dash_table.DataTable(
        id='table2',
        columns=[{"name": a, "id": a} for a in UK.columns],
        data=UK.to_dict('records'),
        style_table={'height': '300px', 'width': '300px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'age'}, 'width': '100px'},
            {'if': {'column_id': 'male'}, 'width': '100px'},
            {'if': {'column_id': 'female'}, 'width': '100px'}, ]
    ), style={'border': '1px solid black'}),
    html.Div(html.H1('Male'), style={'border': '1px solid black', 'width': '900px', 'display': 'inline-block'}),
    html.Div(html.H1('Female'), style={'border': '1px solid black', 'width': '900px', 'display': 'inline-block'}),
    html.Div(dcc.Graph(figure=pieMale), style={'border': '1px solid black', 'width': '900px', 'display': 'inline-block'}),
    html.Div(dcc.Graph(figure=pieFemale), style={'border': '1px solid black', 'width': '900px', 'display': 'inline-block'}),
    html.Div(dcc.Graph(figure=barUK)),
    html.Div(dcc.Graph(figure=pieMf), style={'border': '1px solid black', 'width': '900px'}),

], style={'margin-left': '200px'})

if __name__ == '__main__':
    app.run_server(debug=True)
