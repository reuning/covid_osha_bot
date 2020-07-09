#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:10:58 2020

@author: kevinreuning
"""

import pandas as pd 
import textwrap 
from TwitterAPI import TwitterAPI
import config 
import time


api = TwitterAPI(config.key,  
                 config.secret,  
                 config.access_token, 
                config.access_secret)


wrapper = textwrap.TextWrapper(width=255)

df = pd.read_csv("tweets.csv")
df_past = pd.read_csv("tweeted.csv")

while True:
    tweet_row = df.sample(1)
    
    if tweet_row.ID.values[0] not in df_past.ID.values:
        df_past = pd.concat([df_past.ID, tweet_row.ID])
        df_past.to_csv("tweeted.csv", index=False)
        break
        

message = wrapper.wrap(tweet_row.Tweet.iloc[0])

if len(message) > 1:
    for ii in range(len(message[:-1])):
        message[ii] = (message[ii] + "..." + str(ii+1) +  "/" 
                       + str(len(message)))
    

tweet_id = 0
for tweet in message:
    if tweet_id ==0:
        r = api.request('statuses/update', {'status': tweet})
    else:
        tweet = "@workingwcovid " + tweet
        r = api.request('statuses/update', {'status': tweet, 
                                            'in_reply_to_status_id':tweet_id})
        
    tweet_id = r.json()['id']
    time.sleep(1)



