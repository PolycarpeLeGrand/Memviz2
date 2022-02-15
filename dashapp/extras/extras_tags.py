from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

from dashapp import DM, cache


def make_tag_table(df, t_id):
    return dash_table.DataTable(
        id=t_id,
        #data=DM.LEMMAS_NVA_WORDS_DF.to_dict('records'),
        columns= [{'name': '', 'id': 'index'}] + [
            {'name': c, 'id': c} for c in df.columns
        ],
        #fixed_rows={'headers': True},  # No fixed header because its laggy, waiting for a fix :(
        style_header={'minWidth': '100%'},
        style_cell={'minWidth': '5rem'},
        style_table={'overflowX': 'auto', 'border': '1px solid black'},
        #virtualization=True,
        page_action='custom',
        page_current=0,
        page_size=25,
        page_count=int(len(df)/25)+1
    )


extras_tags_lemmas_maindiv = html.Div([
    html.Div([
        html.Span('Lemmes présents dans au moins 1000 documents (textes complets) et appertenant aux catégories grammaticales noms, verbes ou adjectifs.'),
        html.Br(),
        html.Span(f'Total de {len(DM.LEMMAS_NVA_WORDS_DF)} lemmes (25 par page, utiliser les boutons sous le tableau pour naviguer)'),
        html.Br(),
        html.Span('total_counts: Nombre total d\'occurrences du lemme dans le corpus | presence_counts: Nombre de documents où le lemme est présent au moins une fois.'),
        html.Br(),
        html.Span('Adjectifs: [JJ, JJR, JJS] | Noms: [NN, NNS, NP, NPS] | Verbes: [VV, VVD, VVG, VVN, VVP, VVZ]'),
    ], style={'margin-bottom': '2rem'}),
    dbc.Spinner(make_tag_table(DM.LEMMAS_NVA_WORDS_DF, 'extras-lemmas-table'))
])

extras_tags_words_maindiv = html.Div([
    html.Div([
        html.Span('Mots présents dans au moins 1000 documents (textes complets).'),
        html.Br(),
        html.Span(f'Total de {len(DM.WORDS_POS_LEMMAS_DF)} mots (25 par page, utiliser les boutons sous le tableau pour naviguer)'),
        html.Br(),
        html.Span('total_counts: Nombre total d\'occurrences du lemme dans le corpus | presence_counts: Nombre de documents où le lemme est présent au moins une fois.'),
    ], style={'margin-bottom': '2rem'}),
    dbc.Spinner(make_tag_table(DM.WORDS_POS_LEMMAS_DF, 'extras-words-table'))
])


@callback(
    Output('extras-lemmas-table', 'data'),
    [Input('extras-lemmas-table', 'page_current'),
     Input('extras-lemmas-table', 'page_size')])
def update_lemmas_table(page_current, n):
    return DM.LEMMAS_NVA_WORDS_DF.reset_index().iloc[
        page_current*n:(page_current + 1)*n
    ].to_dict('records')


@callback(
    Output('extras-words-table', 'data'),
    [Input('extras-words-table', 'page_current'),
     Input('extras-words-table', 'page_size')])
def update_words_table(page_current, n):
    return DM.WORDS_POS_LEMMAS_DF.reset_index().iloc[
        page_current*n:(page_current + 1)*n
    ].to_dict('records')