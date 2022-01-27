# This is the code for the search engine task.

# Here we import the CountVectorizer module necessary for the engine.
from sklearn.feature_extraction.text import CountVectorizer

# Here we define the data set used in the search engine.
try:
    documents = ["This is a silly example",
                 "A better example",
                 "Nothing to see here",
                 "This is a great and long example"]
except FileNotFoundError:
    print("One or more of the input documents was not found.")

# Here we define some useful variables and create a matrix out of the data set.

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_

# Here we define the operators that can be used in queries.

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

# These functions parse the query entered by the user.

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query):
    return " ".join(rewrite_token(t) for t in query.split())

# Here we ask the user for a query, call the functions above and display the results.

print("Welcome to the Plague Engine!")
print("You can search our database by submitting a query in the input field below.")
print("To exit the program, enter an empty string when prompted.")
print()
query = str(input("Please type your query here: "))
while query != "":
    try:
        hits_matrix = eval(rewrite_query(query))
        hits_list = list(hits_matrix.nonzero()[1])
        print()
        print("Found {} matching documents:".format(len(hits_list)))
        print("Displayed below are the first ten matches.")
        for i, doc_idx in enumerate(hits_list):
            if i > 9: # only display the first ten documents
                break
            print("Match #{:d}: {:s}".format(i, documents[doc_idx]))
        print()

    except:
       print("No match found. Please enter another query.")
       print()

    query = str(input("Please type your query here: "))

print("No query entered. Program terminated.")
