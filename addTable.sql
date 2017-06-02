DROP TABLE "enthaelt";
DROP TABLE "tweets";
DROP TABLE "hashtags";


CREATE TABLE "tweets"
(    "tweet_ID" INTEGER NOT NULL,
    "autor" VARCHAR(50) NOT NULL,
    "datum" BIGINT NOT NULL,
    "retweets" INTEGER NOT NULL,
    "likes" INTEGER NOT NULL
)
WITH (OIDS = FALSE );

ALTER TABLE "tweets"
    ADD CONSTRAINT "tweets_pkey" PRIMARY KEY ("tweet_ID"); 
    
CREATE TABLE "hashtags"
(    "hashtag_ID" Integer NOT NULL,
    "hashtag_content" VARCHAR(50) NOT NULL
)
WITH (OIDS = FALSE);

ALTER TABLE "hashtags"
    ADD CONSTRAINT "hashtags_pkey" PRIMARY KEY ("hashtag_ID");
    
CREATE TABLE "enthaelt"
(   "tweet_ID" Integer NOT NULL,
    "hashtag_ID" Integer NOT NULL
)
WITH (OIDS = FALSE);

ALTER TABLE "enthaelt"
    ADD CONSTRAINT "enthaelt_pkey" PRIMARY KEY ("tweet_ID", "hashtag_ID"), 
    ADD CONSTRAINT "hashtag_fkey" FOREIGN KEY ("hashtag_ID") REFERENCES "hashtags" ("hashtag_ID"),
    ADD CONSTRAINT "tweet_fkey" FOREIGN KEY ("tweet_ID") REFERENCES "tweets" ("tweet_ID");
 
--angelegte Tabellen angucken
 select COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
       NUMERIC_PRECISION, DATETIME_PRECISION, 
       IS_NULLABLE 
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='enthaelt';
      
select COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
       NUMERIC_PRECISION, DATETIME_PRECISION, 
       IS_NULLABLE 
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='hashtags';     
      
select COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
       NUMERIC_PRECISION, DATETIME_PRECISION, 
       IS_NULLABLE 
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='tweets';      
