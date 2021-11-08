import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, ALL
from dash import dcc
from dash import html
import sd_material_ui
import dash_leaflet as dl

index = 0

app = dash.Dash(external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                                      'https://fonts.googleapis.com/icon?family=Material+Icons'],
                prevent_initial_callbacks=True)

markers = []

app.layout = html.Div([
    html.Div([
        dl.Map(
            [dl.TileLayer(), dl.LayerGroup(markers, id="markers"), dl.LocateControl(options={
                'showCompass': False,
                'locateOptions': {'enableHighAccuracy': True}})],
            id="map",
            style={'width': '80vw', 'height': '90vh', 'float': 'left', 'margin': 'auto', "display": "block"}
        ),

    ]),

    html.Div([
        sd_material_ui.DropDownMenu(
            id='dropdown-input',
            labelText='',
            labelId='dropdown-label',
            value=1,
            useGrouping=True,
            options=[
                dict(primaryText='Free Look', value=1),
                dict(primaryText='Add Marker', value=2),
                dict(primaryText='Remove Marker', value=3),
            ],
            autoWidth=True
        ),

        html.Div(id='clickdata')
    ]),

])


@app.callback([Output("markers", "children"),
              Output("clickdata", "children")],
              [Input({'type': 'filter-dropdown', 'index': ALL}, "n_clicks"),
              Input("map", "click_lat_lng")],
              [dash.dependencies.State('dropdown-input', 'value')]
)
def map_click(n_clicks, click_lat_lng, value):
    selector = dash.callback_context.triggered[-1]['prop_id']
    if selector != 'map.click_lat_lng':
        marker_id = selector[selector.find("index") + 7:selector.find(",")]
    else:
        marker_id = "Map"
    global index
    if selector == 'map.click_lat_lng':
        if value == 2:
            dl.LayerGroup(markers).children.append(dl.Marker(
                id={
                'type': 'filter-dropdown',
                'index': index
            },position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))))
            index = index + 1
        return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id)
    else:

        if value == 3:
            for i in range(len(dl.LayerGroup(markers).children)):
                index_of_bad_marker = str(dl.LayerGroup(markers).children[i])[str(dl.LayerGroup(markers).children[i]).find("index") + 8:str(dl.LayerGroup(markers).children[i]).find("}")]
                if marker_id in index_of_bad_marker:
                    dl.LayerGroup(markers).children.pop(i)
                    break

            return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id)
    return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id)


'''
@app.callback(Output("clickdata", "children"),
              Input({'type': 'filter-dropdown', 'index': ALL}, "n_clicks"),
              [dash.dependencies.State('dropdown-input', 'value')]
              )

def marker_click(n_clicks, value):
    #print(dash.callback_context.triggered)
    marker_id = dash.callback_context.triggered[-1]["prop_id"]
    marker_id = int(marker_id[marker_id.find("index") + 7:marker_id.find("index") + 8])
    if value == 3:
        dl.LayerGroup(markers).children.pop(marker_id)
    return "Last clicked marker: {}".format(marker_id)


@app.callback(Output("markers", "children"),
              Input("map", "click_lat_lng"),
              [dash.dependencies.State('dropdown-input', 'value')]
)
def map_click(click_lat_lng, value):
    global index
    if value == 2:
        dl.LayerGroup(markers).children.append(dl.Marker(
            id={
            'type': 'filter-dropdown',
            'index': index
        },position=click_lat_lng))#, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))))
        #dl.LayerGroup(markers).children.append(dl.Marker(id={'type': 'marker', 'index': 'n_clicks'}, position=click_lat_lng))#, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))))
        index = index + 1
    return dl.LayerGroup(markers)
'''


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
