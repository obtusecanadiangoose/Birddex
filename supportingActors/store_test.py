import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#############################################
########### variables & settings ############
#############################################

## app variabelen
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
len_data = 3500

#############################################
########### setup app-components ############
#############################################

## header met paginaselecties
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Login", href="/login"), id='nav_login'),
        dbc.NavItem(dbc.NavLink("Recode", href="/recode"), id='nav_recode'),
    ],
    brand="recode",
    brand_href="/",
    color="primary",
)

#############################################
############### layout pages ################
#############################################

## layout pagina 1
page_1 = html.Div([navbar,
                   html.Div([
                       html.Div([
                           dbc.FormGroup([dbc.Label("Name"),
                                          dbc.Input(id="name",
                                                    type="text",
                                                    placeholder="...")],
                                         className="m-3"),
                           html.Div(id='output_name')
                       ], style={'width': '40%'}),
                   ]),
                   ])

## layout pagina 2
page_2 = html.Div([navbar,
                   html.Div(id='name_output')
                   ])

#############################################
################ layout app #################
#############################################

app.layout = html.Div([
    dcc.Store(id='session',
              data=[{'name': 'Leeg'}]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


#############################################
############# callbacks routing #############
#############################################
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/login':
        return page_1
    elif pathname == '/recode':
        return page_2


@app.callback(Output('nav_login', 'active'),
              [Input('url', 'pathname')])
def set_page_1_active(pathname):
    return pathname == '/login'


@app.callback(Output('nav_recode', 'active'),
              [Input('url', 'pathname')])
def set_page_2_active(pathname):
    return pathname == '/recode'


#############################################
################# callbacks  ################
#############################################

@app.callback(
    Output('session', 'data'),
    [Input('name', 'value')])
def return_name(value):
    if value is None:
        raise PreventUpdate
    data = [{'name': value}]
    return data


@app.callback(
    Output('name_output', 'children'),
    [Input('session', 'data')])
def print_name(data):
    name = data[0]['name']
    return name


@app.callback(
    Output('slider_output', 'children'),
    [Input('slider_select', 'value')])
def update_slider(value):
    return "You've selected {} from total ({})".format(value, len_data)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)