CREATE TABLE "Tweets"
(
    "Tweet_ID" bigint NOT NULL,
    "Autor" "char"[] NOT NULL,
    "Datum" date NOT NULL,
    "Retweets" bigint NOT NULL,
    "Likes" bigint NOT NULL,
)
WITH ( OIDS = FALSE );

ALTER TABLE "Hashtags"
    ADD CONSTRAINT "tweets_pkey" PRIMARY KEY ("Tweet_ID"); 
    
CREATE TABLE "Hashtags"
(
    "Hashtag_ID" bigint NOT NULL,
    "Hashtag_content" "char"[] NOT NULL,
)
WITH (
    OIDS = FALSE
);

ALTER TABLE "Hashtags"
    ADD CONSTRAINT "hashtags_pkey" PRIMARY KEY ("Hashtag_ID");
    
CREATE TABLE "enthaelt"
(
    "Tweet_ID" bigint NOT NULL,
    "Hashtag_ID" bigint NOT NULL,

)
WITH (
    OIDS = FALSE
);

ALTER TABLE "enthaelt"
    ADD CONSTRAINT "enthaelt_pkey" PRIMARY KEY ("Tweet_ID", "Hashtag_ID") 
    ADD CONSTRAINT "hashtag_fkey" FOREIGN KEY ("Hashtag_ID") REFERENCES "Hashtags"("Hashtag_ID")
    ADD CONSTRAINT "tweet_fkey" FOREIGN KEY ("Tweet_ID") REFERENCES "Tweets"("Tweet_ID")
 
    
      
    