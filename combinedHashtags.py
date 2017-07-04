import networkx as nx
import pandas
import itertools


hashtags = pandas.read_csv("hashtags.csv", sep=';', header = 0, encoding = "latin-1")
enthaelt = pandas.read_csv("enthaelt.csv", sep=';', header = 0, encoding = "latin-1")

tweetsContainingHashtags = list(enthaelt.tweet_ID.unique())
hashtagTweets = pandas.merge(enthaelt, hashtags, how="inner", on="hashtag_ID")


hashtagPairs = []

for tweet in tweetsContainingHashtags:
    df = hashtagTweets[hashtagTweets['tweet_ID'] == tweet]
    hashtagsPerTweet = df.hashtag_content.tolist()
    if(len(hashtagsPerTweet)>1):
        test = list(itertools.combinations(hashtagsPerTweet, 2))
        hashtagPairs += test

hashtagSets = [set(x) for x in hashtagPairs]

hashtagsUniqueEdges = []

for hashtagSet in hashtagSets:
    if hashtagSet not in hashtagsUniqueEdges:
        hashtagsUniqueEdges.append(hashtagSet)

edges = []
for hashtagEdge in hashtagsUniqueEdges:
    i = 0
    for occurence in hashtagSets:
        if hashtagEdge == occurence:
            i += 1
    entry = list(hashtagEdge)
    entry.append(i)
    entryTuple = tuple(entry)
    edges.append(entryTuple)
print(edges)

G=nx.Graph()
G.add_weighted_edges_from(edges)
nx.write_gexf(G, "hashtagNetwork.gexf")




