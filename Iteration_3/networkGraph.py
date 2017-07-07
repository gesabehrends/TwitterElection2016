import networkx as nx
import pandas
import itertools
import psycopg2

#connect to Election-database
try:
    conn = psycopg2.connect("""dbname='election' 
        user='postgres' 
        host='localhost' 
        password='rosalindFranklin'
        port='5432'""")
except psycopg2.Error as e:
    print(e.pgcode)
    print("Verbindung konnte nicht hergestellt werden.")
cur = conn.cursor()

#read Hashtags and Tweets in which they are used in from election-db
cur.execute("""SELECT  
    e.tweet_id,
    e.hashtag_id,
    h.hashtag_content
    FROM enthaelt e 
        JOIN hashtags h ON e.hashtag_id = h.hashtag_id""")

hashtagTweets=pandas.DataFrame(cur.fetchall(),columns=[
    'tweet_id',
    'hashtag_id',
    'hashtag_content'])
cur.close()
conn.close()

#List all different Tweets that contain a hashtag
tweetsContainingHashtags = list(hashtagTweets.tweet_id.unique())

#List all hashtags used in one tweet, list all 2-element combinations (edges!)
hashtagPairs = []

for tweet in tweetsContainingHashtags:
    df = hashtagTweets[hashtagTweets['tweet_id'] == tweet]
    hashtagsPerTweet = df.hashtag_content.tolist()
    if(len(hashtagsPerTweet)>1):
        test = list(itertools.combinations(hashtagsPerTweet, 2))
        hashtagPairs += test

hashtagSets = [set(x) for x in hashtagPairs]

#Find all different (unique!) edges
hashtagsUniqueEdges = []
for hashtagSet in hashtagSets:
    if hashtagSet not in hashtagsUniqueEdges:
        hashtagsUniqueEdges.append(hashtagSet)

#Calculate weight of edge (which we define as number of occurences)
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

#Put the found edges in a Graph that can be used by Gephi
G=nx.Graph()
G.add_weighted_edges_from(edges)
nx.write_gexf(G, "hashtagNetwork.gexf")




