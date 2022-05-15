from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import DM, cache


# DataTable sortable avec tts les topics (20aine de lignes scrollable)
# Num, Nom, Avg and num main (values and/or ranks), Top 3-5 words,
def make_topic_table(n_words=5):

    data = [
        {
            #'topic': topic.replace('_', ' ').capitalize(),
            'name': topic_name,
            'words': '; '.join(str(w) for w in DM.TOPICWORDS_DF.loc[topic].nlargest(n_words).index),
            'avg': f'{DM.DOCTOPICS_DF[topic].mean():.4f}',
            'rank': f'({int(DM.DOCTOPICS_DF.mean().rank(ascending=False, method="min")[topic])}/{len(DM.TOPICWORDS_DF)})',
            'n_main': len(DM.TOPIC_REDUCTIONS['main_topic'][DM.TOPIC_REDUCTIONS['main_topic'] == topic]),
        } for topic, topic_name in DM.TOPIC_NAMES_MAP.items()]

    columns = [
        #{'name': 'Topic', 'id': 'topic'},
        {'name': 'Topic', 'id': 'name'},
        {'name': f'Top {n_words} words', 'id': 'words'},
        {'name': 'Avg topic weight (rank)', 'id': 'avg'},
        {'name': 'Avg topic weight (rank)', 'id': 'rank'},
        {'name': 'Docs with topic as main', 'id': 'n_main'},
    ]

    return dash_table.DataTable(data=data, columns=columns, sort_action='native', style_table={'overflow-y': 'scroll', 'max-height': '60vh', 'border': '1px solid black'}, merge_duplicate_headers=True)


topic_details_stats = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Select(
                options=[{'label': t.replace('_', ' ').capitalize() + ' - ' + n, 'value': t}
                         for t, n in DM.TOPIC_NAMES_MAP.items()],
                value=next(iter(DM.TOPIC_NAMES_MAP)),
                id='topic-details-select'
            ),
        ], lg=3),
        dbc.Col([

        ], lg=9),
    ]),

    dbc.Spinner([
        dbc.Row([

        dbc.Col([
            html.Div(id='topic-details-avg-weight'),
            html.Div(id='topic-details-n-main'),
            html.P('wordcloud?')
        ]),
        dbc.Col([
            html.Div(id='topic-details-top-words')
        ]),
        dbc.Col([
            html.Div(id='topic-details-top-sources-avg')
        ]),
        dbc.Col([
            html.Div(id='topic-details-top-sources-n-main')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Spinner(dcc.Graph(id='cshps-topics-words-graph', style={'width': '520px', 'height': '600px'}))
            ], className='graph-container'),
        ]),
        dbc.Col([
            html.Div([
                dbc.Spinner(dcc.Graph(id='cshps-topics-sources-graph', style={'width': '700px', 'height': '600px'}))
            ], className='graph-container'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.P('Références aux 10 articles les plus fortement associés à ce topic'),
            html.Div(id='topic-details-top-citations'),
        ])
    ])
    ])

])


cshps_topic_details_maindiv = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.Div('Topic Details', className='cshps-title'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            # Explanatory text
            dcc.Markdown(
                'Topic details. Overview on top, or select one below' +
                '\n\n' +
                'blablalba',
                className='cshps-md'
            ),
        ], lg=6),
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Markdown(
                'LDA topic model computed on abstracts using sklearn  \n' +
                f'Number of topics: {len(DM.TOPIC_NAMES_MAP)}  \n' +
                f'Average tokens: {int(DM.METADATA_CORPUSFRAME["abs_tokens"].mean())}  \n' +
                f'Vocabulary size: {len(DM.TOPICWORDS_DF.columns)} lemmas  \n',
                className='cshps-md'
            ),
            #html.P('Topic modeling réalisé sur les abstracts des textes'),
            #html.P(f'Nombre de tokens moyen: {int(DM.METADATA_CORPUSFRAME["abs_tokens"].mean())}'),
            #html.P(f'Taille totale du vocabulaire retenu: {len(DM.TOPICWORDS_DF.columns)} lemmes'),
            #html.P(f'Nombre de topics: {len(DM.TOPIC_NAMES_MAP)}'),
        ]),

        dbc.Col([
            make_topic_table()
        ], lg=9),
    ]),

    dbc.Row(dbc.Col(html.Hr())),

    dbc.Row([
        dbc.Col([
            topic_details_stats
        ]),
    ])

], body=True, className='content-card')


def make_topic_words_graph(topic='topic_0', n_topics=20):

    top_words = DM.TOPICWORDS_DF.loc[topic].nlargest(n_topics).sort_values(ascending=True)
    fig = px.bar(top_words, orientation='h', title=f'Top words ({n_topics} highest)')
    fig.update_layout(showlegend=False, margin_t=60, margin_b=30, margin_l=60, margin_r=30,
                      xaxis_title='Weights', yaxis_title='Words')
    #fig.update_xaxes(range=[0, 0.2]) # 0.28 max
    return fig


def make_topic_sources_graph(topic, n_sources=20):

    df = DM.METADATA_CORPUSFRAME.loc[:, ['source']]
    df[topic] = DM.DOCTOPICS_DF.loc[:, [topic]]
    srs_mean = df.groupby('source')[topic].mean().nlargest(n_sources).sort_values(ascending=True)
    fig = px.bar(srs_mean, orientation='h', title=f'Avg topic weight by journal ({n_sources} highest)')
    fig.update_layout(showlegend=False, margin_t=60, margin_b=30, margin_l=240, margin_r=30,
                      xaxis_title='Average Weights', yaxis_title='Journals')
    return fig


@callback([Output('topic-details-avg-weight', 'children'),
           Output('topic-details-n-main', 'children'),
           Output('topic-details-top-words', 'children'),
           Output('topic-details-top-sources-avg', 'children'),
           Output('topic-details-top-sources-n-main', 'children'),
           Output('topic-details-top-citations', 'children'),
           Output('cshps-topics-words-graph', 'figure'),
           Output('cshps-topics-sources-graph', 'figure')],
          [Input('topic-details-select', 'value')])
def update_topic_details(topic):
    top_words = DM.TOPICWORDS_DF.loc[topic].nlargest(10)

    average_weight = DM.DOCTOPICS_DF[topic].mean()
    rank = int(DM.DOCTOPICS_DF.mean().rank(ascending=False, method='min')[topic])
    n_main = len(DM.TOPIC_REDUCTIONS['main_topic'][DM.TOPIC_REDUCTIONS['main_topic'] == topic])

    # Sources with highest avg weight and topic as main
    df = DM.METADATA_CORPUSFRAME.loc[:, ['source']]
    df[topic] = DM.DOCTOPICS_DF.loc[:, [topic]]
    df['main_topic'] = DM.TOPIC_REDUCTIONS.loc[:, ['main_topic']]
    srs_mean = df.groupby('source')[topic].mean().nlargest(10)

    if n_main != 0:
        main_rank = int(DM.TOPIC_REDUCTIONS['main_topic'].value_counts().rank(ascending=False, method='min')[topic])
        srs_main = df[df['main_topic'] == topic]['source'].value_counts().nlargest(10)
    else:
        main_rank = 'N/A'
        srs_main = pd.Series(['N/A'], index=['N/A'])


    words_table = dash_table.DataTable(columns=[{'name': ['Mots les plus importants', 'Mot'], 'id': 'word'}, {'name': ['Mots les plus importants', 'Poids'], 'id': 'weight'}],
                                       data=[{'word': word, 'weight': f'{weight:.4f}'} for word, weight in top_words.iteritems()],
                                       merge_duplicate_headers=True,)

    srs_means_table = dash_table.DataTable(columns=[{'name': ['Revues par poids moyen', 'Revue'], 'id': 'source'}, {'name': ['Revues par poids moyen', 'Poids moyen'], 'id': 'avg'}],
                                          data=[{'source': source.capitalize(), 'avg': f'{avg:.4f}'} for source, avg in srs_mean.iteritems()],
                                          merge_duplicate_headers=True)

    srs_main_table = dash_table.DataTable(columns=[{'name': ['Topic principal par revues', 'Revue'], 'id': 'source'}, {'name': ['Revues avec topic comme principal', 'Nombre'], 'id': 'n'}],
                                          data=[{'source': source.capitalize(), 'n': n} for source, n in srs_main.iteritems()],
                                          merge_duplicate_headers=True)

    citations_table = dash_table.DataTable(columns=[{'name': 'Identifiant', 'id': 'id'}, {'name': 'Poids', 'id': 'weight'}, {'name': 'Citation', 'id': 'citation'}],
                                           data=[{'id': doc, 'weight': f'{w:.4f}', 'citation': DM.METADATA_CORPUSFRAME.loc[doc, 'citation']} for doc, w in DM.DOCTOPICS_DF[topic].nlargest(10).iteritems()],
                                           style_data={'whiteSpace': 'normal', 'height': 'auto'},)

    return html.P(f'Poids moyen à travers le corpus: {average_weight:.4f} ({rank}/80 plus important)'), \
           html.P(f'Topic principal de {n_main} documents ( {n_main/len(DM.METADATA_CORPUSFRAME)*100:.2f}% du corpus, {main_rank}/80 plus impoirtant)'), \
           words_table, \
           srs_means_table, \
           srs_main_table, \
           citations_table, \
           make_topic_words_graph(topic), \
           make_topic_sources_graph(topic)


