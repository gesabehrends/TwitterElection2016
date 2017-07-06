import pandas
import numpy
import psycopg2
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

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

#calculate average amount of likes and retweets per hashtag, write to dataframe
cur.execute("""SELECT  
    h.hashtag_content,
    h.hashtag_id AS hashtag_id, 
    sum(t.likes) AS likes_total, 
    avg(t.likes) AS likes_avg, 
    sum(t.retweets) AS retweets_total, 
    avg(t.retweets) AS retweets_avg, 
    count(t.tweet_id) AS hashtag_count
    FROM hashtags h 
        JOIN enthaelt e ON h.hashtag_id = e.hashtag_id
        JOIN tweets t ON e.tweet_id = t.tweet_id
    GROUP BY (h.hashtag_id)""")

hashtagData=pandas.DataFrame(cur.fetchall(),columns=[
    'hashtag_content',
    'hashtag_id',
    'likes_total',
    'likes_avg',
    'retweets_total',
    'retweets_avg',
    'hashtag_count'])

hashtagData.to_csv("hashtagData.csv", sep=';', index=False)

#only keep numerical data for cluster analysis, transform dataframe to array
hashtagCluster = hashtagData.drop(["hashtag_content", "hashtag_id", "likes_total", "retweets_total"], axis=1)
hashtagClusterArray = hashtagCluster.values


# Use KMeans from the machine Learning package scikit-learn, write found clusters to dataframe

km = KMeans(n_clusters=2, max_iter=1000)
km.fit(hashtagClusterArray)
labels = km.labels_
results = pandas.DataFrame([hashtagData.hashtag_id, hashtagData.hashtag_content, labels]).T
results.rename(columns = {'Unnamed 0':'cluster'}, inplace = True)

results.to_csv("resultKMeans.csv", sep=';', index=False)

#Combine hashtags with authors to later compare if hashtags cluster by author
cur.execute("""SELECT  
    t.autor,
    e.hashtag_id, 
    h.hashtag_content
    FROM hashtags h 
        JOIN enthaelt e ON h.hashtag_id = e.hashtag_id
        JOIN tweets t ON e.tweet_id = t.tweet_id
    GROUP BY (e.hashtag_id, t.autor, h.hashtag_content)""")

hashtagAutor=pandas.DataFrame(cur.fetchall(),columns=[
    'autor',
    'hashtag_id',
    'hashtag_content'])

cur.close()
conn.close()

hashtagClusterAutor = pandas.merge(results, hashtagAutor, how="inner", on="hashtag_id")
hashtagClusterAutor.to_csv("hashtagClusterAutor.csv", sep=';', index=False)


#Plot value combinations and clusters
plt.scatter(hashtagData.likes_avg, hashtagData.retweets_avg, alpha=.1, s=100)
plt.xlabel('Likes on average')
plt.ylabel('Retweets on average')
plt.savefig('likesRetweets.pdf')
plt.clf()

fig, ax = plt.subplots()
ax.scatter(hashtagData.likes_avg, hashtagData.retweets_avg, c=results.cluster, alpha=.3, s=30)
plt.savefig('likesRetweets.pdf')
plt.clf()

fig, ax = plt.subplots()
ax.scatter(hashtagData.hashtag_count, hashtagData.retweets_avg, c=results.cluster, alpha=.3, s=30)
plt.savefig('countRetweets.pdf')
plt.clf()

fig, ax = plt.subplots()
ax.scatter(hashtagData.hashtag_count, hashtagData.likes_avg, c=results.cluster, alpha=.3, s=30)
plt.savefig('countLikes.pdf')
plt.clf()
