# Overview

As part of the Springboard Capstone project, data downloaded from resources like Kaggle and fast.ai and streaming data (from Twitter API using python) were analyzed.  
The intial idea of the project was run using AWS resources to benchmark the model

## Datasets 
The datasets used were uploaded to AWS S3:
Dataset  |Link | 
 :--- | :---:|
Streaming Twitter data(downloaded from script)|https://dataset20200101projectfiles.s3.us-east-2.amazonaws.com/capstone/input_data/tweets/tweets.zip
Amazon review full score dataset|https://dataset20200101projectfiles.s3.us-east-2.amazonaws.com/capstone/input_data/amazon_review_full_csv/amazon_review_full_csv.zip
Airline Tweet sentiment Analysis |https://dataset20200101projectfiles.s3.us-east-2.amazonaws.com/capstone/input_data/twitter_airline_sentiment/tweets_airline.zip
Twitter data for sentiment analysis|https://dataset20200101projectfiles.s3.us-east-2.amazonaws.com/capstone/input_data/twitter_sentiment140/twitter_sentiment.zip
Myers Briggs Personality analysis|https://dataset20200101projectfiles.s3.us-east-2.amazonaws.com/capstone/input_data/myers_briggs_personality_test/myers_briggs.zip


## Script to collect tweet data
The Capstone project being considered involves analyzing tweets for determining sentiment(positive, negetive and nuetral) and also to determine the personality type based on the Myers Briggs personality test.  
Data on which the sentiment prediction and personality prediction can be done on, was downloaded using the tweepy API.There were 10 json files created with 100,000 tweets each.
The tweets were not cleaned( no emoticons, hyperlinks were removed). The text and full text of the extended test of the tweet were stored as separate fields.
link to the script : https://github.com/agvar/main_projects/blob/master/capstone/scripts/twitter_stream_download_json.py

## Dataset Analysis
 The analysis done on the datasets is at : https://github.com/agvar/main_projects/blob/master/capstone/data_analysis/dataset_analysis.ipynb
 
 ## Model BenchMarking using AWS
 ![model benchmarking using AWS](https://github.com/agvar/main_projects/blob/master/capstone/images/capstone_project_baseline_aws.png)
 
The benchmark architecture consists of the following components:  
1 : Read tweets using tweepy as (Producer)  
2 : Store tweet data fields as json files on AWS S3(Producer    
3 : Push tweet data into Kinesis Data stream  (Producer)**  
4 : Read tweet data from  Kinesis Data stream(Consumer)  
5 : Call the Comprehend API to determine sentiment of the tweet text(Consumer)  
6 : Store the tweet data with the sentiment and different sentiment scores on S3 (Consumer)  

The links to the scripts are as follows  
Producer : https://github.com/agvar/main_projects/blob/master/capstone/scripts/twitter_stream_message_producer.py  
Consumer : https://github.com/agvar/main_projects/blob/master/capstone/scripts/twitter_stream_message_subscriber.py  

** Kinesis data stream was created using the AWS CLI:  
aws kinesis create-stream --stream-name tweet_stream  

aws kinesis describe-stream-summary --stream-name tweet_stream  
{
    "StreamDescriptionSummary": {  
        "StreamName": "tweet_stream",  
        "StreamARN": "arn:aws:kinesis:us-east-2:047180200363:stream/tweet_stream",  
        "StreamStatus": "ACTIVE",  
        "StreamModeDetails": {  
            "StreamMode": "ON_DEMAND"  
        },  
        "RetentionPeriodHours": 24,  
        "StreamCreationTimestamp": 1640483978.0,  
        "EnhancedMonitoring": [  
            {  
                "ShardLevelMetrics": []  
            }  
        ],  
        "EncryptionType": "NONE",  
        "OpenShardCount": 4,  
        "ConsumerCount": 0  
    }  
}  
