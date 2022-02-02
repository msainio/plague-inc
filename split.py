import re 

document = open("enwiki-corpus.txt", "r")
corpus = document.read().replace('\n', ' ')
document.close()

corpus_list = corpus.split("</article>")

#stripped_corpus = []
#for element in corpus_list:
#    stripped_corpus.append(element.strip())

#corpus_list = corpus.split("</article>")

print(corpus_list)
