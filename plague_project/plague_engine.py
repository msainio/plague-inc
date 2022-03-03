# Imports useful modules
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Initializes the Flask instance
app = Flask(__name__)

F_LINES = "data/movies/movie_lines.txt"
F_TITLES = "data/movies/movie_titles_metadata.txt"

# the structure of movie_lines.txt is: line (L), conversation (u), movie title (m), charachter (NAME), line (str)
fl = open(F_LINES, "r", encoding="ISO-8859-2")
lines = fl.read().splitlines()
fl.close()

# structure -> movie number (m), movie name (), year (), imbd-rating (\d), something???, genres(['x', 'y'])
ft = open(F_TITLES, "r", encoding="ISO-8859-2")
titles = ft.read().splitlines()
ft.close()

def prep():
# stripping unnecessary content into a file like: movie (m), charachter (NAME), line (str)
    lines_stripped = {}
    for item in lines:
        new_item = re.sub(r'[\+$]{7} ', '', item)
        new_item = re.sub(r'L\d{1,6} u\d{1,4} ', r'', new_item)
        new_m = re.sub(r'(m\d{1,3}) .+', r'\1', new_item)
        new_c = re.sub(r'm\d{1,3} ([A-Z\s0-9\.]+) [A-Za-z.]+', r'\1', new_item)
        new_l = re.sub(r'm\d{1,3} ([A-Z\s]+) (.+)', r'\2', new_item)

        # this creates a list of with ONLY the lines (in a list!)
        if lines_stripped.get(new_m):
            lines_stripped[new_m].append(new_l)
        else:
            lines_stripped[new_m] = [new_l]


        #if you want the characters and lines (in a dictionary) use this code!
        #if lines_stripped.get(new_m):
        #    lines_stripped[new_m].append({'character': new_c, 'line': new_l})
        #else:
        #    lines_stripped[new_m] = [new_l]


        #print(lines_stripped['m3'])


    # new structure -> movie number (m), movie name (), year (), genres(['x', 'y'])
    movies_list = []
    for item in titles:
        new_item = re.sub(r'[\+$]{7} ', '', item)
        t_nr = re.sub(r'(m\d{1,3}) .+', r'\1', new_item)
        t_name = re.sub(r'm\d{1,3} [\+$]{7} (.+) ', r'\1', item)
        t_year = re.sub(r'.+ [\+$]{7} ((19|20)\d{2})\/?I? .+', r'\1', t_name)
        t_name = re.sub(r'[\+$]{7} .+', '', t_name)
        t_genre = re.sub(r'.+ (\[)', r'\1', new_item)

        movies_list.append({'movie': t_nr, 'name': t_name, 'year': t_year, 'genres': t_genre, 'dialogue': ' '.join(lines_stripped[t_nr]), 'score': ''})

    return movies_list

# Assigns the search function to an address composed of the base URL and "/search"
@app.route('/search')

def search():
    matches = []
    scores = []
    dialogue_list = []

    search_query = request.args.get('query')
    movies = prep()

    for i in movies:
        dialogue_list.append(i['dialogue'])


    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(dialogue_list).T.tocsr()
    if search_query:
        new_matches = []
        matches = new_matches
        query_vec = gv.transform([ search_query ]).tocsc()
        hits = np.dot(query_vec, g_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            for x in range(len(movies)):
                if dialogue_list[doc_idx] in movies[x]['dialogue']:
                    movies[x]['score'] += str(score)
                    matches.append(movies[x])

        fig = plt.figure()
        for i in matches:
            scores.append(float(i['score']))
        if len(scores) > 20:
            scores = scores[:20]
        ranks = []
        for i in range(1,(len(scores)+1)):
            ranks.append(str(i))
        plt.bar(ranks, scores)
        fig.savefig('static/bar_graph.png', dpi=200)

# Renders the HTML file and imports the variable 'matches'
    return render_template('plague.html', matches=matches, search_query=search_query)
