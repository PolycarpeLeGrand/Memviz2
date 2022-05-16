from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

from dashapp import DM, cache
from . import CLUSTER_MAP


coocs_div = html.Div(id='coocs-top-content')

cshps_coocs_maindiv = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.Div('Cooccurrences', className='cshps-title'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            # Explanatory text
            dcc.Markdown(
                'Cooccurrence data was computed across the full-text content of every article (after lemmatization and word filtering), using and +/- 5 window. ' +
                'Selecting a word will display its 100 most frequent cooccurring term. ' +
                'The first column presents the results across the whole corpus, and the others each show the results for a specific clusters. ' +
                #'' +
                #'\n\n' +
                '',
                className='cshps-md'
            ),
        ], lg=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(className='cshps-hr-full'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div('Select a word to show cooccurrence details', className='cshps-subtitle', style={'margin': 'auto'}),
        ], width='auto', align='center'),
        dbc.Col([
            dbc.Select(
                options=[
                    {'label': w, 'value': w} for w in sorted(DM.COOCS_TOP_DICT['full_corpus'])
                ],
                value='mechanism',
                id='coocs-word-select',
                #style={'max-width': '20rem'}
            ),
        ], width='auto'),

    ], justify='start'),

    dbc.Row([
        dbc.Col([
            coocs_div
        ]),
    ], style={'margin-top': '1rem'}),

], body=True, className='content-card')


def make_cluster_tab(word):
    n_top = 100
    c_counts = DM.TOPIC_REDUCTIONS['cluster'].value_counts()
    c_counts['full_corpus'] = len(DM.TOPIC_REDUCTIONS)
    head = html.Thead(
        [
            html.Tr([html.Th('', rowSpan=4)] + [html.Th(f'{CLUSTER_MAP[cluster]} ({c_counts[cluster]} docs)', colSpan=3) for cluster in DM.COOCS_TOP_DICT]),
            html.Tr([html.Th(f'Occurrences: {DM.COOCS_TOP_DICT[cluster][word]["n_occs"]}', colSpan=3) for cluster in DM.COOCS_TOP_DICT]),
            html.Tr([html.Th(f'Avg occs per doc: {DM.COOCS_TOP_DICT[cluster][word]["n_occs"]/c_counts[cluster]:.2f}', colSpan=3) for cluster in DM.COOCS_TOP_DICT]),
            html.Tr([html.Th('Word'), html.Th('Coocs'), html.Th('pct')] * len(DM.COOCS_TOP_DICT)),
        ]
    )

    body = html.Tbody(
        [
            html.Tr([html.Td(i+1)] + [html.Td(v) for cluster in DM.COOCS_TOP_DICT
                     for v in [
                         DM.COOCS_TOP_DICT[cluster][word]['coocs'][i][0],
                         DM.COOCS_TOP_DICT[cluster][word]['coocs'][i][1],
                         f'{DM.COOCS_TOP_DICT[cluster][word]["coocs"][i][1]/DM.COOCS_TOP_DICT[cluster][word]["n_occs"]*100:.2f}%'
                     ]
                     ]
                    ) for i in range(n_top)
        ]
    )

    return dbc.Table([head, body], bordered=True, striped=True, hover=True, responsive=True, class_name='content-text-small')


def make_cluster_col(cluster, word):
    d = DM.COOCS_TOP_DICT[cluster][word]
    name = f'{cluster}(ndocs)'
    occs = f'Occurrences: {d["n_occs"]}'
    head = html.Thead(html.Tr([html.Th('Mot'), html.Th('Coocs'), html.Th('pct')]))
    body = html.Tbody(
        [
            html.Tr([html.Td(word), html.Td(coocs), html.Td(f'{coocs/d["n_occs"]:.2f}')]) for word, coocs in d['coocs']
        ])
    return html.H6(name), html.P(occs), dbc.Table([head, body], class_name='content-text-small')


@callback([Output('coocs-top-content', 'children'),],
          [Input('coocs-word-select', 'value')],)
@cache.memoize()
def update_coocs_content(word):
    return [make_cluster_tab(word)]
        #[dbc.Row(
        #[
        #    dbc.Col(make_cluster_col(cluster, word)) for cluster in DM.COOCS_TOP_DICT
        #]
    #)]

