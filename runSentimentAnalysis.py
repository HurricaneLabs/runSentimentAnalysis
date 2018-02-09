from __future__ import print_function

import json
import urllib
import boto3
import os
from botocore.vendored import requests

#load up necessary boto3 clients
#we use s3 (to get the stuff) and comprehend to analyze it

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    
    #our trigger is the S3 create even so bucket and key will be populated from that.
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    

    
    #Retrieve environment variables...the whole thing goes kaput if there are no environment variables
    splServer = os.environ['splServer']
    splToken = os.environ['splToken']

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #grab the ticket post from the s3 response
        ticketBody = response['Body'].read()
        #run the ticket post through AWS Comprehend to get sentiment analysis
        sentiments = comprehend.detect_sentiment(Text=ticketBody, LanguageCode='en')
        #add the ticket number to the dict so we have a unique key in splunk
        sentiments['ticketNum'] = key
        #fling the data to Splunk HTTP Event Collector for further analysis
        r = requests.post(splServer, headers={"Authorization": "Splunk " + splToken}, json={"host":"lambda-runSentimentAnalysis","event":sentiments})
        return r.status_code
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
