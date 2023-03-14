from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dashapp import DM, cache


meta_stats_div = html.Div([
    html.P(f'Top 10: {DM.METADATA_CORPUSFRAME["source"].value_counts().nlargest(10).sum()*100/len(DM.METADATA_CORPUSFRAME):.2f}%'),
    html.P(f'Top 20: {DM.METADATA_CORPUSFRAME["source"].value_counts().nlargest(20).sum()*100/len(DM.METADATA_CORPUSFRAME):.2f}%'),
    html.P(f'Top 25: {DM.METADATA_CORPUSFRAME["source"].value_counts().nlargest(25).sum()*100/len(DM.METADATA_CORPUSFRAME):.2f}%'),
    html.P(f'Top 29: {DM.METADATA_CORPUSFRAME["source"].value_counts().nlargest(29).sum()*100/len(DM.METADATA_CORPUSFRAME):.2f}%'),
    html.P(f'Top 100: {DM.METADATA_CORPUSFRAME["source"].value_counts().nlargest(100).sum()*100/len(DM.METADATA_CORPUSFRAME):.2f}%'),
])

extras_meta_maindiv = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Label('Choisir une metadonnee pour afficher toutes les valeurs'),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Select(
                options=[{'label': 'Source, catégories et topics', 'value': 'source'},
                         {'label': 'Catégories de revues et probabilités', 'value': 'category'},
                         {'label': 'Year', 'value': 'year'},
                         {'label': 'Doctype', 'value': 'doctype'},
                         {'label': 'Doctype Categories', 'value': 'doctype_cat'},],
                value='source',
                id='extras-meta-select',
                style={'max-width': '20rem'}
            )
        ], lg=3),
        dbc.Col([
            dbc.Button('Télécharger CSV', id='extras-meta-csv-btn'),
            dcc.Download(id='extras-meta-csv-dl')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Spinner(
                html.Div(id='extras-meta-table-container',
                         style={'width': 'fit-content', 'margin-top': '2rem', 'max-height': '80vh', 'overflow-y': 'scroll'})
            )
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(style={'margin': '2rem'}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
           meta_stats_div
        ]),
        dbc.Col([

        ]),
    ]),


    dbc.Row([
        dbc.Col([
            html.Hr(style={'margin': '2rem'}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Select(
                options=[
                    {'label': 'abs_tokens', 'value': 'abs_tokens'},
                    {'label': 'text_tokens', 'value': 'text_tokens'},
                    {'label': 'abs_words', 'value': 'abs_words'},
                    {'label': 'text_words', 'value': 'text_words'},
                ],
                value='abs_tokens',
                id='extras-meta-tokens-select',
            )
        ], lg=3),
        dbc.Col([
            dcc.Graph(id='extras-meta-tokens-graph'),
        ], lg=9)
    ])

])


def make_cat_probs_table():
    df = DM.SUBJECTS_CORPUSFRAME.div(DM.SUBJECTS_CORPUSFRAME.sum(axis=1), axis=0).mean().sort_values(ascending=False).reset_index()
    df.columns = ['Catégorie', 'Probabilité']
    return df


def make_journals_cats_topics_table():

    counts = DM.METADATA_CORPUSFRAME['source'].value_counts()
    data = [
        {'Source': s,
         'Nombre de Docs': counts[s],
         'Catégories BMC': '; '.join(c for c in DM.CATEGORIES_DICT[s]) if s in DM.CATEGORIES_DICT else '',
         'Topics principaux': '; '.join(DM.TOPIC_NAMES_MAP[t] for t in DM.DOCTOPICS_DF.loc[DM.METADATA_CORPUSFRAME['source']==s].mean().nlargest(3).index)}
        for s in counts.index]
    return pd.DataFrame.from_records(data)


def get_meta_df(m):

    if m == 'source':
        df = make_journals_cats_topics_table()
        name = 'sources_cats_topics'
    elif m == 'category':
        df = make_cat_probs_table()
        name = 'sources_cat_probs'
    else:
        df = DM.METADATA_CORPUSFRAME[m].value_counts().to_frame().reset_index()
        df.columns = [m, 'n docs']
        name = f'{m}_counts'
    return df, name


@callback(Output('extras-meta-table-container', 'children'),
          [Input('extras-meta-select', 'value')])
def update_extras_meta_table(m):

    df, _ = get_meta_df(m)
    return dbc.Table().from_dataframe(df, striped=True, bordered=True, hover=True, index=True, class_name='meta-table')


@callback(Output('extras-meta-csv-dl', 'data'),
          Input('extras-meta-csv-btn', 'n_clicks'),
          State('extras-meta-select', 'value'), prevent_initial_call=True)
def dl_meta_csv(n, m):

    df, name = get_meta_df(m)
    return dcc.send_data_frame(df.to_csv, f'{name}.csv')


@callback(Output('extras-meta-tokens-graph', 'figure'),
          Input('extras-meta-tokens-select', 'value'))
def make_corpus_wordcounts_graph(col):
    """

    mode: 'abstracts' for abstracts, else defaults to full texts
    """

    if 'abs' in col:
        bins = [140+30*i for i in range(11)]
    else:
        bins = [1900+500*i for i in range(11)]

    df = DM.METADATA_CORPUSFRAME.loc[:, (col, 'doctype_cat')]
    # Scale back very high values so they fit in the last bin
    # Ex. If bins are [0,100,200,300], all values >= 300 will be set to 299
    df[col] = df[col].map(lambda x: x if x < bins[-1] else bins[-1]-1)

    # Make bins, labels are '(bag[n])-(bag[n+1]-1)', except the last which is 'bag[-2]+'
    # Ex. If bins are [0,100,200,300], first label will be '0-99', last one '200+'
    df['bins'] = pd.cut(df[col], bins, labels=[f'{b}-{bins[i+1]-1}' if b != bins[-2] else f'{bins[-2]}+' for i, b in enumerate(bins[0:-1])])

    groups = ['bins']
    df = df.groupby(groups).size().reset_index(name='counts')

    return px.bar(df, x='bins', y='counts', text='counts',
                  title='Doc len graph',
                  labels={
                      'bins': 'Nombre de mots (tokens)',
                      'counts': 'Nombre de documents',
                    },
                  ).update_layout(showlegend=False)