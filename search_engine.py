# this is the file for the Week 2 search engine task, write and work on the code here :)

from sklearn.feature_extraction.text import CountVectorizer

documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]

query = "NOT example OR great"

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query):
    return " ".join(rewrite_token(t) for t in query.split())

hits_matrix = eval(rewrite_query(query))
hits_list = list(hits_matrix.nonzero()[1])

for i, doc_idx in enumerate(hits_list):
    print("Matching doc \#{:d}: {:s}".format(i, documents[doc_idx]))
