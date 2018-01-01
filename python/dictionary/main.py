import ijson
from urllib import urlopen
f = urlopen(
    'https://raw.githubusercontent.com/adambom/dictionary/master/graph.json')
objects = ijson.items(f, '')
dependency_graph = {}
word_addrs = {}
graph = objects.next()
print("Dict loaded")
for word in graph:
    dependency_graph[word] = set(graph[word])
    for _word in graph[word]:
        if word_addrs.__contains__(_word):
            word_addrs[_word].append(word)
        else:
            word_addrs[_word] = [word]


def constructWord(word):
    if word_addrs.__contains__(word):
        for _word in word_addrs[word]:
            if _word in word_addrs:
                if word in word_addrs[_word]:
                    print("circular dependency; breaking")
                    break
                if _word in dependency_graph:
                    dependency_graph[_word] = dependency_graph[_word].union(
                        dependency_graph[word])


def conAll():
    n = 0
    for word in dependency_graph:
        n += 1
        constructWord(word)
        if n % 100 == 0:
            print n, "..."
    print "Constructed ", n, "words"


running = True

while running:
    word = raw_input("Word: ")
    if dependency_graph.__contains__(word):
        print word, ": "
        for _word in dependency_graph[word]:
            print "    ", _word
    if word == ".exit":
        running = False
    if word == ".recon":
        conAll()
