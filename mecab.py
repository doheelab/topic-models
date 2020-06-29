#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:10:46 2020

@author: dohee
"""

# Tokenization

import MeCab

def main():
    text = '아버지가방에들어가신다'
    tokenizer = MeCab.Tagger()
    print(tokenizer.parse(text))
    
if __name__=="__main__":
    main()
    
#%%
    
import MeCab

def getNVM(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VCP', 'VCN']
    for word_ in word_tag[:-2]:
        word = word_.split("\t")
        tag = word[1].split(",")[0]
        if (tag in tags):
            pos.append(word[0])
    return pos

def main():
    text = '아버지가방에들어가신다'
    print(getNVM(text))

if __name__ == "__main__":
    main()


word_tag = ['우리\tNP,*,F,우리,*,*,*,*', '는\tJX,*,T,는,*,*,*,*', '가까워질\tVA+EC+VX+ETM,*,T,가까워질,Inflect,VA,ETM,가깝/VA/*+어/EC/*+지/VX/*+ᆯ/ETM/*', '수\tNNB,*,F,수,*,*,*,*', '없\tVA,*,T,없,*,*,*,*', '기\tETN,*,F,기,*,*,*,*', '때문\tNNB,*,T,때문,*,*,*,*', '에\tJKB,*,F,에,*,*,*,*', '가깝\tVA,*,T,가깝,*,*,*,*', '게\tEC,*,F,게,*,*,*,*', '느껴\tVV+EC,*,F,느껴,Inflect,VV,EC,느끼/VV/*+어/EC/*', '지\tVX,*,F,지,*,*,*,*', '지\tEC,*,F,지,*,*,*,*', '않\tVX,*,T,않,*,*,*,*', '는다\tEC,*,F,는다,*,*,*,*', 'EOS', '']


#%%
    
# Lemmatization
import MeCab

def getNVM_lemma(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    # nouns, verb, adjective, 긍정/부정 지정사
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN']
    for word_ in word_tag[:-2]:
        word = word_.split("\t")
        tag = word[1].split(",")
        if(tag[0] in tags):
            pos.append(word[0])
        elif('+' in tag[0]): # multiple lemma
            if('VV' in tag[0] or 'VA' in tag[0] or 'VX' in tag[0]):
                t=tag[-1].split('/')[0]
                pos.append(t)
    return pos


def getNVM_lemma(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    # nouns, verb, adjective, 긍정/부정 지정사
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MAG']
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

def main():
    s = '아버지가방에들어가신다'
    s = '우리는 가까워질 수 없기 때문에 가깝게 느껴지지 않는다'
    print(getNVM(s))
    print(getNVM_lemma(s))
    
main()


#%%


reviews = []
for filePath in searchFiles('/home/dohee/kaggle/recommend/Playstore_Crawler/Reviews'):
    review = pd.read_csv(filePath, encoding = 'utf-8', engine='python')
    reviews.append(review)
docs = pd.concat(reviews, ignore_index = True)

# LDA: try 1

import numpy as np
from sklearn.decomposition import LatentDirichletAllocation

docs['내용'] = docs.apply(lambda x: x['내용']*int(np.log2(2+x['공감수'])), axis=1)
tf_vect = TfidfVectorizer(tokenizer=getNVM_lemma, ngram_range=(1,2), min_df = 2, max_df = 20)
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

#%%
    
# try 2

import joblib

tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(1, 2), min_df = 2, max_df = 6000,
                          max_features= 25000)
dtm = tf_vect.fit_transform(docs['내용'])
n_topics = 18
lda = LatentDirichletAllocation(n_components=n_topics, topic_word_prior=0.01, doc_topic_prior=0.001)
lda.fit(dtm)
saved_model = joblib.dump(dtm, 'LDA.pkl')

names = tf_vect.get_feature_names()
topics_word = dict()
# 주제에 포함된 단어 갯수
n_words = 20
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
    
for key, value in sorted_review:
    print('주제 {}: {}'.format(key+1, topics_word[key+1]))
    print('[주제 {}의 대표 리뷰 :{}]\n{}\n\n'.format(key+1, value[0], docs['내용'][value[1]]))



#%%

# visualization

import pyLDAvis.sklearn

visual = pyLDAvis.sklearn.prepare(lda_model=lda, dtm=dtm, vectorizer = tf_vect)
pyLDAvis.save_html(visual, 'LDA_Visualization.html')
pyLDAvis.display(visual)
    
    