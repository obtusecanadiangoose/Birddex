import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_leaflet as dl
import sqlite3
from data import bird_list, latin_and_common_from_code, no_image
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

from app import app
from apps import map, stats


nav_map = dbc.NavItem(dbc.NavLink("Map", id="map_link", href="/apps/map", style={"font-size": "1.8rem", "color":"rgba(248, 249, 252)"}, className="ms-4"))

nav_stats = dbc.NavItem(dbc.NavLink("Stats", id="stats_link", href="/apps/stats", style={"font-size": "1.8rem", "color":"rgba(255,255,255,.55)"}, className="ms-4"))
                                                                                    #color is grey (not selected) and does not have the text-light className

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("FAQ"),
        dbc.DropdownMenuItem("About"),
        dbc.DropdownMenuItem("Donate"),
        #dbc.DropdownMenuItem(divider=True),
        #dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Help",
    style={"font-size": "1.8rem"}, className="ms-4 text-light"
)
# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="../assets/img/logo_white.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Birddex", style={"font-size": "2rem"}, className="ms-2 text-light")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [nav_map, nav_stats, dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    style={"max-width":"inherit", "width":"100%"}),
    color="dark",
    dark=True,
    className="navbar navbar-dark",
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #dcc.Loading(html.Div(id='page-content'))
    logo,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Output('map_link', 'style'),
              Output('stats_link', 'style'),
              Input('url', 'pathname'))
def display_page(pathname):
    curr_page = {"font-size": "1.8rem", "color": "rgba(248, 249, 252)"}
    not_curr_page = {"font-size": "1.8rem", "color":"rgba(255,255,255,.55)"}


    if pathname == '/apps/map':
        return map.layout, curr_page, not_curr_page
    elif pathname == '/apps/stats':
        return stats.layout, not_curr_page, curr_page
    else:
        return map.layout, curr_page, not_curr_page

if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True)