#!/usr/bin/python

import re
#Files oeffnen (input zum lesen "r", output zum schreiben "w")
inputFile = open("american-election-tweets_02.csv", "r")
outputFileAll = open("tweetsPreliminary.csv", "w")
outputFileHashtags = open("hashtags.csv", "w")

#Maximale Anzahl Hashtags pro Tweet zaehlen, um passende neue Spalten
#anzulegen
numberHashtags = 0
for line in inputFile:
    if(line.count('#') > numberHashtags):
        numberHashtags = line.count('#')

addToHeader = ""      
for i in range(0, numberHashtags):
    addToHeader += ";hashtag_"+str(i)

#Read-File auf die erste Zeile setzen, alle Hashtags auslesen und in neuen
#Spalten anlegen
inputFile.seek(0)        
        
headerTweets = inputFile.readline()
headerTweets = headerTweets.rstrip("\n") + addToHeader
headerTweets = headerTweets +"\n"
outputFileAll.write(headerTweets)

allHashtags = []
for line in inputFile:
    listHashtags = re.findall(r"#(\w+)", line)
    allHashtags += listHashtags
    strHashtags = ""
    for hashtag in listHashtags:
        strHashtags += hashtag + ";"
    line = line.rstrip("\n") + ";" + strHashtags.rstrip(" ").rstrip(";") + "\n"
    outputFileAll.write(line)

#Herausfinden, welche unterschiedlichen Hashtags eingesetzt wurden
allHashtags = list(set(allHashtags))    

#Tabelle fuer Hashtags anlegen
headerHashtags = "hashtag_ID;hashtag_content\n"
outputFileHashtags.write(headerHashtags)
i = 0
    
for hashtag in allHashtags:
     i+=1
     line = str(i) + ";" + hashtag +"\n"
     outputFileHashtags.write(line)
    
    
print("Hashtags written to file, max " +str(numberHashtags)+ " hashtags per Tweet, "
+ str(i) +" unique Hashtags used")