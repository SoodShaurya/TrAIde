import nltk

with open("shit.txt", "w+") as file:
    file.write(" ".join([word for word in nltk.corpus.words.words()]))

file.close()