import dash
import dash_html_components as html
import sd_material_ui

app = dash.Dash(
    '',
    external_stylesheets=[
        'https://fonts.googleapis.com/icon?family=Material+Icons',
    ]
)

app.scripts.config.serve_locally = True

spacer = html.Div(children=[], style=dict(height=20, width=50))
final_spacer = html.Div(children=[], style=dict(height=400))

app.layout = html.Div([

    html.Div([
        spacer,
    ]),

    sd_material_ui.Subheader(['Sample Subheader']),

    sd_material_ui.Divider(),

    html.Div([
        spacer,
    ]),

    html.Div([
        html.Div([

            html.Div([
                    html.P([html.Strong('Sample for AutoComplete')]),
                    sd_material_ui.AutoComplete(
                        id='autocomplete',
                        dataSource=[{'label': 'Austin, TX', 'value': 'Austin'},
                                    {'label': 'Houston, TX', 'value': 'Houston'},
                                    {'label': 'New York, NY', 'value': 'New York'},
                                    {'label': 'Denver, CO', 'value': 'Denver'},
                                    {'label': 'Chicago, IL', 'value': 'Chicago'},
                                    {'label': 'Detroit, MI', 'value': 'Detroit'},
                                    {'label': 'Los Angeles, CA', 'value': 'Los Angeles'}],
                        dashCallbackDelay=3000
                    ),
                    html.P(id='autocomplete-output'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.P(id='autocomplete-search'),
                ]),

            spacer,

            html.Div([
                html.P([html.Strong('Test for dropdown menu')]),
                sd_material_ui.DropDownMenu(
                    id='dropdown-input',
                    labelText='Test',
                    labelId='dropdown-label',
                    value=1,
                    useGrouping=True,
                    options=[
                        dict(grouping='Group A'),
                        dict(primaryText='Option 1', value=1),
                        dict(primaryText='Option 2', value=2),
                        dict(grouping='Group B'),
                        dict(primaryText='Option 3', value=3),
                        dict(grouping='Group C'),
                        dict(primaryText='Option 4', value=4),
                    ]),

                html.P(id='dropdown-output'),
            ]),

            spacer,

            html.Div([
                html.P([html.Strong('Test for buttons')]),

                sd_material_ui.Button(
                    children=html.P('This is a Raised Button'),
                    id='button1',
                    disableShadow=False,
                    useIcon=False,
                    variant='contained'),

                spacer,

                sd_material_ui.Button(
                    children=html.P('This is a Flat Button'),
                    id='button2',
                    disableShadow=False,
                    useIcon=False,
                    variant='outlined',
                    classes={'root': 'SAMPLE_ROOT_CLASS',
                             'label': 'SAMPLE_LABEL_CLASS', }),

                spacer,

                sd_material_ui.Button(
                    children='Text Button',
                    id='button3',
                    variant='text', ),

                spacer,

                sd_material_ui.Button(
                    useIcon=True, id='button4', iconClass="glyphicon glyphicon-asterisk"),

                html.P(id='output-button')

            ]),

        ], style=dict(display='flex', flexWrap='wrap')),
    ]),
    ], style={'listStyleType': 'none'})


# Callback for SDDropdownMenu and SDMenuItem
@app.callback(
    dash.dependencies.Output('dropdown-output', 'children'),
    [dash.dependencies.Input('dropdown-input', 'value')])
def dropdown_callback(value):
    return ['Selection is: {}'.format(value)]


# Callback for SDAutoComplete
@app.callback(
    dash.dependencies.Output('autocomplete-search', 'children'),
    [dash.dependencies.Input('autocomplete', 'searchText')])
def autocomplete_callback(searchText: str):
    return ['Selection is (should take 3 seconds to show up) : {}'.format(searchText)]


# Callback for SDAutoComplete
@app.callback(
    dash.dependencies.Output('autocomplete-output', 'children'),
    [dash.dependencies.Input('autocomplete', 'selectedValue')])
def autocomplete_callback(searchValue: int):
    return ['Selection is {}'.format(searchValue if searchValue else '')]

# @app.server.route('/my-search', methods=['POST'])
# def black_box_search_engine():
#     search_term = flask.request.get_json().get('searchTerm')
#
#     assert isinstance(search_term, str)
#
#     return flask.jsonify({
#         'dataSource': [
#             {'label': search_term, 'value': 'val 1'},
#             {'label': 'val 2', 'value': {'a-dict-key': 'a value'}},
#             {'label': 'val 3', 'value': 'val 3'},
#             {'label': 'val 4', 'value': 'val 4'},
#         ]})


if __name__ == '__main__':
    app.run_server(debug=True)
