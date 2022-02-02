
document = open("enwiki-corpus.txt", "r")
corpus = document.read().replace('\n', ' ')
document.close()

corpus_list = corpus.split("</article>")

print(corpus_list)
