import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc

df = px.data.iris()

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Interval(id="graph-update", interval=10000, n_intervals=0),
        dbc.Col(
            html.Div(
                [
                    dcc.Dropdown(
                        id="dropdown",
                        options=[{'label': 'About', 'value': 'abt'},{'label': 'Attack', 'value': 'atk'}, {'label': 'Death', 'value': 'dth'}],
                        value=['abt'],
                        multi=True,
                    )
                ]
            )
        ),
        html.Div(id="graph-container"),
        html.Div(id="graph-container2"),
        html.Div(id="graph-container3"),


    ]
)


@app.callback(
    dash.dependencies.Output("graph-container", "children"),
    [
        dash.dependencies.Input("dropdown", "value"),
    ],
)
def update_graph_scatter(value):
    if 'atk' in value:
        fig = px.scatter(df, x="sepal_width", y="sepal_length")
        return dcc.Graph(figure=fig)
    #return html.Div()


@app.callback(
    dash.dependencies.Output("graph-container2", "children"),
    [
        dash.dependencies.Input("dropdown", "value"),
    ],
)
def update_graph_scatter2(value):
    if 'dth' in value:
        fig = px.scatter_3d(df, x="sepal_width", y="sepal_length", z='petal_width')
        return dcc.Graph(figure=fig)
    #return html.Div()

@app.callback(
    dash.dependencies.Output("graph-container3", "children"),
    [dash.dependencies.Input("dropdown", "value")
     ],
)
def update_about(value):
    if 'abt' in value:
        return dcc.Markdown('''
        # About
        
        ''')
    # return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
