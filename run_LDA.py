import openpyxl
import pandas as pd
import pymongo
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import string
from nltk import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams
import re
import gensim
from gensim.models import CoherenceModel
from gensim import corpora
import tqdm
import pyLDAvis.gensim_models
import pickle
import pyLDAvis
import pyLDAvis.sklearn
from gensim.matutils import hellinger,kullback_leibler,jensen_shannon
from nltk.stem import WordNetLemmatizer
from itertools import chain
from collections import Counter

def compute_coherence_values(corpus, dictionary, k, a, b,texts):
    lda_model = gensim.models.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=k,
                                           passes=10,
                                           alpha=a,
                                           eta=b,
                                           per_word_topics=True,minimum_probability=0.0,random_state=100)

    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
    # from pprint import pprint  # Print the Keyword in the 10 topics
    # pprint(lda_model.print_topics())
    #
    # lda_visualization = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary, mds='mmds', sort_topics=False)
    # pyLDAvis.save_html(lda_visualization, 'lda_G06F870_10_Topics{}.html'.format(k))
    return coherence_model_lda.get_coherence()

def make_corpus(texts):
    dictionary = corpora.Dictionary(texts)
    bow_corpus = [dictionary.doc2bow(row) for row in texts]
    return dictionary,bow_corpus

title_df = pd.read_excel('titles.xlsx')
punc = string.punctuation
stopwords = stopwords.words('english')
stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()
title_df = title_df.apply(lambda x: x.astype(str).str.lower())
title_df['nolinks'] = title_df['title'].str.replace('http\S+|www.\S+', '', case=False)
title_df['cleaned'] = title_df['nolinks'].apply(lambda x: ''.join([i for i in x if i not in punc]))
title_df['tokenized'] = title_df.apply(lambda row: nltk.word_tokenize(row['cleaned']), axis=1)
title_df['no_stop'] = title_df['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])
title_df['stemmed'] = title_df['no_stop'].apply(lambda x: [stemmer.stem(y) for y in x])

dictionary,bow_corpus = make_corpus(title_df['stemmed'])

min_topics = 2
max_topics = 16
step_size = 1
topics_range = range(min_topics, max_topics, step_size)  # Alpha parameter
alpha = list(np.arange(0.01, 1, 0.3))
alpha.append('symmetric')
alpha.append('asymmetric')  # Beta parameter
beta = list(np.arange(0.01, 1, 0.3))
beta.append('symmetric')  # Validation sets
corpus_title = ['100% Corpus']
model_results = {'Validation_Set': [],
                 'Topics': [],
                 'Alpha': [],
                 'Beta': [],
                 'Coherence': []
                 }  # Can take a long time to run
pbar = tqdm.tqdm(total=270)
for k in topics_range:
    # iterate through alpha values
    for a in alpha:
        # iterate through beta values
        for b in beta:
            # get the coherence score for the given parameters
            cv = compute_coherence_values(corpus=bow_corpus, dictionary=dictionary,
                                          k=k, a=a, b=b,texts=title_df['stemmed'])
            # Save the model results
            try:
                model_results['Validation_Set'].append(corpus_title)
            except IndexError:
                model_results['Validation_Set'].append(corpus_title)
            model_results['Topics'].append(k)
            model_results['Alpha'].append(a)
            model_results['Beta'].append(b)
            model_results['Coherence'].append(cv)
            print(cv)
            pbar.update(1)
    pd.DataFrame(model_results).to_excel('lda_tuning_results_PCI_Titles.xlsx',index=False)
pbar.close()