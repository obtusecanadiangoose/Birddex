import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import sd_material_ui
import dash_leaflet as dl

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='myapplication')

mapbox_access_token = open(".mapbox_token").read()

app = dash.Dash(
    '',
    prevent_initial_callbacks=True,
    external_stylesheets=[
        'https://fonts.googleapis.com/icon?family=Material+Icons',
    ]
)

markers = [dl.Marker(position=[56, 10]), dl.CircleMarker(center=[55, 10])]

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id="input1",
            type="text",
            placeholder="centre location",
            style={'width': '18vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}
        ),
        dl.Map(
            [dl.TileLayer(), dl.LayerGroup(markers), dl.LayerGroup(id="layer")],
            id="map",
            style={'width': '80vw', 'height': '90vh', 'float': 'left', 'margin': 'auto'}
        ),

    ]),
    html.Div([
        sd_material_ui.Button(
            children=html.P('Recentre Map'),
            id='button1',
            n_clicks=0,
            disableShadow=False,
            useIcon=False,
            variant='contained',
            style={'width': '18.5vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}
        ),
    ]),
    html.Div([
        sd_material_ui.Button(
            children=html.P('Add Marker'),
            id='button2',
            n_clicks=0,
            disableShadow=False,
            useIcon=False,
            variant='contained',
            style={'width': '18.5vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}
        ),
    ])
])


@app.callback(Output("layer", "children"), [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
    print(dl.LayerGroup(id="layer").children)

    return dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
