import pandas
import psycopg2
import sys
from datetime import *

hashtagWanted = sys.argv[1]

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


cur.execute("""SELECT  
    t.datum
    FROM hashtags h 
        JOIN enthaelt e ON h.hashtag_id = e.hashtag_id
        JOIN tweets t ON e.tweet_id = t.tweet_id
    WHERE h.hashtag_content = %(some_id)s""", {'some_id': hashtagWanted})

abfrageErgebnis = cur.fetchall()

cur.close()
conn.close()

abfrageListe = [x[0] for x in abfrageErgebnis]

for date in abfrageListe:
    currently = datetime.fromtimestamp(date)
    print(currently)
    