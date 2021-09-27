import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc

df = px.data.iris()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("Attack on Cholera", className="display-4"),
        html.Hr(),
        html.P(
            "Jonathan Ma", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("About", href="abt", active="exact"),
                dbc.NavLink("Page 1", href="atk", active="exact"),
                dbc.NavLink("Page 2", href="dth", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [
        dash.dependencies.Input("url", "pathname"),
    ],
)
def update_graph_scatter(value):
    if 'abt' in value:
        return dcc.Markdown('''
        # The Broad Street Cholera Outbreak
        \n
        John Snow(no, not the King of the North dude), 
        ''')
    elif 'atk' in value:
        fig = px.scatter_3d(df, x="sepal_width", y="sepal_length", z='petal_width')
        return dcc.Graph(figure=fig)

#
# @app.callback(
#     dash.dependencies.Output("graph-container2", "children"),
#     [
#         dash.dependencies.Input("dropdown", "value"),
#     ],
# )
# def update_graph_scatter2(value):
#     if 'dth' in value:
#         fig = px.scatter_3d(df, x="sepal_width", y="sepal_length", z='petal_width')
#         return dcc.Graph(figure=fig)
#     #return html.Div()
#
# @app.callback(
#     dash.dependencies.Output("graph-container3", "children"),
#     [dash.dependencies.Input("dropdown", "value")
#      ],
# )
# def update_about(value):
#     if 'abt' in value:
#         return dcc.Markdown('''
#         # About
#
#         ''')
    # return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
