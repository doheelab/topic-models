from konlpy.tag import Kkma, Twitter

import codecs


Kkma().pos("오버워치")
Twitter().pos("오버워치")

tagger = Twitter()
corpus = codecs.open('corpus.txt', 'w', encoding='utf-8')

def flat(content):
    return ["{}/{}".format(word, tag) for word, tag in tagger.pos(content)]

corpus.write(' '.join(flat("메이드복 입은 제이미 귀엽다")) + '\n')
