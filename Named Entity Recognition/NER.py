
#%%

# Data Download

from lovit_textmining_dataset import fetch

import os

os.chdir("/home/dohee/kaggle/textmining_dataset")
from lovit_textmining_dataset import version_check
version_check()
fetch()

#%%

from navermovie_comments import get_movie_comments_path

from collections import defaultdict

class Comments:
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for i, doc in enumerate(f):
                idx, text, rate = doc.split('\t')
                yield text.split()

#path = get_movie_comments_path(large=True, tokenize='soynlp_unsup')
path = '/home/dohee/kaggle/textmining_dataset/lovit_textmining_dataset/navermovie_comments/data/data_large_soynlp_unsup.txt'
comments = Comments(path)

def scan_vocabulary(sents, min_count, verbose=False):
    counter = defaultdict(int)
    for i, sent in enumerate(sents):
        if verbose and i % 100000 == 0:
            print('\rscanning vocabulary .. from %d sents' % i, end='')
        for word in sent:
            counter[word] += 1
    counter = {word:count for word, count in counter.items()
               if count >= min_count}
    idx_to_vocab = [vocab for vocab in sorted(counter,
                    key=lambda x:-counter[x])]
    vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
    idx_to_count = [counter[vocab] for vocab in idx_to_vocab]
    if verbose:
        print('\rscanning vocabulary was done. %d terms from %d sents' % (len(idx_to_vocab), i+1))
    return vocab_to_idx, idx_to_vocab, idx_to_count

vocab_to_idx, idx_to_vocab, idx_to_count = scan_vocabulary(
    comments, min_count=10, verbose=True)

print(idx_to_vocab[:5]) # ['영화', '이', '관람', '객', '의']
print(idx_to_count[:5]) # [1128809, 866305, 600351, 526070, 489950]
