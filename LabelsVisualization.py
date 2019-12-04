#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:52:36 2019

@author: Sophie
"""

import pandas as pd
import matplotlib.pyplot as plt

#we read the file with songs (and labels) in pickle format

SongsDF = pd.read_pickle("song_df.pkl")

SongsDF.insert(0, 'NumbRaws', range(1, (len(SongsDF))+1))

SongsDF["album_label"].head()
CountLabels = SongsDF.groupby('album_label')['NumbRaws'].nunique()
#print(CountLabels)

CountSongs = SongsDF.groupby('title')['NumbRaws'].nunique()
#print(CountSongs)
CountSpotID = SongsDF.groupby('spotify_id')['NumbRaws'].nunique()
#print(CountSpotID)
CountArtist= SongsDF.groupby('artist')['NumbRaws'].nunique()
#print(CountArtist)
SongsDF.sort_values("album_label", inplace = True) 

##we count how many times appear each label
SongsDF['CountLabels'] = SongsDF.groupby('album_label')['NumbRaws'].transform('count')

#list of all different labels  1250 different labels
SongsDF['album_label'].unique()
   
#we plot the 10 first labels
SongsDF['album_label'].value_counts()[:110].plot(kind='bar')
#plt.show()

NumberSmallLabels = len(SongsDF[SongsDF['CountLabels'] == 1]) + len(SongsDF[SongsDF['CountLabels'] == 2])