# Imports useful modules
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import numpy as np
import requests
import re
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
        new_item = re.sub(r'</?\w>', r'', new_item)
        new_m = re.sub(r'(m\d{1,3}) .+', r'\1', new_item)
        new_c = re.sub(r'm\d{1,3} ([A-Z\s0-9\.]+) [A-Za-z.]+', r'\1', new_item)
        new_l = re.sub(r'm\d{1,3} ([A-Z\s]+) (.+)', r'\2', new_item)

        # this creates a list of with ONLY the lines (in a list!)
        if lines_stripped.get(new_m):
            lines_stripped[new_m].append(new_l)
        else:
            lines_stripped[new_m] = [new_l]

    # new structure -> movie number (m), movie name (), year (), genres(['x', 'y'])
    movies_list = []
    for item in titles:
        new_item = re.sub(r'[\+$]{7} ', '', item)
        t_nr = re.sub(r'(m\d{1,3}) .+', r'\1', new_item)
        t_name = re.sub(r'm\d{1,3} [\+$]{7} (.+) ', r'\1', item)
        t_year = re.sub(r'.+ [\+$]{7} ((19|20)\d{2})\/?I? .+', r'\1', t_name)
        t_name = re.sub(r'[\+$]{7} .+', '', t_name)
        t_genre = re.sub(r'.+ (\[)', r'\1', new_item)

        movies_list.append({'movie': t_nr, 'name': t_name, 'year': t_year, 'genres': t_genre, 'dialogue': '\" \"'.join(lines_stripped[t_nr]), 'score': ''})

    return movies_list

def matches_per_genre(search_query, matches):
    all_genres = []
    genres_listed = {}

    for movie in matches:
        assigned_genres = re.sub(r'[\[\]\'\s]', '', movie['genres'])

        for genre in assigned_genres.split(','):
            if genre not in all_genres:
                all_genres.append(genre)
                genres_listed[genre] = 0
            genres_listed[genre] += 1
    return genres_listed

def figure(matches, search_query):
    genres_listed = matches_per_genre(search_query, matches)

    labels = []
    for genre in genres_listed.keys():
        labels.append(genre)
    values = []
    for value in genres_listed.values():
        values.append(value)

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', pctdistance=1.15, labeldistance=1.35)
    ax1.axis('equal')

    fig1.savefig('static/pie_chart_{}.png'.format(search_query), transparent=True)
    return

# Assigns the search functions to an address composed of the base URL and "/search"
@app.route('/search')

def search():
    matches = []
    dialogue_list = []

    search_query = request.args.get('query')

    movies = prep() # returns our list of dictionaries

    for i in movies: # making a list containg only the dialogue of each movie
        dialogue_list.append(i['dialogue'])

    gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    g_matrix = gv.fit_transform(dialogue_list).T.tocsr()

    if search_query:
        new_matches = [] # creates a fully new matches list for each new search (-> we had some errors with old scores overlapping with new ones)
        matches = new_matches

        try:
            query_vec = gv.transform([ search_query ]).tocsc()
            hits = np.dot(query_vec, g_matrix)
            ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

            for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
                for x in range(len(movies)):

                    if dialogue_list[doc_idx] in movies[x]['dialogue']:
                        movies[x]['score'] += str(score) # appends the score to those movie entries that match the query

                        res = re.search(r'\b{}\b'.format(search_query).lower(), movies[x]['dialogue'].lower())
                        if res != None:
                            index = res.start()
                        else:
                            index = movies[x]['dialogue'].find(search_query)
                        if index != -1:
                            if index < 40:
                               movies[x]['dialogue'] = "...{}...".format(movies[x]['dialogue'][0: index + 80])
                               matches.append(movies[x])
                            else:
                               movies[x]['dialogue'] = "...{}...".format(movies[x]['dialogue'][index -40: index + 40])
                               matches.append(movies[x])
                    else:
                        continue

            figure(matches, search_query) # creates figure for each search

            # Renders the HTML file and imports the variable 'matches' and 'search_query'
            return render_template('plague.html', matches=matches, search_query=search_query)

        except: # Renders to HTML file for cases with no matches
            return render_template('bad_query.html', search_query=search_query)
    else:
        return render_template('plague.html', matches=matches, search_query=search_query)
