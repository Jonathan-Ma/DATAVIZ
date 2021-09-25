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
                        id="oxygen",
                        options=[{"label": s, "value": s} for s in ['Attack', 'Death']],
                        value=[],
                        multi=True,
                    )
                ]
            )
        ),
        html.Div(id="graph-container"),
    ]
)


@app.callback(
    dash.dependencies.Output("graph-container", "children"),
    [
        dash.dependencies.Input("oxygen", "value"),
        dash.dependencies.Input("graph-update", "n_intervals"),
    ],
)
def update_graph_scatter_2(value, n):
    if value:
        # Change the line below to dynamically create the figure based on value
        fig = px.scatter(df, x="sepal_width", y="sepal_length")
        return dcc.Graph(id="live-graph2", figure=fig)
    return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
