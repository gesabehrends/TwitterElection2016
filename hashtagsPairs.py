import psycopg2
import networkx as nx

try:
    conn = psycopg2.connect("""dbname='dbs' 
        user='testuser' 
        host='localhost' 
        password='testpass'""")
except psycopg2.Error as e:
    print(e.pgcode)
    print("Verbindung konnte nicht hergestellt werden.")
cur = conn.cursor()

cur.execute("""SELECT * FROM Student""")
#SQL statement, das ausgefuehrt werden soll

abfrageErgebnis = cur.fetchall()
#Die Abfrageergebnisse werden in der Variable "abfrageErgebnis" gespeichert

print("Tabellen in der Datenbank:")
for rows in abfrageErgebnis:
    print(rows)