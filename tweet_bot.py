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
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont



api = TwitterAPI(config.key,  
                 config.secret,  
                 config.access_token, 
                config.access_secret)


wrapper = textwrap.TextWrapper(width=50)
byte_io = BytesIO()

df = pd.read_csv("tweets.csv")
df_past = pd.read_csv("tweeted.csv")


while True:
    tweet_row = df.sample(1)
    
    if tweet_row.ID.values[0] not in df_past.ID.values:
        df_past = pd.concat([df_past.ID, tweet_row.ID])
        df_past.to_csv("tweeted.csv", index=False)
        break
        


message = tweet_row.Tweet.iloc[0]

if(len(message) > 250):
    message = "\n".join(wrapper.wrap(tweet_row.Tweet.iloc[0]))
    width = 1200
    height = 675
    img = Image.new('RGB', (width, height), color=(40, 60, 140))
    draw = ImageDraw.Draw(img)
    fontsize = 1  # starting font size
    img_fraction = .9
    font = ImageFont.truetype("LibreBaskerville-Bold.ttf", fontsize)
    
    
    while True:
        check_size = draw.multiline_textsize(message,   font=font)
        if check_size[0] > img_fraction*width or check_size[1] > img_fraction*height:
            break 
        else:
            fontsize += 1
            font = ImageFont.truetype("LibreBaskerville-Bold.ttf", 
                                      fontsize)
    
    
    text_size = draw.multiline_textsize(message,  font=font)
    draw.multiline_text(xy=((width - text_size[0])/2, 
                            (height - text_size[1])/2), text=message,  
                        align='center',font=font,   fill='white')
    
    font = ImageFont.truetype("LibreBaskerville-Bold.ttf", 
                              15)
    size = draw.textsize("Complaint Reported to OSHA\nSee: @WorkingWCovid", 
                         font=font)
    draw.multiline_text(xy=(width-size[0] - 5, 
                            height-size[1] - 5), 
                        text="Complaint Reported to OSHA\nSee: @WorkingWCovid",
                        align='right', font=font, 
                        fill='white')
    
    img.save("tmp.PNG",
             dpi=(300,300), optimize=True, 
             compress_level=4) # save it
    img.save(byte_io, "PNG",
             dpi=(300,300), optimize=True, 
             compress_level=4) # save it
    
    data = byte_io.getvalue()
    r = api.request('media/upload', None, {'media': data})
    
    status = tweet_row.Tweet.iloc[0]
    status = textwrap.shorten(status, width=200, placeholder='...')
    
    if r.status_code == 200:
        media_id = r.json()['media_id']
        
        # r = api.request('media/metadata/create', 
        #                 {'media_id':media_id,
        #                  "alt_text": {
        #                      "text": caption[0:999]} })
        r = api.request('statuses/update', 
                        {'status': status, 'media_ids': media_id})
else:

    r = api.request('statuses/update', 
                {'status': message})
        




