
import re

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
    character_lines = []
    for item in lines:
        new_item = re.sub(r'[\+$]{7} ', '', item)
        new_item = re.sub(r'L\d{1,6} u\d{1,4} ', r'', new_item)
        new_m = re.sub(r'(m\d{1,3}) .+', r'\1', new_item)
        new_c = re.sub(r'm\d{1,3} ([A-Z]+(\.-)?(\s:[A-Z]{2,12})?) .+', r'\1', new_item)
        new_l = re.sub(r'm\d{1,3} ([A-Z\s:\.]+) (.+)', r'\2', new_item)


        # this creates a list of with ONLY the lines (in a list!)
        if lines_stripped.get(new_m):
            lines_stripped[new_m].append(new_l)
        else:
            lines_stripped[new_m] = [new_l]



#        if lines_stripped.get(new_c):
#            lines_stripped[new_c].append(new_l)
#        else:
#            lines_stripped[new_c] = [new_l]

#        if lines_stripped.get(new_m):
#            lines_stripped[new_m].append({'character': new_c, 'line': new_l})
#       else:
#            lines_stripped[new_m] = [new_l]


        #for i in lines_stripped:
        #    if i['character'] == new_c:
        #        character_lines
#    print(lines_stripped[0])

    print(lines_stripped[:50])


    # new structure -> movie number (m), movie name (), year (), genres(['x', 'y'])
    movies_list = []
    for item in titles:
        new_item = re.sub(r'[\+$]{7} ', '', item)
        t_nr = re.sub(r'(m\d{1,3}).+', r'\1', new_item)
        t_name = re.sub(r'm\d{1,3} [\+$]{7} (.+) ', r'\1', item)
        t_year = re.sub(r'.+ [\+$]{7} ((19|20)\d{2})\/?I? .+', r'\1', t_name)
        t_name = re.sub(r'[\+$]{7} .+', '', t_name)
        t_genre = re.sub(r'.+ (\[)', r'\1', new_item)

        movies_list.append({'movie': t_nr, 'name': t_name, 'year': t_year, 'genres': t_genre})

#    print(movies_list[1]['dialogue'])
#    movies = []
#    for i in movies_list:
#        movies.append((i['year'], i['name']))

#    print(movies[600:602])
#    for j in movies:
#        print(j)

prep()
