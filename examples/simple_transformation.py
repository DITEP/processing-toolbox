import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from preprocessing.text2vec.transformers import HTMLParser, Text2Vector
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

sns.set()

# load data
path = 'data/reports.csv'
df = pd.read_csv(path, sep=';', encoding='utf-8') .head(5000)

# parse the reports
parser = HTMLParser(strategy='tokens')
X = parser.transform(df)



###################### vectorization using word2vec aggregation
text2vec = Text2Vector().fit(X)
x_w2v = text2vec.transform(X)

# plot the result using t-sne reduction
X_embedded = TSNE().fit_transform(x_w2v)
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], s=10)
plt.show()


###################### vectorization using TF-IDF

X_2 = HTMLParser(strategy='strings').transform(df['report'])

counter = CountVectorizer(ngram_range=(1, 5), lowercase=False,
                          max_df=0.9,
                          min_df=0.1)

tfidf = TfidfTransformer()

pipe = Pipeline([('counter', counter), ('transformer', tfidf)])

x_tfidf = pipe.fit_transform(X_2)

X_embedded = TSNE().fit_transform(x_tfidf.todense())
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], s=10)
plt.show()
