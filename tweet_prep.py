#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 07:21:38 2020

@author: kevinreuning
"""

import pandas as pd 



df = pd.read_csv("all_data_fin.csv")
df = df.dropna(subset= ['City','State','Hazard.Desc.and.Location'])


df['Trimmed_Address'] = df.Address.str.extract("(.*?) [0-9|$]")
df.Trimmed_Address = df.Trimmed_Address.apply(lambda x: 
                                              " ".join(str(x).split(" ")[:4]))

df['Date'] = pd.to_datetime(df['Receipt.Date'])

df['Weight'] = (df.Date - min(df.Date)).dt.days + 1
df.Weight = df.Weight/sum(df.Weight)


df['Tweet'] = ('"' + df['Hazard.Desc.and.Location'] + '" - ' + 
               df.Trimmed_Address + " in " + df.City + ", " + 
               df.State + ' reported on ' + df.Date.dt.strftime('%b %d'))
df_out = df[['Tweet', 'Act.ID', 'Weight']]

df_out.columns = ['Tweet', 'ID', 'Weight']

df_out.to_csv('tweets.csv', index=False)

