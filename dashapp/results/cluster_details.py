from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import DM, cache


def make_cluster_overview_table():
    # Name, num docs, top topics,

    columns = [{'name': 'Topic', 'id': 'cluster_name'},
               {'name': 'Nombre de documents', 'id': 'n_docs'},
               {'name': 'Topics principaux', 'id': 'top_topics'},]

    counts = DM.TOPIC_REDUCTIONS['cluster'].value_counts()
    data = [
        {'cluster_name': c.capitalize().replace('_', ' '),
         'n_docs': counts[c],
         'top_topics': ', '.join(DM.TOPIC_NAMES_MAP[t] for t in DM.DOCTOPICS_DF.loc[DM.TOPIC_REDUCTIONS['cluster']==c].mean().nlargest(3).index)}
            for c in sorted(DM.TOPIC_REDUCTIONS['cluster'].unique())]

    return dash_table.DataTable(columns=columns, data=data)

# Topic overview
# N docs, top 5 topics

# Top topics (average values) (side bars graph?)
# Tab Top journals, avg journal categories probs
# n docs


clusters_overview_div = html.Div([
    dbc.Row([
        dbc.Col([
            make_cluster_overview_table()
        ])
    ]),
])


cluster_breakdown_div = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Select(
                options=[
                    {'label': c.capitalize().replace('_', ' ') + f' ({len(DM.TOPIC_REDUCTIONS[DM.TOPIC_REDUCTIONS["cluster"]==c])} documents)',
                     'value': c}
                         for c in sorted(DM.TOPIC_REDUCTIONS['cluster'].unique())],
                value=sorted(DM.TOPIC_REDUCTIONS['cluster'].unique())[0],
                id='cluster-details-select'
            )
        ], lg=4),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='cluster-details-source-table', style={'margin-top': '2rem'}),
            dcc.Graph(id='cluster-details-subjects-pie', style={'height': '30rem', 'width': '30rem'}),
        ], lg=5),
        dbc.Col([
            dcc.Graph(id='cluster-details-topics-graph', style={'height': '40rem', 'width': '48rem'}),
            dcc.Graph(id='cluster-details-words-graph', style={'height': '40rem', 'width': '48rem'}),
        ], lg=5),
    ]),
])

cluster_details_maindiv = html.Div([

    dbc.Row([
        dbc.Col([
            html.H4('Détails des clusters')
        ]),
    ]),

    dbc.Row([

        dbc.Col([
            html.P('Explication'),
            dbc.Button('Télécharger CSV Cluster-Topics', id='cluster-details-topics-csv-btn'),
            dcc.Download(id='cluster-details-topics-csv-dl'),
            dbc.Button('Télécharger CSV Cluster-Categories', id='cluster-details-cats-csv-btn', style={'margin-top': '2rem'}),
            dcc.Download(id='cluster-details-cats-csv-dl')
        ], width=3),

        dbc.Col([
            clusters_overview_div,
        ], width=9),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr()
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            cluster_breakdown_div,
        ]),
    ]),

])


def make_cluster_topics_graph(cluster='cluster_0', n_topics=20):

    s = DM.DOCTOPICS_DF.loc[DM.TOPIC_REDUCTIONS['cluster']==cluster].mean().nlargest(n_topics).sort_values(ascending=True)
    s.index = s.index.map(DM.TOPIC_NAMES_MAP)
    fig = px.bar(s, orientation='h', title=f'Poids moyens des topics ({n_topics} plus importants)')
    fig.update_layout(showlegend=False)
    return fig


def make_cluster_words_graph(cluster='cluster_0', n_words=20):
    dt = DM.DOCTOPICS_DF.loc[DM.TOPIC_REDUCTIONS['cluster']==cluster].mean()
    s = DM.TOPICWORDS_DF.multiply(dt, axis='index').sum().nlargest(n_words).sort_values(ascending=True)
    fig = px.bar(s, orientation='h', title=f'Poids proportionnels moyens des mots ({n_words} plus importants)')
    fig.update_layout(showlegend=False)

    return fig


def make_cluster_subjects_pie(cluster='cluster_0', cutoff=0.01):

    df = DM.SUBJECTS_CORPUSFRAME.loc[DM.TOPIC_REDUCTIONS['cluster'] == cluster]
    df = df.div(df.sum(axis=1), axis=0).mean()
    df['Autres'] = df[df < cutoff].sum()
    df = df[df >= cutoff].sort_values(ascending=True)
    fig = px.pie(df, values=0, color=df.index, names=df.index, title='Probabilités des catégories de revues')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)

    return fig


def make_source_cluster_table(cluster, n=10):
    s = DM.METADATA_CORPUSFRAME.loc[DM.TOPIC_REDUCTIONS['cluster']==cluster]['source'].value_counts().nlargest(n)

    columns = [{'name': 'Revue', 'id': 'source'},
               {'name': 'Nombre de documents', 'id': 'n_docs'},]

    data = [{'source': s.capitalize(), 'n_docs': n} for s, n in s.iteritems()]

    return dash_table.DataTable(columns=columns, data=data)


@callback(
    [Output('cluster-details-subjects-pie', 'figure'),
     Output('cluster-details-topics-graph', 'figure'),
     Output('cluster-details-source-table', 'children'),
     Output('cluster-details-words-graph', 'figure')],
    [Input('cluster-details-select', 'value')]
)
def update_cluster_details(cluster):
    return make_cluster_subjects_pie(cluster), make_cluster_topics_graph(cluster), make_source_cluster_table(cluster), make_cluster_words_graph(cluster)


@callback(Output('cluster-details-topics-csv-dl', 'data'),
          Input('cluster-details-topics-csv-btn', 'n_clicks'), prevent_initial_call=True)
def download_cluster_topics_csv(n):
    df = DM.DOCTOPICS_DF.groupby(DM.TOPIC_REDUCTIONS['cluster']).mean()
    df.columns = df.columns.map(DM.TOPIC_NAMES_MAP)
    return dcc.send_data_frame(df.to_csv, 'cluster_topics.csv')


@callback(Output('cluster-details-cats-csv-dl', 'data'),
          Input('cluster-details-cats-csv-btn', 'n_clicks'), prevent_initial_call=True)
def download_cluster_topics_csv(n):
    df = DM.SUBJECTS_CORPUSFRAME.div(DM.SUBJECTS_CORPUSFRAME.sum(axis=1), axis=0).groupby(DM.TOPIC_REDUCTIONS['cluster']).mean()
    return dcc.send_data_frame(df.to_csv, 'cluster_categories.csv')