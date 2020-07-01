
import joblib
import MeCab
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def getNVM_lemma(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    # nouns, verb, adjective, 긍정/부정 지정사
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN']#, 'MAG']
    for word_ in word_tag[:-2]:
        word = word_.split("\t")
        tag = word[1].split(",")
        if(len(word[0])<2):
            continue
        if(tag[-1] != "*"):
            t = tag[-1].split('/')
            if(len(t[0])>1 and ('VV' in t[1] or 'VA' in t[1] or 'VX' in t[1])):
                pos.append(t[0])
        else:
            if(tag[0] in tags):
                pos.append(word[0])
    return pos

def searchFiles(path):
    filelist = []
    filenames = os.listdir(path)
    for filename in filenames:
        file_path = os.path.join(path, filename)
        filelist.append(file_path)
    return filelist


#%%
"""
# LDA: try 1

tf_vect = TfidfVectorizer(tokenizer=getNVM_lemma, ngram_range=(1,1), min_df = 2, max_df = 20)
dtm = tf_vect.fit_transform(docs['내용'])
n_topics = 20
lda = LatentDirichletAllocation(n_components = n_topics)
lda.fit(dtm)

names = tf_vect.get_feature_names()
topics = dict()

for idx, topic in enumerate(lda.components_):
    vocab = []
    for i in topic.argsort()[:-(30-1):-1]:
        vocab.append((names[i], topic[i].round(2)))
    print("주제 %d:" % (idx + 1))
    print([(names[i], topic[i].round(2)) for i in topic.argsort()[:-(30-1):-1]])
"""

#%%

reviews = []

for filePath in searchFiles('/home/dohee/kaggle/topic-models/crawling/Reviews'):
    review = pd.read_csv(filePath, encoding = 'utf-8', engine='python')
    reviews.append(review)

# LDA: try 2
docs = pd.concat(reviews, ignore_index = True)
docs = docs[docs['평점']>3]
docs = docs.reset_index(drop=True)
docs['내용'] = docs.apply(lambda x: x['내용']*int(np.log2(2+x['공감수'])), axis=1)

#tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(1, 2), min_df = 2, max_df = 6000,
#                          max_features= 25000)

tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(1, 2), min_df = 2, max_df = 6000,
                          max_features= 25000)

dtm = tf_vect.fit_transform(docs['내용'])
n_topics = 18 # 18
lda = LatentDirichletAllocation(n_components=n_topics, topic_word_prior=0.01, doc_topic_prior=0.001)
lda.fit(dtm)
saved_model = joblib.dump(dtm, 'LDA.pkl')

names = tf_vect.get_feature_names()
topics_word = dict()
# 주제에 포함된 단어 갯수
n_words = 20 #20
# 주제에 속한 단어 topics_word에 저장
for idx, topic in enumerate(lda.components_):
    vocab = []
    for i in topic.argsort()[:-(n_words-1):-1]:
        vocab.append((names[i], topic[i].round(2)))
    topics_word[idx+1] = [(names[i], topic[i].round(2)) for i in topic.argsort()[:-(n_words-1):-1]]
    
# 주제당 가장 큰 비중을 차지하는 리뷰 출력
max_dict = dict()
for idx, vec in enumerate(lda.transform(dtm)):
    t = vec.argmax()
    if (t not in max_dict):
        max_dict[t] = (vec[t], idx)
    else:
        if max_dict[t][0] < vec[t]:
            max_dict[t] = (vec[t], idx)

sorted_review = sorted(max_dict.items(), key = lambda x: x[0], reverse = False)

docs = pd.concat(reviews, ignore_index = True)
docs = docs[docs['평점']>3]
docs = docs.reset_index(drop=True)

for key, value in sorted_review:
    print('주제 {}: {}'.format(key+1, topics_word[key+1]))
    print('[주제 {}의 대표 리뷰 :{}]\n{}\n\n'.format(key+1, value[0], docs['내용'][value[1]]))

print('[주제 {}의 대표 리뷰 :{}]\n{}\n\n'.format(key+1, value[0], docs['내용'][value[1]]))

#%%

# visualization

import pyLDAvis.sklearn

visual = pyLDAvis.sklearn.prepare(lda_model=lda, dtm=dtm, vectorizer = tf_vect)
pyLDAvis.save_html(visual, 'LDA_Visualization.html')
pyLDAvis.display(visual)
