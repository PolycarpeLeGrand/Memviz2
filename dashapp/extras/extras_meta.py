from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

from dashapp import DM, cache


def make_cat_probs_table():
    df = DM.SUBJECTS_CORPUSFRAME.div(DM.SUBJECTS_CORPUSFRAME.sum(axis=1), axis=0).mean().sort_values(ascending=False).reset_index()
    df.columns = ['Catégorie', 'Probabilité']
    return dbc.Table.from_dataframe(df, bordered=True, striped=True, hover=True, index=True)


meta_table_div = html.Div([
    dbc.Label('Choisir une metadonnee pour afficher toutes les valeurs'),
    dbc.Select(
        options=[{'label': m, 'value': m} for m in ['year', 'source', 'doctype', 'doctype_cat']],
        value='source',
        id='extras-meta-select',
        style={'max-width': '15rem'}
    ),
    html.Div(id='extras-meta-table-container', style={'margin-top': '2rem', 'max-height': '80vh', 'overflow-y': 'scroll'})
])


extras_meta_maindiv = html.Div([
    dbc.Row([
        dbc.Col([
            meta_table_div,
        ], lg=4),

        dbc.Col([
            html.Div([
                make_cat_probs_table(),
            ], style={'margin-left': '4rem', 'margin-top': '6rem', 'max-height': '80vh', 'overflow-y': 'scroll'}),
        ], lg=4)

    ]),

    dbc.Row([
        dbc.Col([

        ]),
    ]),
])


@callback(Output('extras-meta-table-container', 'children'),
          [Input('extras-meta-select', 'value')])
def update_extras_meta_table(m):
    df = DM.METADATA_CORPUSFRAME[m].value_counts().to_frame().reset_index()
    df.columns = [m, 'n']
    return dbc.Table().from_dataframe(df, striped=True, bordered=True, hover=True, index=True, style={})