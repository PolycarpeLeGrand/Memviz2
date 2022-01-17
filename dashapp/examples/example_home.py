from dash import html
import dash_bootstrap_components as dbc

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

page_name = 'example-home'

home_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H2('PhiDash Home'),
            ]),
        ], className='title-row'),
        dbc.Row([
            html.P('Card content', className='content-text'),
        ]),
        dbc.Row([

        ]),
    ])
],  className='content-card')


example_home_layout = dbc.Container([
    # First card row, two columns
    dbc.Row([
        dbc.Col([
            home_card,
        ], lg=10),
    ], justify='center'),
], id='example-home-layout', className='std-content-div', fluid=True)



