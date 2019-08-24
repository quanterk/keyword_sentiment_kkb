from gensim.models import Word2Vec

model = Word2Vec.load("word2vec.model")
say = model.most_similar(u'说',topn=100)
print(say)
for i in say:
    print(model.most_similar(i[0], topn=10))