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
    html.Div([
        dcc.Input(
            id="input1",
            type="text",
            placeholder="centre location",
            style={'width': '18vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}
        ),

        dcc.Graph(
            id='map',
            figure=fig,
            style={'width': '80vw', 'height': '90vh', 'float': 'left', 'margin': 'auto'}
        ),
        html.Pre(
            id='structure',
            style={
                'border': 'thin lightgrey solid',
                'overflowY': 'scroll',
                'height': '275px'
        }
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

"""
@app.callback(
    Output("map", "figure"),
    Input("button1", "n_clicks"),
    Input('button2', 'n_clicks'),
    [dash.dependencies.State('input1', 'value')]
)
def change_map_centre(btn1, btn2, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    if changed_id == "button1.n_clicks":
        print("Button 1 Clicked")
        location = geolocator.geocode(value)
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
                    lat=location.latitude,
                    # lon=-77.07
                    lon=location.longitude
                ),
                pitch=0,
                zoom=10
            ),
        )
        return fig

    elif changed_id == "button2.n_clicks":
        print("Button 2 Clicked")
        return fig
    else:
        print("nothing clicked yet...")
        return fig
        
"""
@app.callback(
    Output("structure", "children"),
    [Input("graph", "figure")])
def display_structure(fig_json):
    return 0#json.dumps(fig_json, indent=2)


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
