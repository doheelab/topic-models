


# n-gram analysis    

import MeCab
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


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

reviews = []
for filePath in searchFiles('/home/dohee/kaggle/recommend/Playstore_Crawler/Reviews'):
    review = pd.read_csv(filePath, encoding = 'utf-8', engine='python')
    reviews.append(review)
docs = pd.concat(reviews, ignore_index = True)

# positive
#docs = docs[docs['평점']>3]

# negative
#docs = docs[docs['평점']<2]

tf_vect = CountVectorizer(tokenizer=getNVM_lemma, min_df = 2)
tf_vect = CountVectorizer(tokenizer=getNVM_lemma, ngram_range=(2,2), min_df = 2)

dtm = tf_vect.fit_transform(docs['내용']) # 문서-단어 행렬
vocab = dict()
for idx, word in enumerate(tf_vect.get_feature_names()):
    vocab[word] = dtm.getcol(idx).sum()
words = sorted(vocab.items(), key=lambda x:x[1], reverse = True)
max = 20
plt.bar(range(max), [i[1] for i in words[:max]])
plt.title('Frequency Top 20')
plt.xlabel('Word')
ax = plt.subplot()
ax.set_xticks(range(max))
ax.set_xticklabels([i[0] for i in words[:max]], rotation = 30)
plt.show()