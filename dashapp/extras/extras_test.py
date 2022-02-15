from dash import html, Input, Output, State, callback, MATCH, ALL, callback_context
import dash_bootstrap_components as dbc
import json

# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM


extras_test_maindiv = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.ListGroup(
                [dbc.ListGroupItem(html.H4('Titre'), class_name='list-group-select-title')] +
                [dbc.ListGroupItem(f'List item {n}', active=n==0, n_clicks=0, class_name='list-group-select-item',
                                   style={'cursor': 'pointer'}, id={'type': 'extras-test-list-item', 'index': n})
                 for n in range(10)]),
        ], width=3),
        dbc.Col([
            html.Div('Placeholder', id='extras-test-details', style={'border': '1px solid #eeeeee', 'height': '100%'}),
        ], width=6),
    ], ),#className='g-0'),

    dbc.Row([
        dbc.Col([
            html.P('Allo', n_clicks=0, id='test-p', className='testp'),
            html.P('Zero', id='test-pp',)
        ])
    ])
])


@callback([Output('extras-test-details', 'children'),
           Output({'type': 'extras-test-list-item', 'index': ALL}, 'active'),],
          Input({'type': 'extras-test-list-item', 'index': ALL}, 'n_clicks'))
def update_test_details(n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        button_id = 0
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id = json.loads(button_id)['index']
    a = [False for _ in n_clicks]
    a[button_id] = True
    return button_id, a


@callback(Output('test-pp', 'children'),
          [Input('test-p', 'n_clicks')])
def testp(n):
    return n

#@callback(Output({'type': 'extras-test-list-item', 'index': MATCH}, 'active'),
#          Input({'type': 'extras-test-list-item', 'index': MATCH}, 'n_clicks'), prevent_initial_call=True)
#def update_test_active(a):
#    return True
