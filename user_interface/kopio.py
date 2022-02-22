

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer 
import math
import numpy as np 
import requests 
import re
from bs4 import BeautifulSoup

url = "../data/enwiki-1000-corpus.txt"

content_list = []
name_list = []
list = []

document = open(url, "r")
corpus = document.read().replace('\n', ' ').replace('\\', '')
document.close()
soup = BeautifulSoup(corpus, "html.parser")
for article in soup.find_all('article'):
    content_list.append(article.contents.pop())
    name_list.append(article.get('name'))

for i,j in zip(name_list, content_list):
    list.append({"article": i, "content": j, "ranked value": ''})
#data = [x['content'] for x in list if 'content' in x]

#print(data[:1])
#print(list[0]['content'])

def search():
    matches = []
    query = 'division'


    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(content_list).T.tocsr()
    if query:
        query_vec = gv.transform([ query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
           # for entry in list:
            for x in range(len(list)):
                if content_list[doc_idx] in list[x]['content']:
                    list[x]['ranked value'] += str(score)
                    matches.append('{}'.format(list[x]))
    for i in range(len(matches)):
       print('match: {}, {}'.format(i+1, matches[i][:100]))
#        print(list[1:3])
#    print(len(matches))
#    print('{}\n{}'.format(list[1], list[2]))
"""
    # Output result
        print("Found {} matching documents.".format(len(ranked_scores_and_doc_ids)))
        if len(ranked_scores_and_doc_ids) > 0:
            num_matches = int(input("Please enter the maximum amount of matches to be displayed: "))
            print()
        print("These are the {} most relevant matches to your query '{:s}':".format(num_matches, query))
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            if i > (num_matches-1):
                break
            print("Match {:d}: (score: {:.4f}): {:s}".format(i+1, score, name_list[doc_idx]))
"""
search()
