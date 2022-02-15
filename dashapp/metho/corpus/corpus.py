from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import DM

# Graph histo avec bins longueur textes/abstracts
# Tableau avec diferentes metadonnees


def make_corpus_wordcounts_graph(mode='abstracts', split_doctypes=False):
    """

    mode: 'abstracts' for abstracts, else defaults to full texts
    """

    if mode == 'abstracts':
        col = 'abs_tokens'
        bins = [140+30*i for i in range(11)]
    else:
        col = 'text_tokens'
        bins = [1900+500*i for i in range(11)]

    df = DM.METADATA_CORPUSFRAME.loc[:, (col, 'doctype_cat')]

    # Scale back very high values so they fit in the last bin
    # Ex. If bins are [0,100,200,300], all values >= 300 will be set to 299
    df[col] = df[col].map(lambda x: x if x < bins[-1] else bins[-1]-1)

    # Make bins, labels are '(bag[n])-(bag[n+1]-1)', except the last which is 'bag[-2]+'
    # Ex. If bins are [0,100,200,300], first label will be '0-99', last one '200+'
    df['bins'] = pd.cut(df[col], bins, labels=[f'{b}-{bins[i+1]-1}' if b != bins[-2] else f'{bins[-2]}+' for i, b in enumerate(bins[0:-1])])

    groups = ['bins', 'doctype_cat'] if split_doctypes else ['bins']
    df = df.groupby(groups).size().reset_index(name='counts')

    return px.bar(df, x='bins', y='counts', text='counts', color='doctype_cat' if split_doctypes else None,
                  title='Doc len graph',
                  labels={
                      'bins': 'Nombre de mots (tokens)',
                      'counts': 'Nombre de documents',
                    },
                  ).update_layout(showlegend=split_doctypes)


def make_pubdate_graph():

    d = DM.METADATA_CORPUSFRAME.loc[:, 'year'].value_counts().sort_index()
    return px.bar(d, text=d,
                  title='Documents par année de publication',
                  labels={
                      'value': 'Nombre de documents',
                      'index': 'Année de publication'
                  }).update_layout(showlegend=False)


def make_source_graph():

    df = DM.METADATA_CORPUSFRAME.loc[:, ('source', 'doctype')]
    d = df['source'].value_counts()

    return px.pie(d,
                  values='source',
                  names=d.index,
                  color=d.index,).update_layout(showlegend=False).update_traces(textinfo='none')


wordcounts_div = html.Div([

    dbc.Row([
        dbc.Col([
            html.P('Intro')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.P('blablabla'),
        ], lg=4),
        dbc.Col([
            dcc.Graph(id='metho-corpus-wordcounts-fig', figure=make_corpus_wordcounts_graph())
        ], lg=8),
    ]),

    dbc.Row([
        dbc.Col([
            # Texte
        ], lg=4),
        dbc.Col([
            dcc.Graph(id='metho-corpus-years-fig', figure=make_pubdate_graph())
        ], lg=8),
    ]),

    dbc.Row([
        dbc.Col([
            # Texte
        ], lg=4),
        dbc.Col([
            dcc.Graph(id='metho-corpus-source-fig', figure=make_source_graph())
        ], lg=8),
    ]),

])




