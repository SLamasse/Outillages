import os
import re
import nltk
import spacy

from pprint import pprint


# Gensim pour les topics models 
import gensim
import gensim.corpora as corpora
from gensim.models import ldamodel
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel


# stop liste
from nltk.corpus import stopwords
nlp = spacy.load("fr_core_news_lg")

fr_stop = set(nltk.corpus.stopwords.words('french'))


# visualisation 
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt

def lemmatize(text):        
    sent = []
    doc = nlp(text)
    for word in doc:
        sent.append(word.lemma_)
    return " ".join(sent)


def nettoyer(doc):
    '''
    On enlève stop_words  et ponctuation
    '''
    txt = []
    for token in doc :
        if token.text not in fr_stop and not token.is_punct:
            txt.append(token.lemma_.lower())
    return txt



path = "Text1"
listfile = os.listdir(path)

documents = []
for filename in listfile:
    data = open(path + "/" + filename, 'r', encoding="latin1").read()
    txt = re.sub(r'[\n\s]+',' ', data)
    txt = lemmatize(txt)
    doc = nlp(txt)
    pt = nettoyer(doc)
    documents.append(pt)




dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(text) for text in documents]



NUM = 2
lda_model = ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=20, random_state=100,update_every=1,chunksize=100,passes=10, alpha='auto', per_word_topics=True)

pprint(lda_model.print_topics())

# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=documents, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)


# Visualize the topics

print("--- Génération visu LDAvis")
res = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(res, "visu.html")

