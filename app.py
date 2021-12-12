import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_leaflet as dl
import sqlite3
from data import bird_list, latin_and_common_from_code, no_image
import dash_dangerously_set_inner_html



def lat_lon_id(lat: float, lon: float) -> str:
    return str(lat).replace(".", "") + str(lon).replace(".", "")


def clk_lat_lon_id(click_lat_lng) -> str:
    lat = click_lat_lng[0]
    lon = click_lat_lng[1]
    return str(lat).replace(".", "") + str(lon).replace(".", "")


conn = sqlite3.connect("birddex.db", check_same_thread=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

icon_green = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -340]
}

icon_red = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -340]
}

icon_blue = {
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "shadowSize": [41, 41],
    "iconAnchor": [12, 41],
    # "shadowAnchor": [4, 62],
    "popupAnchor": [1, -340]
}

curr = conn.cursor()
fetchData = "SELECT * from Markers"
curr.execute(fetchData)
answer = curr.fetchall()
markers = []
# We print the data
for data in answer:
    species = latin_and_common_from_code[data[3]]
    bird_name = species[0]
    markers.append(dl.Marker(
        id={
            'type': 'filter-dropdown',
            'index': data[0]
        }, position=(data[1], data[2]), children=dl.Tooltip(bird_name),
        bubblingMouseEvents=True, icon=icon_blue
    ))

app.layout = \
    html.Div(id="wrapper", children=[
        html.Nav(className="navbar navbar-dark align-items-start sidebar sidebar-dark accordion bg-gradient-primary p-0",
            style={"font-size": "1.5rem"}, children=[
            html.Div(className="container-fluid d-flex flex-column p-0", children=[
                html.A(className="navbar-brand d-flex justify-content-center align-items-center sidebar-brand m-0", href="#", children=[
                    html.Div(className="sidebar-brand-icon rotate-n-15", children=[
                        html.I(className="fas fa-laugh-wink")
                    ]),
                    html.Div(className="sidebar-brand-text mx-3", children=[
                        html.Span("Birddex", style={"font-size": "1.5rem"})
                    ])
                ]),
                html.Hr(className="sidebar-divider my-0"),
                html.Ul(className="navbar-nav text-light", id="accordianSidebar", children=[
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link active", style={"font-size": "1.5rem"}, children=["Map Entry"])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", style={"font-size": "1.5rem"}, children=["Stats for Nerds"])
                    ])
                ]),
                html.Div(className="text-center d-none d-md-inline", children=[
                   html.Button(className="btn rounded-circle border-0", id="sidebarToggle", type="button")
                ])
            ]),
        ]),
        html.Div(className="d-flex flex-column", id="content-wrapper", children=[
            html.Div(id="content", children=[
                #html.Nav(className="navbar navbar-dark navbar-expand accordian bg-gradient-primary shadow mb-0 topbar static-top", style={"font-size": "1.5rem"}, children=[
                #]),
                html.Div(className="container-fluid", children=[
                    html.Div(className="d-sm-flex justify-content-between align-items-center mb-4", children=[
                    ]),
                    html.Div(className="row", children=[
                        html.Div(className="col-lg-7 col-xl-8", style={"height": "96vh"}, children=[
                            html.Div(id="clickdata"),
                            html.Div(className="card shadow mb-4", children=[
                                html.Div(className="card-body", children=[
                                    html.Div(className="chart-area", style={"height": "66.6667vh"}, children=[
                                        dl.Map(
                                            [dl.TileLayer(), dl.LayerGroup(markers, id="markers"),
                                             dl.LocateControl(options={
                                                 'showCompass': False,
                                                 'locateOptions': {'enableHighAccuracy': True}})],
                                            id="map"
                                        ),
                                    ]),
                                ]),
                            ]),
                        ]),
                        html.Div(className="col-lg-5 col-xl-4", children=[
                            html.Div(className="card shadow mb-4", children=[
                                html.Div(className="card-body", children=[
                                    dcc.Loading(id="loading-1", type="default",children=[
                                            html.Div(className="chart-area", style={"height": "66.6667vh"}, children=[
                                                ######## RIGHT PANEL
                                                html.P(id="intro",
                                                       children=["Click the map to create a marker, or select an"
                                                                 " existing marker to get started"],
                                                       style={"margin": "0 0",
                                                              "font-size": "1.5rem",
                                                              "display": "block",
                                                              "text-align": "center"
                                                              }),

                                                html.Strong(id="bird_name", children=["Grey Squirrel"],
                                                            style={"font-size": "1.5rem",
                                                                   "display": "none"  ###block, none
                                                                   }),

                                                dcc.Dropdown(className="bg-light border-0 small",
                                                             id="bird_name_input", search_value="",
                                                             placeholder="Bird Name",
                                                             options=bird_list,
                                                             style={"font-size": "1.5rem", "display": "none"
                                                                    ###block, none
                                                                    }),

                                                html.Img(id="bird_picture", className="shadow",
                                                         src="assets/imgs/dogs/image3.jpeg",
                                                         style={"height": "25vh",
                                                                "width": "100%", "padding": "0px 0px",
                                                                "background-color": "#fff",
                                                                "border": "1px solid #D1D1D1", "border-radius": "4px",
                                                                "box-shadow": "none",
                                                                "box-sizing": "border-box", "margin": "1rem 0",
                                                                "fontFamily": "inherit",
                                                                "display": "none"}),  # None, block

                                                dcc.Upload(id="upload_bird", children=html.Div(['Drag and Drop or ',
                                                                                                html.A('Select Files')
                                                                                                ]),
                                                           style={
                                                               'width': '100%',
                                                               'height': '60px',
                                                               'display': 'none',  # none. block
                                                               'lineHeight': '60px',
                                                               'borderWidth': '1px',
                                                               'borderStyle': 'dashed',
                                                               'borderRadius': '5px',
                                                               'textAlign': 'center',
                                                               "margin": "1rem 0",
                                                               "font-size": "1.5rem"
                                                           },
                                                           # Allow multiple files to be uploaded
                                                           multiple=False),
                                                html.Div(className="col", style={"display": "flex"}, children=[
                                                    html.I(id="bird_latin", children=["Sciurus carolinensis"],
                                                           style={"margin": "0 0",
                                                                  "font-size": "1.3rem",
                                                                  "display": "none",  # none. block
                                                                  "width": "50%"
                                                                  }),

                                                    html.I(id="bird_group", children=["Critters"],
                                                           style={"margin": "0 0",
                                                                  "font-size": "1.3rem",
                                                                  "display": "none",  # none. block
                                                                  "text-align": "right",
                                                                  "width": "50%"
                                                                  }),
                                                ]),
                                                html.P(id="bird_blurb",
                                                       children=["The eastern gray squirrel, also known as simply "
                                                                 "the grey squirrel, is a tree squirrel in the genus "
                                                                 "Sciurus. It is native to eastern North America, "
                                                                 "where it is the most prodigious and ecologically "
                                                                 "essential natural forest regenerator."],
                                                       style={"margin": "0 0",
                                                              "font-size": "1.5rem",
                                                              "display": "none"  # none block
                                                              }),

                                                html.Span(id="bird_dot_1", style={"height": "25px",
                                                                                  "width": "25px",
                                                                                  "background-color": "#bbbbbb",
                                                                                  "border-radius": "50%",
                                                                                  "display": "none",
                                                                                  # None, inline-block
                                                                                  "border": "1px solid #858796",
                                                                                  "margin": "1rem 0"
                                                                                  }),

                                                html.Span(id="bird_dot_2", style={"height": "25px",
                                                                                  "width": "25px",
                                                                                  "background-color": "#bbbbbb",
                                                                                  "border-radius": "50%",
                                                                                  "display": "none",
                                                                                  # None, inline-block
                                                                                  "border": "1px solid #858796",
                                                                                  "margin": "1rem 0.5rem"
                                                                                  }),

                                                html.Span(id="bird_dot_3", style={"height": "25px",
                                                                                  "width": "25px",
                                                                                  "background-color": "#bbbbbb",
                                                                                  "border-radius": "50%",
                                                                                  "display": "none",
                                                                                  # None, inline-block
                                                                                  "border": "1px solid #858796",
                                                                                  "margin": "1rem 0"
                                                                                  }),

                                                html.I(id="notes", children=["Notes:"], style={"margin": "0 0",
                                                                                               "font-size": "1.3rem",
                                                                                               "display": "none"}),
                                                html.P(id="bird_notes", children=["Look at this chubby lil guy"],
                                                       style={
                                                           "font-size": "1.5rem", "display": "none", "height": "10vh"
                                                       }),

                                                dcc.Textarea(id="bird_notes_input", className="form-control", rows="6",
                                                             placeholder="Notes:", style={
                                                        "font-size": "1.5rem", "display": "none", "height": "10vh"
                                                    }),

                                                html.Button(
                                                    className="btn btn-primary btn-user w-100",
                                                    children=html.P('Edit Marker'),
                                                    id='editMarker',
                                                    n_clicks=0,
                                                    style={"font-size": "1.5rem", 'display': 'none',
                                                           "position": "absolute",
                                                           "bottom": "0", "left": "0"}
                                                ),

                                                html.Button(
                                                    className="btn btn-primary btn-user w-100",
                                                    children=html.P('Save Marker'),
                                                    id='saveMarker',
                                                    n_clicks=0,
                                                    style={"font-size": "1.5rem", 'display': 'none',
                                                           "position": "absolute",
                                                           "bottom": "3rem", "left": "0", "margin": "1rem 0"}
                                                ),
                                                dcc.ConfirmDialogProvider(id='deleteMarkerWrapper',
                                                                          message="This will delete the currently selected marker, are you sure?",
                                                                          children=[html.Button(
                                                                              className="btn btn-user w-100",
                                                                              children=['Delete Marker'],
                                                                              id='deleteMarker',
                                                                              n_clicks=0,
                                                                              style={"font-size": "1.5rem",
                                                                                     'display': 'none',
                                                                                     "position": "absolute",
                                                                                     "bottom": "0", "left": "0", }
                                                                              # "margin": "1rem 0", }
                                                                          ), ]
                                                                          ),
                                            ]),
                                        ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            html.Div(className="container my-auto", children=[
                html.Div(className="text-center my-auto copyright", children=[
                    html.Span(className="text-center my-auto copyright", children=["Copyright © Brand 2021"
                                                                                   ]),
                ]),
            ]),
        ]),
    ])


##############################################
# I learned nothing about clean architecture #
##############################################
@app.callback([Output("markers", "children"),
               Output("clickdata", "children"),
               ###### Info Screen Show/Hide ######
               Output("intro", "style"),
               Output("bird_name", "style"),
               Output("bird_picture", "style"),
               Output("bird_latin", "style"),
               Output("bird_group", "style"),
               Output("bird_blurb", "style"),
               Output("bird_dot_1", "style"),  # Surely there's an easier way to do this
               Output("bird_dot_2", "style"),  # If you have any suggestions let me know
               Output("bird_dot_3", "style"),
               Output("notes", "style"),
               Output("bird_notes", "style"),
               Output("editMarker", "style"),
               ###### Edit Screen Show/Hide ######
               Output("bird_name_input", "style"),
               Output("upload_bird", "style"),
               Output("bird_notes_input", "style"),
               Output("saveMarker", "style"),
               Output("deleteMarker", "style"),
               ###### Info Screen Info ######
               Output("bird_name", "children"),
               Output("bird_picture", "src"),
               Output("bird_latin", "children"),
               Output("bird_group", "children"),
               Output("bird_blurb", "children"),
               Output("bird_notes", "children"),
               Output('bird_name_input', 'value'),
               Output('bird_notes_input', 'value'),
               Output("upload_bird", "contents"),
               ],
              [Input("map", "click_lat_lng"),
               Input("saveMarker", "n_clicks"),
               Input('upload_bird', 'contents'),
               Input("editMarker", "n_clicks"),
               Input("deleteMarkerWrapper", "submit_n_clicks")],
              [State('bird_name_input', 'value'),
               State('upload_bird', 'filename'),
               State('upload_bird', 'contents'),
               State('bird_notes_input', 'value')
               ],
              )
def map_click(click_lat_lng, saveMarker_clicks, upload_bird_picture, editMarker_clicks, deleteMarker_nclicks,
              bird_name_input_value,
              upload_bird_filename, upload_bird_picture_contents, bird_notes_input_value):
    screen = 'info'

    # Initialize Info
    bird_name_children = ""
    bird_picture_children = ""
    bird_latin_children = ""
    bird_group_children = ""
    bird_blurb_children = ""
    bird_notes_children = ""
    bird_notes_input_value_output = bird_notes_input_value
    bird_name_input_value_output = bird_name_input_value

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
    setdata = "SELECT indexx from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
    curr.execute(setdata)
    marker_data = curr.fetchall()

    if marker_data == []:
        for marker in dl.LayerGroup(markers).children:  # but if it's not saved change it to red
            marker_index = str(marker.id['index'])
            if marker_index in clk_lat_lon_id(click_lat_lng):
                marker.icon = icon_red
                break

    # You can only add a point to the map if you assign data to it
    if selector == 'map.click_lat_lng':  # Add Temp Marker

        # Get # of saved entries
        curr = conn.cursor()
        setdata = "SELECT * from Markers"
        curr.execute(setdata)
        marker_num = curr.fetchall()

        if len(dl.LayerGroup(markers).children) > len(marker_num):  # if there's more markers on screen than saved ones
            dl.LayerGroup(markers).children.pop(-1)  # pop the most recent one (bc the user didn't save it)

        # check if there's already a saved marker at this lat/lon
        curr = conn.cursor()
        fetchData = "SELECT * from Markers WHERE indexx=\'" + str(clk_lat_lon_id(click_lat_lng)) + "\'"
        curr.execute(fetchData)
        marker_num = curr.fetchall()
        if marker_num:

            species = latin_and_common_from_code[marker_num[0][3]]

            bird_name_children = species[0]
            bird_picture_children = marker_num[0][4]
            bird_latin_children = species[1]
            bird_group_children = species[2]
            bird_blurb_children = "A short blurb about " + str(marker_num[0][3])
            bird_notes_children = marker_num[0][5]

        else:
            bird_name_children = ""
            bird_picture_children = ""
            bird_latin_children = ""
            bird_group_children = ""
            bird_blurb_children = ""
            bird_notes_children = ""
            bird_name_input_value_output = ""
            bird_notes_input_value_output = ""

            dl.LayerGroup(markers).children.append(dl.Marker(
                id={
                    'type': 'filter-dropdown',
                    'index': clk_lat_lon_id(click_lat_lng)
                }, position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)),
                bubblingMouseEvents=True, icon=icon_red
            ))
            screen = 'edit'
    elif selector == 'saveMarker.n_clicks':  # Save Marker To Database
        if bird_name_input_value != "":
            if upload_bird_picture_contents == None:
                upload_bird_picture_contents = no_image
            # Does marker exist?
            curr = conn.cursor()
            setdata = "SELECT indexx from Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
            curr.execute(setdata)
            marker_data = curr.fetchall()

            for marker in dl.LayerGroup(markers).children:  # then make the clicked one green
                marker_index = str(marker.id['index'])
                if marker_index in clk_lat_lon_id(click_lat_lng):
                    marker.icon = icon_green
                    break

            if marker_data == []:  # Entry Doesn't exist
                curr = conn.cursor()
                data = [[clk_lat_lon_id(click_lat_lng), click_lat_lng[0], click_lat_lng[1], bird_name_input_value,
                         upload_bird_picture_contents, bird_notes_input_value]]
                for i in data:
                    addData = f"""INSERT INTO Markers VALUES('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}', '{i[5]}')"""
                    print(addData)  # To see all the commands iterating
                    curr.execute(addData)
                conn.commit()

            else:  # Entry Exists, update data
                print("entry exists")
                curr = conn.cursor()
                setdata = "UPDATE Markers SET bird=\"" + bird_name_input_value + "\" WHERE indexx=\"" + \
                          str(clk_lat_lon_id(click_lat_lng)) + "\""
                curr.execute(setdata)
                if upload_bird_picture_contents is not None:
                    setdata = "UPDATE Markers SET img=\"" + upload_bird_picture_contents + "\" WHERE indexx=\"" + \
                              str(clk_lat_lon_id(click_lat_lng)) + "\""
                    curr.execute(setdata)
                setdata = "UPDATE Markers SET notes=\"" + bird_notes_input_value + "\" WHERE indexx=\"" + \
                          str(clk_lat_lon_id(click_lat_lng)) + "\""
                curr.execute(setdata)
                conn.commit()

            curr = conn.cursor()
            fetchData = "SELECT * from Markers WHERE indexx=\'" + str(clk_lat_lon_id(click_lat_lng)) + "\'"
            curr.execute(fetchData)
            marker_num = curr.fetchall()

            species = latin_and_common_from_code[marker_num[0][3]]

            bird_name_children = species[0]
            bird_picture_children = marker_num[0][4]
            bird_latin_children = species[1]
            bird_group_children = species[2]
            bird_blurb_children = "A short blurb about " + str(marker_num[0][3])
            bird_notes_children = marker_num[0][5]

            marker.children = dl.Tooltip(species[0])
            upload_bird_picture_contents = None

    elif selector == 'upload_bird.contents':  # Save Marker To Database
        screen = 'edit'
        bird_picture_children = upload_bird_picture

    elif selector == 'editMarker.n_clicks':
        screen = 'edit'

        for marker in dl.LayerGroup(markers).children:  # Find out which marker is green (the last selected one)
            # print(marker.icon['iconUrl'][-9:-4])
            if 'green' in marker.icon['iconUrl'][-9:-4]:
                curr_marker = marker
                break

        curr = conn.cursor()
        fetchData = "SELECT * from Markers WHERE indexx=\'" + curr_marker.id['index'] + "\'"
        curr.execute(fetchData)
        marker_num = curr.fetchall()
        if marker_num:
            bird_name_input_value_output = marker_num[0][3]
            bird_picture_children = marker_num[0][4]
            bird_notes_input_value_output = marker_num[0][5]
            if bird_notes_input_value_output == 'None':
                bird_notes_input_value_output = ""


    elif selector == 'deleteMarkerWrapper.submit_n_clicks':
        for marker in dl.LayerGroup(markers).children:
            marker_index = str(marker.id['index'])
            if marker_index in clk_lat_lon_id(click_lat_lng):
                dl.LayerGroup(markers).children.remove(marker)
                break

        curr = conn.cursor()
        setdata = "DELETE FROM Markers WHERE indexx=\"" + str(clk_lat_lon_id(click_lat_lng)) + "\""
        curr.execute(setdata)
        conn.commit()

        screen = 'intro'

    # TODO: Anything that modifies style further (reset text input, set colours has to go AFTER
    if screen == 'info':  # User is not editing a marker - Show Info

        ###### Info Screen ######
        intro_style = {"margin": "0 0", "font-size": "1.5rem", "display": "none", "text-align": "center"}
        bird_name_style = {"font-size": "1.5rem", "display": "block"}
        bird_picture_style = {"height": "25vh", "width": "100%", "padding": "0px 0px", "background-color": "#fff",
                              "border": "1px solid #D1D1D1", "border-radius": "4px", "box-shadow": "none",
                              "box-sizing": "border-box", "margin": "1rem 0", "fontFamily": "inherit",
                              "display": "block"}
        bird_latin_style = {"margin": "0 0", "font-size": "1.3rem", "display": "block", "width": "50%"}
        bird_group_style = {"margin": "0 0", "font-size": "1.3rem", "display": "block", "text-align": "right",
                            "width": "50%"}
        bird_blurb_style = {"margin": "0 0", "font-size": "1.5rem", "display": "block"}
        bird_dot_1_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "inline-block", "border": "1px solid #858796", "margin": "1rem 0"}
        bird_dot_2_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "inline-block", "border": "1px solid #858796", "margin": "1rem 0.5rem"}
        bird_dot_3_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "inline-block", "border": "1px solid #858796", "margin": "1rem 0"}
        notes_style = {"margin": "0 0", "font-size": "1.3rem", "display": "block"}
        bird_notes_style = {"font-size": "1.5rem", "display": "block", "height": "10vh"}
        editMarker_style = {"font-size": "1.5rem", 'display': 'block', "position": "absolute", "bottom": "0",
                            "left": "0"}
        ###### Edit Screen ######
        bird_name_input_style = {"font-size": "1.5rem", "display": "none"}
        upload_bird_style = {'width': '100%', 'height': '60px', 'display': 'none', 'lineHeight': '60px',
                             'borderWidth': '1px',
                             'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', "margin": "1rem 0",
                             "font-size": "1.5rem"}
        bird_notes_input_style = {"font-size": "1.5rem", "display": "none", "height": "10vh"}
        saveMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "3rem",
                            "left": "0", "margin": "1rem 0"}
        deleteMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "0",
                              "left": "0", }

    elif screen == 'edit':  # User is editing a marker
        ###### Info Screen ######
        intro_style = {"margin": "0 0", "font-size": "1.5rem", "display": "none", "text-align": "center"}
        bird_name_style = {"font-size": "1.5rem", "display": "none"}
        bird_picture_style = {"height": "25vh", "width": "100%", "padding": "0px 0px", "background-color": "#fff",
                              "border": "1px solid #D1D1D1", "border-radius": "4px", "box-shadow": "none",
                              "box-sizing": "border-box", "margin": "1rem 0", "fontFamily": "inherit",
                              "display": "block"}
        bird_latin_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none", "width": "50%"}
        bird_group_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none", "text-align": "right",
                            "width": "50%"}
        bird_blurb_style = {"margin": "0 0", "font-size": "1.5rem", "display": "none"}
        bird_dot_1_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0"}
        bird_dot_2_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0.5rem"}
        bird_dot_3_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0"}
        notes_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none"}
        bird_notes_style = {"font-size": "1.5rem", "display": "none", "height": "10vh"}
        editMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "0",
                            "left": "0"}
        ###### Edit Screen ######
        bird_name_input_style = {"font-size": "1.5rem", "display": "block"}
        upload_bird_style = {'width': '100%', 'height': '60px', 'display': 'block', 'lineHeight': '60px',
                             'borderWidth': '1px',
                             'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', "margin": "1rem 0",
                             "font-size": "1.5rem"}
        bird_notes_input_style = {"font-size": "1.5rem", "display": "block", "height": "10vh"}
        saveMarker_style = {"font-size": "1.5rem", 'display': 'block', "position": "absolute", "bottom": "3rem",
                            "left": "0", "margin": "1rem 0"}
        deleteMarker_style = {"font-size": "1.5rem", 'display': 'block', "position": "absolute", "bottom": "0",
                              "left": "0", }

    elif screen == 'intro':
        ###### Info Screen ######
        intro_style = {"margin": "0 0", "font-size": "1.5rem", "display": "block", "text-align": "center"}
        bird_name_style = {"font-size": "1.5rem", "display": "none"}
        bird_picture_style = {"height": "25vh", "width": "100%", "padding": "0px 0px", "background-color": "#fff",
                              "border": "1px solid #D1D1D1", "border-radius": "4px", "box-shadow": "none",
                              "box-sizing": "border-box", "margin": "1rem 0", "fontFamily": "inherit",
                              "display": "none"}
        bird_latin_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none", "width": "50%"}
        bird_group_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none", "text-align": "right",
                            "width": "50%"}
        bird_blurb_style = {"margin": "0 0", "font-size": "1.5rem", "display": "none"}
        bird_dot_1_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0"}
        bird_dot_2_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0.5rem"}
        bird_dot_3_style = {"height": "25px", "width": "25px", "background-color": "#bbbbbb", "border-radius": "50%",
                            "display": "none", "border": "1px solid #858796", "margin": "1rem 0"}
        notes_style = {"margin": "0 0", "font-size": "1.3rem", "display": "none"}
        bird_notes_style = {"font-size": "1.5rem", "display": "none", "height": "10vh"}
        editMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "0",
                            "left": "0"}
        ###### Edit Screen ######
        bird_name_input_style = {"font-size": "1.5rem", "display": "none"}
        upload_bird_style = {'width': '100%', 'height': '60px', 'display': 'none', 'lineHeight': '60px',
                             'borderWidth': '1px',
                             'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', "margin": "1rem 0",
                             "font-size": "1.5rem"}
        bird_notes_input_style = {"font-size": "1.5rem", "display": "none", "height": "10vh"}
        saveMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "3rem",
                            "left": "0", "margin": "1rem 0"}
        deleteMarker_style = {"font-size": "1.5rem", 'display': 'none', "position": "absolute", "bottom": "0",
                              "left": "0", }

    return dl.LayerGroup(
        markers), "", intro_style, bird_name_style, bird_picture_style, bird_latin_style, bird_group_style, bird_blurb_style, bird_dot_1_style, bird_dot_2_style, bird_dot_3_style, notes_style, bird_notes_style, editMarker_style, bird_name_input_style, upload_bird_style, bird_notes_input_style, saveMarker_style, deleteMarker_style, \
           bird_name_children, bird_picture_children, bird_latin_children, bird_group_children, bird_blurb_children, bird_notes_children, \
           bird_name_input_value_output, bird_notes_input_value_output, upload_bird_picture_contents


if __name__ == '__main__':
    app.run_server(debug=True)
