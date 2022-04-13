from dash import html, Input, Output, State, callback, MATCH, ALL, callback_context, dcc
import dash_bootstrap_components as dbc
import json
import plotly.express as px

# If using DataManagers, import them from dashapp on this line as well
from dashapp import DM


def make_test_graph():
    d = DM.TOPICWORDS_DF.loc['topic_0'].nlargest(10)

    fig = px.bar(d, orientation='h', title=f'Top words')
    fig.update_layout(showlegend=False)
    return fig


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
    ]),

    dbc.Row([dbc.Col([html.Hr(style={'margin': '2rem'})])]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(figure=make_test_graph(), id='extras-test-graph', style={'height': '32rem', 'width': '32rem'}),
                dcc.Graph(id='extras-word-graph', style={'height': '32rem', 'width': '32rem'})
            ], style={'display': 'inline-block'}),
        ]),
    ]),
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


@callback(Output('extras-word-graph', 'figure'),
          Input('extras-test-graph', 'clickData'))
def make_word_graph(w):
    w = w['points'][0]['y']
    d = DM.TOPICWORDS_DF[w].nlargest(10)
    fig = px.bar(d, orientation='h', title=f'Top topics for {w}')
    fig.update_layout(showlegend=False)
    return fig