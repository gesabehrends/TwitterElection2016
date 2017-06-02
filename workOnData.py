#!/usr/bin/python

import pandas
import datetime
import calendar
import psycopg2
import sqlalchemy as sq

#Daten aus den csv-files in pandas.dataframe einlesen
allDataTweets = pandas.read_csv("tweetsPreliminary.csv", sep=';', header = 0, encoding = "latin-1")
hashtags = pandas.read_csv("hashtags.csv", sep=';', header = 0, encoding = "latin-1")

#Fuer die Tweets-Auspraegung alle nicht benoetigten Attribute entfernen, Attribute umbennen,
#ID-Attribut hinzufuegen, Timestamp berechnen

allDataTweets = allDataTweets.drop(["text", "is_retweet", "original_author", "in_reply_to_screen_name",
 "is_quote_status", "source_url", "truncated"], axis=1)
allDataTweets = allDataTweets.rename(columns={"handle": "autor",
 "time":"datum", "retweet_count":"retweets", "favorite_count":"likes"})

allDataTweets.insert(0, "tweet_ID", range(1, len(allDataTweets)+1))  
tweets = allDataTweets
tweets = tweets.drop(["hashtag_0", "hashtag_1", "hashtag_2", "hashtag_3", "hashtag_4", 
"hashtag_5"], axis=1)

def calcUnixTimestamp(str):
    return calendar.timegm(datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%S").utctimetuple())

tweets["datum"] = tweets.apply(lambda x: calcUnixTimestamp(x["datum"]), axis=1)

#Enthaelt-Aupraegung aufstellen
enthaelt = allDataTweets
enthaelt = enthaelt.drop(["autor",	"datum", "retweets", "likes"], axis =1)

#Alle Hashtags in einer (langen Spalte verschmelzen)
enthaelt = pandas.melt(enthaelt, id_vars=["tweet_ID"])
enthaelt = enthaelt.rename(columns={"value": "hashtag_content"})

#die enthaelt-Tabelle mit der Hashtag-Tabelle verschmelzen, um die Schluessel zusammen-
#zubringen. (Inner join, da wir nur Tweet-IDs behalten wollen, in denen tatsaechlich
#Hashtags auftreten)

enthaelt = pandas.merge(enthaelt, hashtags, how="inner", on="hashtag_content")
enthaelt = enthaelt.drop(["variable","hashtag_content"], axis=1)
enthaelt = enthaelt.drop_duplicates(subset=['tweet_ID', 'hashtag_ID'], keep=False)

#Tabellen schreiben
enthaelt.to_csv("enthaelt.csv", sep=';', index=False)
tweets.to_csv("tweets.csv", sep=';', index=False)

#Tabelle in die postgresql-Datenbank hochladen
engine = sq.create_engine("postgresql+psycopg2://user:password@localhost:5432/election")
engine.connect()

hashtags.to_sql("hashtags", engine, if_exists='append', index=False)
tweets.to_sql("tweets", engine, if_exists='append', index=False, chunksize=10000)
enthaelt.to_sql("enthaelt", engine, if_exists='append', index=False)



