from pathlib import Path
from dotenv import load_dotenv
from os import environ, walk
from data.datamanager import SavedData, DType

# Browser tab title
PROJECT_TITLE = 'Memviz'

# Title and subtitle to display on navbar
NAV_TITLE = 'Memviz'
NAV_SUBTITLE = 'Visualisation du corpus BioMed'


# Load project settings
PROJECT_PATH = Path(__file__).parent
load_dotenv(PROJECT_PATH / '.env')
IS_PROD = environ.get('IS_PROD') == 'True'
LOCAL_IP = environ.get('LOCAL_IP')
PORT = 33

# If the data is not stored in the project directory, specify the path in .env and that path instead
# BASE_STORAGE_PATH = Path(environ.get('LOCAL_STORAGE_PATH'))
BASE_STORAGE_PATH = PROJECT_PATH / 'data'
DATA_PATH = Path('C:/Users/Sanchez/Desktop/m4data/memviz')
# DATA_PATH = BASE_STORAGE_PATH
DF_PATH = DATA_PATH / 'dataframes'
P_PATH = DATA_PATH / 'pickles'
STATIC_PATH = DATA_PATH / 'static'

# Pickled Dataframes to be loaded in the DfManager on app init
# Keys will be added to the DfManager object as variables <DfManager>.<key>
# Values can be either a path to the df or a tuple consisting of the path and a string (markdown) describing the df
GENERATE_DF_DOC_FILE = True

# List of data objects to load in the DataManager
# Add a SavedData object to DATA for each one
# d_type param must be a DType
DATA = [
    # Dataframes
    SavedData(name='METADATA_CORPUSFRAME', path=DF_PATH / 'metadata_corpusframe.p', d_type=DType.DF, details='A dataframe holding metadata for each document of the corpus'),
    SavedData(name='SUBJECTS_CORPUSFRAME', path=DF_PATH / 'secondary_subjects_corpusframe.p', d_type=DType.DF, details='A docs x journal subjects dataframe with a binary col for ech subject'),
    SavedData(name='TOPIC_REDUCTIONS', path=DF_PATH / 'topic_reductions_corpusframe.p', d_type=DType.DF, details='A dataframe holding 2d and 3d topic profiles and cluster ids for each doc'),
    SavedData(name='DOCTOPICS_DF', path=DF_PATH / 'lda_doc_topics_df.p', d_type=DType.DF, details='LDA doc x topics weight matrix'),
    SavedData(name='TOPICWORDS_DF', path=DF_PATH / 'lda_topic_words_df.p', d_type=DType.DF, details='LDA topic x words weight matrix'),
    SavedData('LEXCORRS_PARAS_FULL_DF', DF_PATH / 'lexcorrs_paras_full_df.p', DType.DF, 'Pearson corrs between lex cats, full corpus paragraphs.'),
    SavedData('LEMMAS_NVA_WORDS_DF', DF_PATH / 'lemmas_nva_words_1000docs_df.p', DType.DF, 'Lemmas with pos and words, with nva pos found in at least 1000 docs'),
    SavedData('WORDS_POS_LEMMAS_DF', DF_PATH / 'words_pos_lemmas_1000docs_df.p', DType.DF, 'Words with n_occs, pos and lemmas, found in at least 1000 docs'),
    SavedData('TOPIC_NAMES_MAP', P_PATH / 'topic_names_mapping_dict.p', d_type=DType.PICKLE, details='Topic number to topic name mapping dict'),
    SavedData('LEXICON_DICT', P_PATH / 'lexicon_dict.p', DType.PICKLE, 'word:[word] lexicon dict'),
    SavedData('COOCS_TOP_DICT', P_PATH / 'coocs_top_dict.p', DType.PICKLE, 'Dict top 100 coocs for each lexicon word, for each cluster. {cluster: {word: {\'n_occs\': n_occs, \'coocs\': [(word, coocs),...]}}}'),
    SavedData('COOC_REFS_WORDS_LIST', P_PATH / 'cooc_refs_words_list.p', DType.PICKLE, 'List of unique words in cooc refs')
]

# Add all .md files in data/markdowns and its children to DATA as MD files, with name.upper() as names
# Can be commented out, has the same effect as manually adding the files to DATA
for p in walk(BASE_STORAGE_PATH / 'markdowns'):
    for f in p[-1]:
        if f.split('.')[1][-2:] == 'md':
            DATA.append(SavedData(name=f.split('.')[0].upper(), path=Path(p[0])/f, d_type=DType.MD))


# Cache config
# Specify if using cache, and which config to use for prod and test
# If using Redis, specify info in .env
# Redis config:
#   Make sure Redis package is installed (pip install redis)
#   CACHE_TYPE: RedisCache
#   CACHE_REDIS_HOST: redis server address (plain ip as str, no port)
#   CACHE_REDIS_PORT: redis server port, default is 6379
#   CACHE_REDIS_PASSWORD: redis server password
USE_CACHE = True
if USE_CACHE:
    if IS_PROD:
        CACHE_CONFIG = {
            'CACHE_TYPE': 'RedisCache',
            'CACHE_REDIS_HOST': environ.get('CACHE_REDIS_HOST'),
            'CACHE_DEFAULT_TIMEOUT': 0,
        }
    else:
        CACHE_CONFIG = {
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': 0,
        }
else:
    CACHE_CONFIG = None

