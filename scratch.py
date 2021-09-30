import plotly.graph_objects as go
import pandas as pd
from dash import html
from dash import dcc
import dash

mapbox_access_token = 'pk.eyJ1IjoibGlnZ21hIiwiYSI6ImNrdTZhdzJ5NDU4a3Eyd28yN200Y2hjcWYifQ.Srqhm05N6Silps_KAbRq4g'
app = dash.Dash()
df = pd.read_csv('choleraPumpLocations.csv')
site_lat = df.lat
site_lon = df.long

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=17,
        color='rgb(255, 0, 0)',
        opacity=0.5
    ),
    hoverinfo='text',

))
fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=51.512354,
            lon=-0.13163
        ),
        pitch=0,
        zoom=13
    ),
)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
