from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from sklearn.manifold import TSNE

from dashapp import DM, cache


modal_div = html.Div([
    dbc.Button('Voir le détail des champs', id='lexcorrs-details-btn'),
    dbc.Modal([
            dbc.ModalBody(
                dcc.Markdown('\n'.join(
                    f'1. **{lex}:** ' + ', '.join(w for w in words) for lex, words in DM.LEXICON_DICT.items() if lex != 'common'
                ))
            ),
        ],
        id='lexcorrs-details-modal',
        centered=True,
        is_open=False,
        scrollable=True,
    )
])

options_div = html.Div([
    dbc.Select(
        options=[{'label': 'Corpus complet', 'value': 'full'}] + [
            {'label': c.capitalize().replace('_', ' '), 'value': c} for c in sorted(DM.TOPIC_REDUCTIONS['cluster'].unique())
        ],
        value='cluster_0', # 'full'
        id='lexcorrs-cluster-select',
        style={'max-width': '12rem'}
    ),

    dbc.Button('Download Corrs CSV', id='lexcorrs-corrs-dl-btn'),
    dbc.Button('Download Freqs CSV', id='lexcorrs-freqs-dl-btn'),
])


lex_corrs_maindiv = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4('Lexique et corrélations'),
            html.P('Corrélations paragraphe-paragraphe sur l\'ensemble des textes.'),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            modal_div,
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            options_div,
            dcc.Download(id='lexcorrs-corrs-csv-dl'),
            dcc.Download(id='lexcorrs-freqs-csv-dl'),
        ]),
    ], style={'margin-top': '2rem', 'margin-bottom': '2rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Select(
                options=[{'label': w, 'value': w} for w in DM.LEX_OCCS_PARAS_DF.columns],
                value='mechanism',
                id='lexcorrs-comparison-select'
            ),
            html.Div(id='lexcorrs-comparison-table-div')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Spinner(
                dcc.Graph(id='lexcorrs-heatmap', style={'height': '900px', 'width': '100%'})
            ),  # 1350x1300, scroll
        ]),
    ]),
])


@callback(Output('lexcorrs-details-modal', 'is_open'),
          [Input('lexcorrs-details-btn', 'n_clicks')],
          [State('lexcorrs-details-modal', 'is_open')],)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open


def make_lexoccs_df(cluster: str) -> pd.DataFrame:

    if cluster != 'full':
        doc_ids = DM.TOPIC_REDUCTIONS.loc[DM.TOPIC_REDUCTIONS['cluster']==cluster].index
        df = DM.LEX_OCCS_PARAS_DF.loc[[i for i in DM.LEX_OCCS_PARAS_DF.index if i.split('_')[0] in doc_ids]]
    else:
        df = DM.LEX_OCCS_PARAS_DF

    return df


def make_corrs_df(cluster: str, norm_diag: bool = True) -> pd.DataFrame:

    df = make_lexoccs_df(cluster)
    df = df.corr()

    if norm_diag:
        df = df.applymap(lambda x: 0 if x == 1 else x)

    return df


def make_cprobs_df(cluster: str, max_value: int = 10) -> pd.DataFrame:

    df = make_lexoccs_df(cluster)
    df = (df >= 1)
    n_p = len(df)
    sums = df.sum()
    pf = pd.DataFrame(
        {c: [1 if v == c else df[df[v]][c].mean() / (sums[c] / n_p) for v in df.columns] for c in df.columns},
        index=sums.index
    )

    if max_value > 0:
        pf = pf.applymap(lambda x: max_value if x > max_value else x)

    return pf


def make_lexcorr_heatmap(df):

    #df = DM.LEXCORRS_PARAS_FULL_DF
    fig = px.imshow(df)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(showspikes=True, spikemode='toaxis', spikesnap='data', showline=False, spikedash='dot')
    fig.update_xaxes(showspikes=True, spikemode='toaxis', spikesnap='data', showline=False, spikedash='dot')
    return fig


def make_lex_scatter(df):
    df[['tsne_x', 'tsne_y']] = TSNE(n_components=2, random_state=2112).fit_transform(df)
    #df[['tsne_x', 'tsne_y', 'tsne_z']] = TSNE(n_components=3, random_state=2112).fit_transform(df)
    df['lex'] = df.index
    print(df)
    fig = px.scatter(df, x='tsne_x', y='tsne_y', color='lex', text='lex')
    #fig = px.scatter_3d(df, x='tsne_x', y='tsne_y', z='tsne_z', color='lex', text='lex')
    return fig



#print('This gonna be long...')
#corr_df = make_corrs_df('full', norm_diag=True)
#print('half done...')
#prob_df = make_cprobs_df('full', max_value=-1)
#print('done!')

@callback(Output('lexcorrs-heatmap', 'figure'),
          [Input('lexcorrs-cluster-select', 'value')])
def update_lex_heatmap(cluster):
    #df = corr_df
    df = make_corrs_df(cluster, norm_diag=True)
    #df = make_cprobs_df(cluster)
    #return make_lex_scatter(df)
    return make_lexcorr_heatmap(df)

"""
@callback(Output('lexcorrs-comparison-table-div', 'children'),
          [Input('lexcorrs-comparison-select', 'value')])
def update_top_comp(lex):
    rows = 20
    corr = corr_df[lex].nlargest(rows).index
    prob = prob_df[lex].nlargest(rows).index
    # print(corr.nlargest(20))
    # print(prob.nlargest(20))

    head = [html.Thead([html.Tr([html.Th('Rank'), html.Th('Corr'), html.Th('Prob')])])]
    body = [html.Tbody(
        [
        html.Tr([html.Td(i+1), html.Td(corr[i]), html.Td(prob[i])]) for i in range(rows)
        ]
    )]

    table = dbc.Table(head+body, bordered=True, striped=True, )

    return table
"""

@callback(Output('lexcorrs-corrs-csv-dl', 'data'),
          [Input('lexcorrs-corrs-dl-btn', 'n_clicks')],
          [State('lexcorrs-cluster-select', 'value')], prevent_initial_call=True)
def dl_lex_csv(n, cluster):
    df = make_lexoccs_df(cluster)
    df = df.corr().applymap(lambda x: 0 if x == 1 else x)
    return dcc.send_data_frame(df.to_csv, f'correlations_{cluster}.csv')


@callback(Output('lexcorrs-freqs-csv-dl', 'data'),
          [Input('lexcorrs-freqs-dl-btn', 'n_clicks')], prevent_initial_call=True)
def dl_occs_csv(n):
    counts = []
    counts.append(DM.LEX_OCCS_PARAS_DF.sum().div(len(DM.TOPIC_REDUCTIONS)).to_dict())
    index = ['corpus']
    for c in sorted(DM.TOPIC_REDUCTIONS['cluster'].unique()):
        doc_ids = DM.TOPIC_REDUCTIONS.loc[DM.TOPIC_REDUCTIONS['cluster'] == c].index
        df = DM.LEX_OCCS_PARAS_DF.loc[[i for i in DM.LEX_OCCS_PARAS_DF.index if i.split('_')[0] in doc_ids]]
        counts.append(df.sum().div(len(doc_ids)).to_dict())
        index.append(c)

    df = pd.DataFrame.from_records(counts, index=index).transpose()
    return dcc.send_data_frame(df.to_csv, f'frequences_champs.csv')
