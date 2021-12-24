# Overview

As part of the Springboard Capstone project, data downloaded from resources like Kaggle and fast.ai and streaming data (from Twitter API using python) were analyzed.  

## Datasets 
The datasets used are as follows:
Dataset  |Link | 
 :--- | :---:|
Streaming Twitter data(downloaded from script)| |
Amazon review full score dataset||
Airline Tweet sentiment Analysis ||
Twitter data for sentiment analysis||
Myers Briggs Personality analysis||


The sentiment data collected from amazon reviews, twitter airline review was modified to add a new field for sentiment of 0( negetive), positive (4) or neutral(2).  

## Script to collect tweet data
The Capstone project being considered involves analyzing tweets for determining sentiment(positive, negetive and nuetral) and also to determine the personality type based on the Myers Briggs personality test.  
Data on which the sentiment prediction and personality prediction can be done on, was downloaded using the tweepy API.There were 10 json files created with 100,000 tweets each.
The tweets were not cleaned( no emoticons, hyperlinks were removed). The text and full text of the extended test of the tweet were stored as separate fields.
link to the script : https://github.com/agvar/main_projects/blob/master/capstone/scripts/twitter_stream_download_json.py

## Dataset Analysis
 The analysis done on the datasets is at : https://github.com/agvar/main_projects/blob/master/capstone/data_analysis/dataset_analysis.ipynb
 
 
