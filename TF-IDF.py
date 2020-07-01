
import MeCab
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def getNVM(text):
    tokenizer = MeCab.Tagger()
    parsed = tokenizer.parse(text)
    word_tag = [w for w in parsed.split("\n")]
    pos = []
    tags = ['NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN']
    for word_ in word_tag[:-2]:
        word = word_.split("\t")
        tag = word[1].split(",")[0]
        if(tag in tags):
            pos.append(word[0])
    return pos

def main():
    docs = ['오늘은 비가 오기 전에 빨래를 거두어야 한다.',
            '비가 내리는 어느 날에는 네가 생각나.',
            '오늘 비가 내리지 않으면 소풍을 갈 수 있어']
    tf_vect = CountVectorizer(tokenizer=getNVM, preprocessor=None, lowercase=False)
    dtm = tf_vect.fit_transform(docs)
    print("tf:", tf_vect.get_feature_names())
    print(dtm)
    
    tfidf_vect = TfidfVectorizer(tokenizer=getNVM, preprocessor=None, lowercase=False)
    dtm = tfidf_vect.fit_transform(docs)
    print("tf-idf:", tfidf_vect.get_feature_names())
    print(dtm)

if __name__=="__main__":
    main()