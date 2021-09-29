import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc


import pandas as pd
us_cities = pd.read_csv("choleraPumpLocations.csv")

app = dash.Dash()
fig = px.scatter_mapbox(us_cities, lat="lat", lon="long",
                        zoom=14, height=300)
fig.update_layout(mapbox_style="stamen-toner")
fig.update_layout(margin={"r": 1000, "t": 0, "l": 1000, "b": 0})
fig.update_traces(marker=dict(size=12),selector=dict(mode='markers'))
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
