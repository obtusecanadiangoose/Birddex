import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import sd_material_ui

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='myapplication')

mapbox_access_token = open(".mapbox_token").read()

fig = go.Figure(go.Scattermapbox(
    lat=['38.91427'],
    lon=['-77.02827'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=["The coffee bar"],

))

fig.update_layout(
    margin={
        'l': 0,
        'r': 0,
        'b': 0,
        't': 0,
        'pad': 0,
    },
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        # dragRotate=False,
        style='mapbox://styles/mapbox/outdoors-v11',
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            # lat=38.92,
            lat=43.7059439,
            # lon=-77.07
            lon=-80.3779366
        ),
        pitch=0,
        zoom=10
    ),
)

app = dash.Dash(
    '',
    external_stylesheets=[
        'https://fonts.googleapis.com/icon?family=Material+Icons',
    ]
)

app.layout = html.Div([

        # dcc.Graph(figure=fig, style={'width': '50vw', 'height': '90vh'}),
        dcc.Graph(
            id='map',
            figure=fig,
            style={'width': '80vw', 'height': '90vh', 'float': 'left', 'margin': 'auto'}
        )

])





app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
