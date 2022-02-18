import sys
import os
import tweepy
from datetime import datetime
import json
import argparse
import boto3
from twitter_credentials  import API_key,API_secret_key,Access_token,Acess_token_secret


def save_tweet_s3(data_list):
    current_ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    s3_bucket = 'dataset20200101projectfiles'
    s3_file = s3.Object(s3_bucket, 'capstone/output_data/streaming/tweets_stream_' + current_ts + '.json')
    return_s3 = s3_file.put(Body=(bytes(json.dumps(data_list).encode('UTF-8'))))
    if return_s3['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to upload files to s3 bucket :{s3_bucket}")
        sys.exit(1)

def read_tweet_stream(kinesis_client,stream_name):

    sentiment_score_map={'POSITIVE':4,
                     'NEGATIVE':0,
                     'NEUTRAL':2
                     }
    try:
        response_shards = kinesis_client.list_shards(StreamName=stream_name)

    except Exception as e:
        print(f"Failed to get shards:{e}")

    for shard in response_shards['Shards']:
        try:
            response_shard_iterator=kinesis_client.get_shard_iterator(
                StreamName=stream_name,
                ShardId=shard['ShardId'],
                ShardIteratorType='TRIM_HORIZON'
                )
        except Exception as e:
            print(f"Failed to get shards:{e}")
        ShardId = shard['ShardId']
        ShardIterator=response_shard_iterator['ShardIterator']
        #print(f'shard id, shard iterator :{ShardId},{ShardIterator}')

        while ShardIterator:
            data_records=kinesis_client.get_records(ShardIterator=ShardIterator)
            if len(data_records['Records'])>0:
                tweet_list=[]
                for record in data_records['Records']:
                    tweets=json.loads(record['Data'])
                    for tweet in tweets:
                        if tweet['extended_tweet_text']:
                            tweet_text=tweet['extended_tweet_text']
                        else:
                            tweet_text = tweet['text']
                        sentiment_response=comprehend.detect_sentiment(Text=tweet_text, LanguageCode='en')
                        tweet['sentiment']=sentiment_response['Sentiment']
                        tweet['sentiment_score_overall'] = sentiment_score_map[sentiment_response['Sentiment']]
                        tweet['sentiment_score_positive'] = sentiment_response['SentimentScore']['Positive']
                        tweet['sentiment_score_negetive'] = sentiment_response['SentimentScore']['Negative']
                        tweet['sentiment_score_mixed'] = sentiment_response['SentimentScore']['Mixed']
                        tweet['sentiment_score_neutral'] = sentiment_response['SentimentScore']['Neutral']
                        tweet_list.append(tweet)
                        save_tweet_s3(tweet_list)

                ShardIterator=data_records['NextShardIterator']
            else:
                break



#main function
if __name__=='__main__':
    #creating kinesis client and s3 resource
    kinesis_client=boto3.client('kinesis',region_name='us-east-2')
    s3 = boto3.resource('s3')
    comprehend=boto3.client('comprehend',region_name='us-east-2')
    stream_name = 'tweet_stream'
    read_tweet_stream(kinesis_client,stream_name)





