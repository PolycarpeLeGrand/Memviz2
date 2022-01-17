# Example card with tabs
# Requires a callback to update content on click. Should have active_tab as input and CardBody-children as output.
$card_name$_card = dbc.Card([
    dbc.CardHeader([
        html.H3('This is a title above the card tabs'),
        dbc.Tabs([
                dbc.Tab(label='Tab 1', tab_id='$card_name$-tab-1'),
                dbc.Tab(label='Tab 2', tab_id='$card_name$-tab-2'),
            ],
            id='$card_name$-tabs',
            card=True,
            active_tab='$card_name$-tab-1',
            className='card-tabs',
        ),
    ], className='content-card-head'),
    dbc.CardBody([
        html.Div('Placeholder card content, add child components here', id='$card_name$-content-div'),
    ]),
], id='$card_name$-card', className='content-card')

@app.callback()
def card_callback():
    return