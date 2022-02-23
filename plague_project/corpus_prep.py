""" i wanna prepare the files appropriately for the task at hand """

import re

F_LINES = "../data/movies/movie_lines.txt"
F_TITLES = "../data/movies/movie_titles_metadata.txt"

# the structure of movie_lines.txt is: line (L), conversation (u), movie title (m), charachter (NAME), line (str)
fl = open(F_LINES, "r", encoding="ISO-8859-2")
lines = fl.read().splitlines()
fl.close()

# structure -> movie number (m), movie name (), year (), imbd-rating (\d), something???, genres(['x', 'y'])
ft = open(F_TITLES, "r", encoding="ISO-8859-2")
titles = ft.read().splitlines()
ft.close()

# stripping unnecessary content into a file like: movie (m), charachter (NAME), line (str)
lines_stripped = []
for item in lines:
    new_item = re.sub(r'[\+$]{7} ', '', item)
    new_m = re.sub(r'L\d{1,6} u\d{1,4} (m\d{1,3}) .+', r'\1', new_item)
    new_c = re.sub(r'L\d{1,6} u\d{1,4} m\d{1,3} (\w+) .+', r'\1', new_item)
    new_l = re.sub(r'L\d{1,6} u\d{1,4} m\d{1,3} \w+ (.+)', r'\1', new_item)
#    new_l = re.sub('\', '', new_l)

    lines_stripped.append({'movie': new_m, 'character': new_c, 'line': new_l})

#for j in lines_stripped[:10]:
#    print(j, '\n')

# new structure -> movie number (m), movie name (), year (), genres(['x', 'y'])
titles_stripped = []
for item in titles:
    new_item = re.sub(r'[\+$]{7} ', '', item)
    t_nr = re.sub(r'(m\d{1,3}).+', r'\1', new_item)
    t_name = re.sub(r'm\d{1,3} [\+$]{7} (.+) ', r'\1', item)
    t_year = re.sub(r'.+ [\+$]{7} (\d{4}) .+', r'\1', t_name)
    t_name = re.sub(r'[\+$]{7} .+', '', t_name)
    t_genre = re.sub(r'.+ (\[)', r'\1', new_item)

    titles_stripped.append({'movie': t_nr, 'name': t_name, 'year': t_year, 'genres': t_genre, 'dialogue': []})

#for i in titles_stripped[:10]:
#    print(i, '\n')
combined = []

for i in titles_stripped:
    for j in lines_stripped:
        if i['movie'] == j['movie']:
            break
#            i['dialogue'] += j['line']

print(titles_stripped[:1])

"""
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            for x in range(len(list)):
                if content_list[doc_idx] in list[x]['innehåll']:
                    list[x]['ranked value'] += str(score)
                    matches.append(list[x])
"""
