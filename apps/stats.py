import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_leaflet as dl
import sqlite3
from data import bird_list, latin_and_common_from_code, no_image
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

from app import app

layout = \
    html.Div(id="wrapper", children=[

        html.Div(className="d-flex flex-column", id="content-wrapper", children=[
            html.Div(id="content", children=[

                #html.Nav(className="navbar navbar-dark navbar-expand accordian bg-gradient-primary shadow mb-0 topbar static-top", style={"font-size": "1.5rem"}, children=[
                #]),
                html.Div(className="container-fluid", children=[
                    html.Div(className="d-sm-flex justify-content-between align-items-center mb-4", children=[
                    ]),
                    html.Div(className="row", children=[
                        html.Div(className="col-lg-7 col-xl-8", style={"height": "91vh"}, children=[ #IF SCROLLBAR SHOWS UP EDIT THIS
                            html.Div(id="clickdata"),
                            html.Div(className="card shadow mb-4", children=[
                                html.Div(className="card-body", children=[
                                    html.Div(className="chart-area", style={"height": "66.6667vh"}, children=[

                                    ]),
                                ]),
                            ]),
                        ]),
                        html.Div(className="col-lg-5 col-xl-4", children=[
                            html.Div(className="card shadow mb-4", children=[
                                html.Div(className="card-body", children=[
                                    dcc.Loading(id="loading-1", type="default",children=[
                                            html.Div(className="chart-area", style={"height": "66.6667vh"}, children=[

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


@app.callback(
    Output('app-2-display-value', 'children'),
    Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)