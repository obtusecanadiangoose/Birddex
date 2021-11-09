import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, ALL, State
from dash import dcc
from dash import html
import sd_material_ui
import dash_leaflet as dl
import sqlite3


def lat_lon_id(lat: float, lon: float) -> str:
    return str(lat).replace(".", "") + str(lon).replace(".", "")


def clk_lat_lon_id(click_lat_lng) -> str:
    lat = click_lat_lng[0]
    lon = click_lat_lng[1]
    return str(lat).replace(".", "") + str(lon).replace(".", "")


conn = sqlite3.connect("birddex.db", check_same_thread=False)

searched = "null"

app = dash.Dash(external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                                      'https://fonts.googleapis.com/icon?family=Material+Icons'],
                prevent_initial_callbacks=True)

icon_green = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -34]
}

icon_red = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -34]
}

icon_blue = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -34]
}

curr = conn.cursor()
fetchData = "SELECT * from Markers"
curr.execute(fetchData)
answer = curr.fetchall()
markers = []
# We print the data
for data in answer:
    markers.append(dl.Marker(
        id={
            'type': 'filter-dropdown',
            'index': data[0]
        }, position=(data[1], data[2]), children=dl.Tooltip("({:.3f}, {:.3f})".format(*(data[1], data[2]))),
        bubblingMouseEvents=True, icon=icon_blue
    ))
    print(data)
    last_used_marker = data[0]

app.layout = html.Div([
    html.Div([
        dl.Map(
            [dl.TileLayer(), dl.LayerGroup(markers, id="markers"), dl.LocateControl(options={
                'showCompass': False,
                'locateOptions': {'enableHighAccuracy': True}})],
            id="map",
            style={'width': '75vw', 'height': '90vh', 'float': 'left', 'margin': 'auto', "display": "block"}
        ),

    ]),
    html.Div([
        sd_material_ui.Divider(),
        html.Div(children=[], style={'height': '1vh', 'width': '23.5vw'}),
        html.Div(id='markerdata'),
        html.Div(id='clickdata'),
        html.Div(id='searchdata'),
        html.Div(children=[], style={'height': '1vh', 'width': '23.5vw'}),

        sd_material_ui.AutoComplete(
            style={'width': '23.5vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'},
            id='autocomplete',
            dataSource=[{'label': 'Austin, TX', 'value': 'Austin'},
                        {'label': 'Houston, TX', 'value': 'Houston'},
                        {'label': 'New York, NY', 'value': 'New York'},
                        {'label': 'Denver, CO', 'value': 'Denver'},
                        {'label': 'Chicago, IL', 'value': 'Chicago'},
                        {'label': 'Detroit, MI', 'value': 'Detroit'},
                        {'label': 'Los Angeles, CA', 'value': 'Los Angeles'}],
            dashCallbackDelay=0, hintText="Enter City", classes={"noOptions": "True"}
        ),
        html.Div(children=[], style={'height': '10vh', 'width': '23.5vw'}),
        sd_material_ui.Button(
            children=html.P('Assign to Marker'),
            id='assign2marker',
            n_clicks=0,
            disableShadow=False,
            useIcon=False,
            variant='contained',
            style={'width': '23.5vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}
        ),

        # html.Div(children=[], style={'height': '7vh', 'width': '23.5vw'}),
        # sd_material_ui.Button(
        #    children=html.P('Remove Marker'),
        #    id='deleteMarker',
        #    n_clicks=0,
        #    disableShadow=False,
        #    useIcon=False,
        #    variant='contained',
        #    style={'width': '23.5vw', 'height': '3vh', 'float': 'right', 'margin': 'auto', 'display': 'none'}
        # ),

        sd_material_ui.Dialog([
            #html.P('Really Delete?'),
            html.Div(children=[html.P('Really Delete?')], style={'text-align': 'center'}),
            #html.Div(html.Button('Yes'), id='del_yes'),
            sd_material_ui.Button(
                children=html.P('Yes'),
                id='del_yes',
                n_clicks=0,
                disableShadow=False,
                useIcon=False,
                variant='contained',
                style={'width': '300px', 'float': 'left'}
            ),
            #html.Div(html.Button('No'), id='del_no')
            sd_material_ui.Button(
                children=html.P('No'),
                id='del_no',
                n_clicks=0,
                disableShadow=False,
                useIcon=False,
                variant='contained',
                style={'width': '300px', 'float': 'right'}
            ),
        ], style={'justify': 'center'}, id='output2'),
        html.Div(id='deleteMarker', children=[
            sd_material_ui.Button(
                children=html.P('Remove Marker'),
                id='deleteMarker2',
                n_clicks=0,
                disableShadow=False,
                useIcon=False,
                variant='contained',
                style={'width': '23.5vw', 'height': '3vh', 'float': 'right', 'margin': 'auto', 'display': 'none'}
            ),
        ], style={'width': '23.5vw', 'height': '3vh', 'float': 'right', 'margin': 'auto', 'display': 'flex'}),
    ]),
])


# TODO: move "select bird" to a function.


# Callback for SDAutoComplete
@app.callback(Output('searchdata', 'children'),
              [Input('autocomplete', 'selectedValue'),
               ],
              [dash.dependencies.State('autocomplete', 'searchText')]
              )
def autocomplete_callback(searchValue: int, searchText: str):
    global searched
    searched = searchValue

    return ['Selection is {}'.format(searchValue if searchValue else '')]


##############################################
# I learned nothing about clean architecture #
##############################################
@app.callback([Output("markers", "children"),
               Output("clickdata", "children"),
               Output("markerdata", "children"),
               Output("deleteMarker2", "style"),
               Output('output2', 'open')],
              [Input({'type': 'filter-dropdown', 'index': ALL}, "n_clicks"),
               Input("map", "click_lat_lng"),
               Input("assign2marker", "n_clicks"),
               Input("deleteMarker", "n_clicks"),
               Input('deleteMarker', 'n_clicks'),
               Input('del_yes', 'n_clicks'),
               Input('del_no', 'n_clicks')],
              [State('output2', 'open')
               ],
              )
def map_click(n_clicks, click_lat_lng, assign_clicks, delete_clicks,
              modal_click: int, del_yes: int, del_no: int, open_state: bool):
    global searched

    selector = dash.callback_context.triggered[-1]['prop_id']
    print(selector)

    for marker in dl.LayerGroup(markers).children:  # reset all markers to blue
        marker.icon = icon_blue

    for marker in dl.LayerGroup(markers).children:  # then make the clicked one green
        marker_index = str(marker.id['index'])
        if marker_index in clk_lat_lon_id(click_lat_lng):
            marker.icon = icon_green
            break

    curr = conn.cursor()
    fetchData = "SELECT bird from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
    curr.execute(fetchData)
    marker_data = curr.fetchall()
    if marker_data != []:
        marker_data = marker_data[0][0]
    else:
        marker_data = "penisNULL"

    """
    if selector != 'map.click_lat_lng' and selector != 'assign2marker.n_clicks'\
            and selector != 'deleteMarker.n_clicks': #marker clicked
        marker_id = selector[selector.find("index") + 7:selector.find(",")]

        curr = conn.cursor()
        fetchData = "SELECT bird from Markers WHERE indexx=" + str(marker_id)
        curr.execute(fetchData)
        marker_data = curr.fetchall()
        if marker_data != []:
            marker_data = marker_data[0][0]
    """

    # You can only add a point to the map if you assign data to it
    if selector == 'map.click_lat_lng':  # Add Marker

        # Get # of saved entries
        curr = conn.cursor()
        setdata = "SELECT * from Markers"
        curr.execute(setdata)
        marker_num = curr.fetchall()

        if len(dl.LayerGroup(markers).children) > len(marker_num):  # if there's more markers on screen than saved ones
            dl.LayerGroup(markers).children.pop(-1)  # pop the most recent one (bc the user didn't save it)

        # check if there's already a saved marker at this lat/lon
        curr = conn.cursor()
        fetchData = "SELECT bird from Markers WHERE indexx=\'" + str(clk_lat_lon_id(click_lat_lng)) + "\'"
        curr.execute(fetchData)
        marker_num = curr.fetchall()

        if marker_num == []:
            dl.LayerGroup(markers).children.append(dl.Marker(
                id={
                    'type': 'filter-dropdown',
                    'index': clk_lat_lon_id(click_lat_lng)
                }, position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)),
                bubblingMouseEvents=True, icon=icon_red
            ))

        curr = conn.cursor()
        fetchData = "SELECT bird from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
        curr.execute(fetchData)
        marker_data = curr.fetchall()
        if marker_data != []:
            marker_data = marker_data[0][0]
        else:
            marker_data = "penisNULL"

        removeMarkerVisible = 'flex'

    if selector == 'deleteMarker.n_clicks':
        if not open_state:
            deletedialog = True
        else:
            deletedialog = False
        removeMarkerVisible = 'flex'
    else:
        deletedialog = False
        # removeMarkerVisible = 'flex'

    if selector == 'del_no.n_clicks':  # delete a marker
        deletedialog = False
        removeMarkerVisible = 'flex'

    if selector == 'del_yes.n_clicks':

        for marker in dl.LayerGroup(markers).children:
            marker_index = str(marker.id['index'])
            if marker_index in clk_lat_lon_id(click_lat_lng):
                dl.LayerGroup(markers).children.remove(marker)
                break

        curr = conn.cursor()
        setdata = "DELETE FROM Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
        print(setdata)
        curr.execute(setdata)
        conn.commit()

        removeMarkerVisible = 'none'

    if selector == 'assign2marker.n_clicks':
        # print("marker_id to assign to: "+marker_id)############################################
        # Does marker exist?
        curr = conn.cursor()
        setdata = "SELECT indexx from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
        curr.execute(setdata)
        marker_data = curr.fetchall()

        if marker_data == []:  # Entry Doesn't exist
            curr = conn.cursor()
            data = [[clk_lat_lon_id(click_lat_lng), click_lat_lng[0], click_lat_lng[1], str(searched)]]
            for i in data:
                addData = f"""INSERT INTO Markers VALUES('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}')"""
                print(addData)  # To see all the commands iterating
                curr.execute(addData)
            conn.commit()

            for marker in dl.LayerGroup(markers).children:  # then make the clicked one green
                marker_index = str(marker.id['index'])
                if marker_index in clk_lat_lon_id(click_lat_lng):
                    marker.icon = icon_green
                    break

        else:  # Entry Exists, update data
            print("entry exists")
            curr = conn.cursor()
            setdata = "UPDATE Markers SET bird=\"" + str(searched) + "\" WHERE indexx=\"" + \
                      str(clk_lat_lon_id(click_lat_lng)) + "\""
            print(setdata)
            curr.execute(setdata)
            conn.commit()

        curr = conn.cursor()
        fetchData = "SELECT bird from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
        curr.execute(fetchData)
        marker_data = curr.fetchall()
        if marker_data != []:
            marker_data = marker_data[0][0]
        else:
            marker_data = "penisNULL"
        removeMarkerVisible = 'flex'

    return dl.LayerGroup(markers), "Last clicked marker: {}".format(
        clk_lat_lon_id(click_lat_lng)), "Marker Data: {}".format(marker_data), \
           {'width': '23.5vw', 'height': '3vh', 'float': 'right', 'margin': 'auto',
            'display': removeMarkerVisible}, deletedialog


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
