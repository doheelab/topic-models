


# n-gram analysis    

import MeCab
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# plot configuration
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
plt.rc('font', family=font_name)
plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (12,8)

def searchFiles(path):
    filelist = []
    filenames = os.listdir(path)
    for filename in filenames:
        file_path = os.path.join(path, filename)
        filelist.append(file_path)
    return filelist

def getNVM_lemma(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MAG']
    # nouns, verb, adjective, 긍정/부정 지정사
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

reviews = []
for filePath in searchFiles('/data/kaggle/topic-models/crawling/Reviews'):
    review = pd.read_csv(filePath, encoding = 'utf-8', engine='python')
    reviews.append(review)
docs = pd.concat(reviews, ignore_index = True)

# positive
#docs = docs[docs['평점']==5]

# negative
docs = docs[docs['평점']==1]


#%%

import numpy as np

# uni-gram
tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(1,1), min_df = 2)

dtm = tf_vect.fit_transform(docs['내용']) # 문서-단어 행렬
vocab = dict()
for idx, word in enumerate(tf_vect.get_feature_names()):
    vocab[word] = dtm.getcol(idx).sum()
    

words = sorted(vocab.items(), key=lambda x:x[1], reverse = True)
max = 10

# Remove stopwords
StopWords = ['게임', '너무', '나오', '생각', '만들', '많이', '정말', '아니', '정도', '아직', '괜찮', '드리']
words = [item for item in words if item[0] not in StopWords][:max]

plt.bar(range(max), [i[1] for i in words[:max]])
plt.title('Frequency Top 20')
plt.xlabel('Word')
ax = plt.subplot()
ax.set_xticks(range(max))
ax.set_xticklabels([i[0] for i in words[:max]], rotation = 30)
plt.show()


#%%


word = '와이파이'
word_list = tf_vect.get_feature_names()
idx = word_list.index(word)

print("단어:", tf_vect.get_feature_names()[idx])
max_idx = np.argmax(dtm.getcol(idx).toarray())
print("반복횟수:", dtm.getcol(idx).toarray()[max_idx])
print("대표리뷰:", docs['내용'].iloc[max_idx])



#%%

# bi-gram

#tf_vect = CountVectorizer(tokenizer=getNVM_lemma, min_df = 2)
tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(2,2), min_df = 2)

dtm = tf_vect.fit_transform(docs['내용']) # 문서-단어 행렬
vocab = dict()
for idx, word in enumerate(tf_vect.get_feature_names()):
    vocab[word] = dtm.getcol(idx).sum()
words = sorted(vocab.items(), key=lambda x:x[1], reverse = True)
max = 20

# Remove stopwords
StopWords = ['즐기 게임', '나오 나오', '부탁 드리', '게임 게임', '게임 만들', '만들 게임', '게임 자체', '나오 게임', '과금 과금']
words = [item for item in words if item[0] not in StopWords][:max]

plt.bar(range(max), [i[1] for i in words[:max]])
plt.title('Frequency Top 20')
plt.xlabel('Word')
ax = plt.subplot()
ax.set_xticks(range(max))
ax.set_xticklabels([i[0] for i in words[:max]], rotation = 30)
plt.show()