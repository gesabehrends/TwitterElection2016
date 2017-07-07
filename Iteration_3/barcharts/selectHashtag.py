import pandas
import psycopg2
import sys
from datetime import *

hashtagWanted = sys.argv[1]
fileName = sys.argv[1] + ".csv"

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
abfrageListe = [datetime.fromtimestamp(date) for date in abfrageListe]
abfrageListe = [date.strftime('%Y-%m-%d') for date in abfrageListe]

uniqueDates = list(set(abfrageListe))
countDates = []
for scannedDate in uniqueDates:
    i = 0
    for date in abfrageListe:
        if date == scannedDate:
            i += 1
    countDates.append(i)

datesCumulated = pandas.DataFrame({'date': uniqueDates, 'count' : countDates})
datesCumulated.to_csv(fileName, sep=';', index=False)