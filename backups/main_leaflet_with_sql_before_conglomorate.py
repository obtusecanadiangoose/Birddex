import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, ALL, State
from dash import dcc
from dash import html
import sd_material_ui
import dash_leaflet as dl
import sqlite3

conn = sqlite3.connect("../birddex.db", check_same_thread=False)

def clk_lat_lon_id(click_lat_lng) -> str:
    lat = click_lat_lng[0]
    lon = click_lat_lng[1]
    return str(lat).replace(".", "")+str(lon).replace(".", "")

index = 0
marker_id = "Map"
lat = 0.0
lon = 0.0

app = dash.Dash(external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                                      'https://fonts.googleapis.com/icon?family=Material+Icons'],
                prevent_initial_callbacks=True)

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
                }, position=(data[1], data[2]), children=dl.Tooltip("({:.3f}, {:.3f})".format(*(data[1], data[2])))))
    index = index + 1
    print(data)

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
        html.Div([
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
                    autoWidth=False
                )], style={'float': 'middle'})],
            style={'width': '23.5vw', 'height': '5vh', 'float': 'right', 'margin': 'auto'}),
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
            dashCallbackDelay=0
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
    ]),

])

#TODO: Set up database
#TODO: Put this all into one function [should probably make a backup first

# Callback for SDAutoComplete
@app.callback(Output('searchdata', 'children'),
              [Input('autocomplete', 'selectedValue'),
                Input("assign2marker", "n_clicks")
               ],
              [dash.dependencies.State('autocomplete', 'searchText')]
              )
def autocomplete_callback(searchValue: int, searchText: str, n_clicks: int):
    global index
    global marker_id
    global lat
    global lon

    selector = dash.callback_context.triggered[-1]['prop_id']
    print(searchValue)
    if selector == 'assign2marker.n_clicks' and marker_id != "Map":
        #Does marker exist?
        curr = conn.cursor()
        setdata = "SELECT indexx from Markers WHERE indexx=" + str(marker_id)
        curr.execute(setdata)
        marker_data = curr.fetchall()

        if marker_data == []: #Entry Doesn't exist
            curr = conn.cursor()
            print(lat)
            data = [[marker_id, lat, lon, str(searchValue)]]
            for i in data:
                addData = f"""INSERT INTO Markers VALUES('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}')"""
                print(addData)  # To see all the commands iterating
                curr.execute(addData)
            conn.commit()
            index+1


        else:   #Entry Exists, update data
            curr = conn.cursor()
            setdata = "UPDATE Markers SET bird=\""+str(searchValue)+"\" WHERE indexx="+str(marker_id)
            print(setdata)
            curr.execute(setdata)
            conn.commit()


    return ['Selection is {}'.format(searchValue if searchValue else '')]


@app.callback([Output("markers", "children"),
               Output("clickdata", "children"),
               Output("markerdata", "children")],
              [Input({'type': 'filter-dropdown', 'index': ALL}, "n_clicks"),
               Input("map", "click_lat_lng"),
               ],
              [State('dropdown-input', 'value')]
              )
def map_click(n_clicks, click_lat_lng, value):
    global index
    global marker_id
    global lat
    global lon

    selector = dash.callback_context.triggered[-1]['prop_id']
    print(selector)
    marker_data = ""

    if selector != 'map.click_lat_lng': #marker clicked
        marker_id = selector[selector.find("index") + 7:selector.find(",")]

        curr = conn.cursor()
        fetchData = "SELECT bird from Markers WHERE indexx=" + str(marker_id)
        curr.execute(fetchData)
        marker_data = curr.fetchall()
        if marker_data != []:
            marker_data = marker_data[0][0]
    else:
        marker_id = "Map"

    #You can only add a point to the map if you assign data to it
    if selector == 'map.click_lat_lng':  # Add Marker
        if len(dl.LayerGroup(markers).children) > index:
            dl.LayerGroup(markers).children.pop(-1)
        dl.LayerGroup(markers).children.append(dl.Marker(
            id={
                'type': 'filter-dropdown',
                'index': index
            }, position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))))
        marker_id = index
        lat = click_lat_lng[0]
        lon = click_lat_lng[1]


        return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id), "Marker Data: {}".format(marker_data)


    """
    if selector == 'map.click_lat_lng': #Add Marker
        if value == 2:
            dl.LayerGroup(markers).children.append(dl.Marker(
                id={
                    'type': 'filter-dropdown',
                    'index': index
                }, position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))))
            print(click_lat_lng)
            index = index + 1

            return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id), "Marker Data: {}".format(marker_data)
    else:

        if value == 3:  #Remove Marker
            for i in range(len(dl.LayerGroup(markers).children)):
                index_of_bad_marker = str(dl.LayerGroup(markers).children[i])[
                                      str(dl.LayerGroup(markers).children[i]).find("index") + 8:str(
                                          dl.LayerGroup(markers).children[i]).find("}")]
                if marker_id in index_of_bad_marker:
                    dl.LayerGroup(markers).children.pop(i)
                    break

            return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id), "Marker Data: {}".format(marker_data)
    """
    return dl.LayerGroup(markers), "Last clicked marker: {}".format(marker_id), "Marker Data: {}".format(marker_data)


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
