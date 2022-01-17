$page_name$_layout = dbc.Container([
    # First Row, full width
    dbc.Row([
       dbc.Col([
           # jumbotron
       ]),
    ]),

    # Second row with 2 cards
    dbc.Row([
        dbc.Col('card-1-children', lg=6),
        dbc.Col('card-2-children', lg=4),
    ]),
], id='$page_name$-layout', className='std-content-div', fluid=True)

$END$