import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

mapbox_access_token = 'pk.eyJ1IjoibGlnZ21hIiwiYSI6ImNrdTZhdzJ5NDU4a3Eyd28yN200Y2hjcWYifQ.Srqhm05N6Silps_KAbRq4g'

app = dash.Dash(__name__)
# external_stylesheets=[dbc.themes.BOOTSTRAP]
server = app.server
# -----------------------------------------------------------------------------
# FILE READING
# -----------------------------------------------------------------------------

df = pd.read_csv('choleraDeaths.tsv', sep='\t')
naples = pd.read_csv('naplesCholeraAgeSexData.tsv', sep='\t', comment='#')
UK = pd.read_csv('UKcensus1851.csv', sep=',', comment='#')

# -----------------------------------------------------------------------------
# FIRST PART OF PROJECT
# -----------------------------------------------------------------------------

# creating total column for first table
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
fig = px.line()

fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Deaths'], mode='markers', name='Total Deaths', marker_color="#000000"))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Death'], mode='lines', name='Deaths', marker_color="#000000"))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Attacks'], mode='markers', name='Total Attacks', marker_color="#B8561A"))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Attack'], mode='lines', name='Attacks', marker_color="#B8561A"))

fig.update_yaxes(title_text='Cases', title_font_size=20)
fig.update_xaxes(tickangle=0, dtick=17, title_font_size=20)
fig.update_layout(title={'text': 'Death Cases', 'xanchor': 'center', 'x': 0.5, 'yanchor': 'top'}, yaxis_title="Deaths", font=dict(family="Courier New, monospace", size=20, ))
# -----------------------------------------------------------------------------
# PART TWO OF PROJECT
# -----------------------------------------------------------------------------

# making fig for bar chart compare sex and group by age
fig2 = px.bar(naples, x="Age", y=["Male", "Female"], barmode="group")
fig2.update_layout(title={'text': 'Age and Sex Death Comparison', 'xanchor': 'center', 'x': 0.5, 'yanchor': 'top'},
                   yaxis_title="Deaths",
                   font=dict(
                       family="Courier New, monospace",
                       size=20,
                   ))

# -----------------------------------------------------------------------------
# PART THREE OF PROJECT
# -----------------------------------------------------------------------------

barUK = px.bar(UK, x="age", y=["male", "female"], barmode="group")
barUK.update_layout(title='Male vs Female Population', yaxis_title='Population')
UK['total'] = UK['male'] + UK['female']

male = UK['male'].sum()
female = UK['female'].sum()
labels = ['male', 'female']
values = [male, female]
pieMf = go.Figure(data=[go.Pie(values=values, labels=labels, sort=False)])

pieMale = px.pie(UK, values='male', names='age', color_discrete_sequence=px.colors.sequential.Blues_r)
pieFemale = px.pie(UK, values='female', names='age', color_discrete_sequence=px.colors.sequential.Purples_r)

pieMale.update_layout(title='Male Population Age Distribution')
pieFemale.update_layout(title='Female Population Age Distribution')
pieMf.update_layout(title='Female vs Male Population')

# -----------------------------------------------------------------------------
# PART FOUR OF PROJECT
# -----------------------------------------------------------------------------

pump = pd.read_csv('choleraPumpLocations.csv')
site_lat = pump.lat
site_lon = pump.long

dff = pd.read_csv('choleraDeathLocations.csv')
long = dff.long
lat = dff.lat
death = dff.Deaths
GIS = go.Figure()
GIS.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    name='Pump',
    marker=go.scattermapbox.Marker(
        symbol='drinking-water',
        size=15,
        color='rgb(0, 0, 255)',
    ),
    showlegend=False
))
GIS.add_trace(go.Scattermapbox(
    lat=lat,
    lon=long,
    mode='markers',
    name='Death',
    text=death,
    marker=go.scattermapbox.Marker(
        size=death * 3,
        color='rgb(255, 0, 0)',
        opacity=0.4
    ),
    hoverinfo='text',
    showlegend=True
))
GIS.update_layout(
    autosize=True,
    height=700,
    width=700,
    hovermode='closest',

    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=51.513227,
            lon=-0.135801
        ),
        zoom=15
    ),
)

# -----------------------------------------------------------------------------
# LAYOUT
# -----------------------------------------------------------------------------
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#000000",
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
        html.H2("Attack on Cholera", className="display-4", style={'color': 'white'}),
        html.P("by", style={'color': 'white'}),
        html.A(
            "Jonathan Ma", href="https://jonathan-ma.github.io/"
        ),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("About", href="/", active="exact"),
                dbc.NavLink("Attacks and Deaths", href="/atk", active="exact"),
                dbc.NavLink("Fatalities by Age and Sex", href="/page-2", active="exact"),
                dbc.NavLink("UK Census", href="/page-3", active="exact"),
                dbc.NavLink("GIS", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# -----------------------------------------------------------------------------
# CALLBACK
# -----------------------------------------------------------------------------
icon1 = {
    'Slide1': '/assets/Cholera-map-zoom.png',
}


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
                    dbc.CardImg(src=icon1['Slide1'], style={'height': '50%', 'width': '50%'}),
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
        return (
            html.Div(
                dash_table.DataTable(
                    columns=[
                        {"name": x, "id": x} for x in df.columns
                    ],
                    data=df.to_dict('records'),
                    fixed_rows={'headers': True, 'data': 0},
                    page_action='none',
                    style_table={'height': '100vh', 'width': '410px'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'Attack'}, 'padding-right': '10px', 'padding-left': '10px'},
                        {'if': {'column_id': 'Death'}, 'padding-right': '10px'},
                        {'if': {'column_id': 'Total'}, 'padding-right': '10px'},
                        {'if': {'column_id': 'Total Attacks', },
                         'display': 'None', },
                        {'if': {'column_id': 'Total Deaths', },
                         'display': 'None', },
                        {'if': {'column_id': 'Date'},
                         'text-align': 'center'},
                    ]
                ), style={'display': 'inline-block', 'overflow': 'auto', 'width': '365', 'margin-left': '10px', 'margin-top': '10px', "border": "1px black solid"}
            ),
            html.Div(
                dcc.Graph(id="graph", figure=fig,
                          config={
                              'scrollZoom': True,
                              'doubleClick': 'reset',
                              'showTips': True,
                              'displayModeBar': 'hover',
                              'modeBarButtonsToRemove': ['toImage'],
                          },
                          style={'height': '597px'}
                          ), style={'display': 'inline-block', 'width': '750px', 'height': '600px', 'margin-left': '10px', "border": "1px black solid", 'margin-top': '10px'}
            )
        )

    elif pathname == "/page-2":
        return html.Div([
            html.Div(dash_table.DataTable(
                id='table',
                columns=[{"name": y, "id": y} for y in naples.columns],
                data=naples.to_dict('records'),
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_table={'height': '', 'width': '300px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'Age'}, 'width': '50px'},
                    {'if': {'column_id': 'Male'}, 'width': '50px'},
                    {'if': {'column_id': 'Female'}, 'width': '50px'},
                    {'if': {'column_id': 'Age'}, 'text-align': 'center'}
                ]
            ), style={'border': '1px solid black', 'display': 'inline-block', 'overflow': 'auto', 'margin-left': '10px', 'margin-top': '10px'}),
            html.Div(
                dcc.Graph(figure=fig2),
                style={'border': '1px solid black', 'display': 'inline-block', 'width': '750px', 'margin-top': '10px', 'margin-left': '10px'}
            )
        ])

    elif pathname == "/page-3":
        return html.Div([
            html.Div([

                html.Div(
                    dash_table.DataTable(
                        id='table2',
                        columns=[{"name": x, "id": x} for x in UK.columns],
                        data=UK.to_dict('records'),
                        style_table={'height': '310px', 'width': '400px'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': 'age'}, 'width': '100px', 'text-align': 'center'},
                            {'if': {'column_id': 'male'}, 'width': '100px', 'padding-left': '10px', 'padding-right': '10px'},
                            {'if': {'column_id': 'female'}, 'width': '100px', 'padding-left': '10px', 'padding-right': '10px'},
                            {'if': {'column_id': 'total'}, 'width': '100px', 'padding-left': '10px', 'padding-right': '10px'}]
                    ), style={'width': '401px', 'height': '311px', 'margin-left': '5px', 'border': '1px solid black', 'display': 'inline-block', 'overflow': 'auto'}
                ),
                html.Div(dcc.Graph(figure=pieMf, style={'height': '309px'}),
                         style={'width': '493px', 'height': '311px', 'display': 'inline-block', 'margin-left': '5px',
                                'border': '1px solid black'}),
                html.Div(
                    (dcc.Graph(figure=barUK)), style={'width': '900px', 'display': 'inline-block', 'margin-left': '5px', 'border': '1px solid black'}),
                # html.Div(dcc.Graph(figure=pieMf), style={'width': '400px', 'display': 'inline-block', 'margin-left': '5vw', 'border': '1px solid black'})
            ]),

            html.Div(dcc.Graph(figure=pieMale), style={'width': '600px', 'display': 'inline-block', 'margin-left': '5px', 'border': '1px solid black'}),
            html.Div(dcc.Graph(figure=pieFemale), style={'width': '600px', 'display': 'inline-block', 'margin-left': '5px', 'border': '1px solid black'}),

        ], style={'margin-left': '20px'})

    elif pathname == '/page-4':
        return html.Div([
            dcc.Graph(figure=GIS)
        ], style={'width': '50vw', 'height': '50vh', 'margin-left': '5vw'})

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
