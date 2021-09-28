import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
# the style arguments for the sidebar. We use position:fixed and a fixed width
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
        html.H2("Attack on Cholera", className="display-4"),
        html.A(
            "Jonathan Ma", href="https://jonathan-ma.github.io/"
        ),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("About", href="/", active="exact"),
                dbc.NavLink("Attacks and Deaths", href="/atk", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Container([
            dbc.Row(
                [
                    dcc.Markdown('''
                # The Broad Street Cholera Outbreak
                ##### Backstory
                John Snow (no, not King of the North dude), is considered the Father of Epidemiology for his
                contributions to stopping the 1854 cholera outbreak that killed 616 people. Preceding the 1854 outbreak,
                there were two main theories as to how cholera spread: [miasma](https://en.wikipedia.org/wiki/Miasma_theory) theory and [germ](https://en.wikipedia.org/wiki/Germ_theory_of_disease) theory.
                Snow collected and mapped data of the street addresses where there had been cholera deaths.  
                
                
            '''),
                    html.Div(html.Img(src=app.get_asset_url('Cholera-map-zoom.jpg'), style={'height': '50%', 'width': '50%'})
                             ),
                    dcc.Markdown('''
                *Each hash mark represents a cholera death*\n
                By hashing the locations of each death, Snow was able to identify a common factor of the victims; they were 
                all drinking water from the same pump.
                This brilliant use of data plotted on a map is what we would call data visualization, a simple yet
                powerful and efficient way to convey data.\n
                In this project, I attempt to use the data collected by Snow and visually represent what happened in 1854 Broad Street. By plotting simple 
                table graphs that depict the attacks and deaths of victims to more complex GIS (geographic information system) that shows locations of deaths.
                ##### Data
                [Cholera.zip](https://laulima.hawaii.edu/access/content/group/MAN.XLSICSACM484jl.202210/Cholera.zip)
                ##### Languages
                * Python
                ##### Libraries
                * Dash
                * Plotly
                * Pandas
                
        ''')
                ], justify="center", align="center", className="h-5", style={'display': 'inline-block'}
            ),

        ], style={"height": "100vh"}

        )

    elif pathname == "/atk":
        return (html.Div([
            dash_table.DataTable(
                columns=[
                    {"name": i, "id": i} for i in df.columns
                ],
                data=df.to_dict('records'),
                fixed_rows={'headers': True, 'data': 0},
                page_action='none',
                style_table={'height': '100vh', 'width': '100%'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[
                    # {'if': {'column_id': 'Attack'}, 'width': '50px'},
                    # {'if': {'column_id': 'Death'}, 'width': '50px'},
                    # {'if': {'column_id': 'Total'}, 'width': '50px'},
                    {'if': {'column_id': 'Total Attacks', },
                     'display': 'None', },
                    {'if': {'column_id': 'Total Deaths', },
                     'display': 'None', },
                    {'if': {'column_id': 'Date'},
                     'text-align': 'center'},
                ]
            )], style={'display': 'inline-block', 'overflow': 'auto', 'width': '30vw', 'margin-left': '20vw', 'margin-top': '30vh', "border": "1px black solid"}
        ),
                html.Div([
                    dcc.Graph(id="graph", figure=fig,
                              config={
                                  'scrollZoom': True,
                                  'doubleClick': 'reset',
                                  'showTips': True,
                                  'displayModeBar': 'hover',
                                  'modeBarButtonsToRemove': ['toImage'],
                              }, style={'height': '48.5vh'}),

                ], style={'display': 'inline-block', 'width': '40vw', 'height': '42.5vh', 'margin-left': '100px'})
        )

    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
