# Final Project Report - IND ENG 242 - Predicting a Song Performance in the Billboard
#### *Ilias Miraoui, Youssef Lazrak, Owen Liu, Sophie Pealat, Jacques-Olivier Weulassagou*


_**[Introduction](#introduction)**_
_**[I - Data Processing](#data-processing)**_
&nbsp;&nbsp;&nbsp;&nbsp;_**[Data Sources](#data-sources)**_
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**[Billboard](#billboard)**_
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**[Spotify](#spotify)**_
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**[The Recording Industry Association of America (RIAA)](#riaa)**_
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**[Google Trends](#trends)**_
&nbsp;&nbsp;&nbsp;&nbsp;_**[Some Additional Challenges](#challenges)**_
&nbsp;&nbsp;&nbsp;&nbsp;_**[Feature Engineering and Train/Test Split](#feature)**_
_**[II - Models & Results](#models)**_
_**[III - Limitations & Potential Improvements](#limitations)**_
_**[Conclusion](#conclusion)**_
_**[Appendix](#appendix)**_
_**[Appendix 1: Features Tables](#appendix1)**_
_**[Appendix 2: Model Results](#appendix2)**_
_**[Appendix 3: Visualizations](#appendix3)**_
_**[Appendix 4: Reproducing the Code](#appendix4)**_	

## Introduction <a name="introduction"></a>

In this project, we attempt to predict whether or not a song in the hot 100 Billboard will reach the top 10. Billboard kept a record of music sales and airplays of singles since the 1940&#39;s. It is the most consistent and trusted source of music rankings and could thus be very informative. Through this endeavor, we intend to focus on &quot;external&quot; factors (music label, search trends,etc.) in addition to &quot;internal&quot; details on the song itself (length, danceability, energy, etc.) to make such a prediction. There have been a few projects leveraging the &quot;internal&quot; aspects of the song to predict whether or not the song would appear in the hot 100 Billboard charts at some point. However, our analysis goes deeper as it takes into account additional &quot;external&quot; features such as the ones we mentioned previously and attempts to predict the outperformers among the Billboard-featured songs.

We believe that the project could be very useful for music producers, labels and artists. For instance, with the help of the prediction, artists could gain inferential insights on factors that affect the popularity of hit songs. The prediction could also help labels manage the lifecycle of music pieces considering the popularity to maximize the value of inventory and adjust advertising accurately. Such a prediction could also help event planners in selecting artists before their songs have reached the top of the Billboard and help allow them to create events better tailored to the current trends and at a lower cost.

## I - Data Processing <a name="data-processing"></a>

Our data originates from various sources. We leveraged and aggregated data from Billboard, Spotify, RIAA and Google Trends.

### Data Sources <a name="data-sources"></a>
#### &nbsp;&nbsp;&nbsp;&nbsp;A) Billboard <a name="billboard"></a>

Leveraging the &quot;Billboard&quot; library,  we were able to gather the rank of each song for each week for which the Billboard was released since March 21st, 1998.

#### &nbsp;&nbsp;&nbsp;&nbsp;B) Spotify <a name="spotify"></a>

Spotify has more than 100 million subscribers as of Q1 2019 and contains one of the most comprehensive music libraries in the world. Luckily, they also provide very broad access to their data through a friendly Web API. After registering to the Web API, we used the Spotify library2 to find the spotify-related information for a given song. Using this API, we find all the information related to the song itself: some &quot;intrinsic&quot; data (i.e. length of the song, danceability, tempo, etc.) but also numerous &quot;extrinsic&quot; features (i.e. album type, release date, etc.).

#### &nbsp;&nbsp;&nbsp;&nbsp;C) The Recording Industry Association of America (RIAA) <a name="riaa"></a>

The RIAA has honored the best music records through Gold &amp; Platinum Awards since 1958. Gold and platinum awards are given depending on sales and streaming figures and hence are another indication of a song&#39;s success, or an artist&#39;s popularity.

However, the RIAA does not provide an easy access to its data or an API. To get the data, we had to use Selenium and simulate a &quot;human browser&quot; for every artist. Interacting with the page through the HTML/Javascript was challenging. The process itself was also time-consuming (requiring more than 20 hours of runtime) and the data was in a messier format but we were able to scrape awards data for all the artists in our dataset.

#### &nbsp;&nbsp;&nbsp;&nbsp;D) Google Trends <a name="trends"></a>

Google Trends analyzes the popularity of top search queries in Google Search across various regions and languages. We use a library to scrape Google Trends and look at the average popularity of an artist three months prior to the release of the song. Unfortunately, Google Trends only contains data following 01/01/2004.

### Some Additional Challenges <a name="challenges"></a>

One of our main challenges was the conception of the original dataset. Our data came from very different sources and each platform had its particularities.

A particular challenge was in finding a maximum number of songs on Spotify. The search functionality expected very particular similarities between the two strings to be able to correctly identify the songs (sometimes there are a lot of songs with the same titles or the &quot;feat&quot; in the artist name may trip up the search). To counter such an issue, we tried various combinations of artist/title strings for unidentified songs (i.e. splitting on &quot;Featuring&quot; and searching for both artists, replacing special characters, etc.) and leveraged intensively the &quot;SeatGeek Fuzzy Wuzzy&quot; python library, using a mix of &quot;partial\_ratio&quot; and &quot;ratio&quot; to accurately match strings3 with the relevant song. We faced similar problems for the RIAA dataset and used comparable techniques to find all the awards related to each artists.

Additionally, for the RIAA data, the string matching for multiple artists was compounded with the fact that the search function was a lot less restrictive than the Spotify one. We thus had to manually remove around 3000 rows to make sure our data was accurate.

Google Trends also places a limit on how many times its data can be accessed every day. Thus, we had to run our process during multiple days so as to capture the entire dataframe.

### Feature Engineering and Train/Test Split <a name="feature"></a>

Thanks to the data scraped from all the various APIs, we created plenty of features that seemed able to capture what makes a song a hit. For instance, we leveraged the Billboard chart to compute the rank obtained by a song during its first appearance. The closer a given song&#39;s rank is to 10 when it first appears, the more likely it is that it will later reach the top 10 (i.e. Appendix 3). We also gathered the number of songs each artists placed in the Hot 100 and Hot 10, to have a proxy for the musician&#39;s popularity (i.e. we could easily imagine that the last song of Beyonce, who has already placed 61 songs in the Hot 100, has great chances to be on this ranking).

From the RIAA data, we summarized the total number of gold/platinum awards and the number of songs with a certification that a given artist collected before the song appeared on the Billboard as it could be a proxy of an artist&#39;s popularity/success.

Initially, we had over 1230 different labels from Spotify. Using string-matching techniques, we were able to aggregate the labels to ~1000. However, given our limited amount of data, we created categories to segregate the different types of labels (i.e. &quot;Mega Label&quot; have more than 200 songs in our dataset, &quot;Great Label&quot; have more than 100 songs, etc.) into just a few categories.

**An exhaustive list of all the features created and/or used in our models can be found in the Appendix 1 at the end of this report. Appendix 4 contains instructions to reproduce the dataset.**

Given that a song may take a few weeks to reach the top 10, we have had to delete the data corresponding to the last 6 weeks. This number corresponds to the median number of weeks a song takes to reach the top 10 (it was computed only on the songs which effectively reached the top 10). We used the median to cancel the effect of outliers (i.e. a few songs such as _All I Want for Christmas Is You_ took more than 6000 days to reach the top 10). Thus, by ignoring these rows and allowing for a few weeks for songs to reach the top 10, we make sure that our test set represents more accurately the real distribution of the data.

## II - Models &amp; Results <a name="model"></a>

An important challenge we have had to deal with is class imbalance. Approximately 94% of the songs that do not rank in the top 10 the first time they enter the Billboard rankings never reach the top 10. By simply selecting that the song will not end up in the top 10 all the time, we would thus be correct 94% of the time (baseline model) but that would not help us find hits before they happen. For our analysis to be impactful, we need to be able to correctly identify future hits. We aim hence to maximize Precision, or the probability that a song is indeed a future hit when we predict that it will be so ().

Because of our heavy class imbalance, a simple logistic regression would only predict that the song never reaches the top 10 and does not fare any better than our baseline model. To counter this, we start by attempting undersampling. To undersample, we shuffled our training set and kept as many &quot;0&quot; than &quot;1&quot; for our variable &quot;top 10&quot; (we ended up with a much smaller training set of ~1200 rows). We trained our model on the smaller dataset but found poor results. Hence, given the small size of our dataset, oversampling was more efficient. To do so, we used a technique called SMOTE, that creates synthetic cases of the minority class, allowing us to have a more balanced training set. As per Appendix 2, SMOTE allowed us to improve our results meaningfully.

Logistic regression is a high bias and low variance model. However, other methods such as boosting are more prone to overfitting. Given the relatively small amount of data available (6287 songs in the training set and the number of features (26) being used, we decided to attempt to use Principal Components Analysis to reduce variance. Using the scree plot, we find that 1 component is the optimal given that it captures ~0.99 of the variance. However, it was unsuccessful in improving our models&#39; performance and we ended up not using it. In addition, we decided not to use the data we collected around Google Trends as it was not very helpful in improving our model. Because it is only available since 2004, our model that included this feature was of a much smaller size, did not help with tackling overfitting and hence did not have better results.

**Our final results are summarized in the table in Appendix 2.**

Our best model is **Ordinal Regression** with an AUC of **0.66**. We are able to reach a precision  of ~21% using a threshold of 0.75. On the test set, assigning all the songs to the top 10 would have yielded a precision of 6% so our models do provide a significant improvement to the baseline. However, it may not be sufficient to be actionable per se as precision remains relatively low and we are only predicting very few songs of the  top 10. We require additional features and further analysis.

## III - Limitations &amp; Potential Improvements <a name="limitations"></a>

As highlighted by Lucas during our presentation, our dependent variable is an ordered ranking and thus depends on the other observations present in the Billboard that week. Rank is thus not independent and identically distributed and would need additional processing so as to be better adjusted for. To account for this, we first explored using an alternative dependent variable (number of sales, number of views…) to reframe the problem. However, given the lack of availability of historical data, we attempted to use the ranking at our advantage and ran an ordinal regression (see Appendix 2). To improve our results in a further analysis, more complex optimization methods might also be used.

Our model has several additional limitations. We know that people&#39;s tastes regarding music changes radically over time. Rap is today one of the most popular music genres, but wasn&#39;t important in the 80s. Since we use the past performance of the songs, our model may be outdated after five or ten years, and could need to be regularly updated, by dropping some of the oldest songs. An interesting fact to illustrate this is that, there seems to be much less turnover in the billboard rankings: back in 1999, around 18% of the songs that did not initially place in the top 10, eventually did so while in 2018, only around 3% did so (see graph in Appendix 3).

To make our model more powerful, we could leverage social networks&#39; data. Using NLP, we could calculate a sentiment score for a given artists&#39; as a song is released. It could give a first sense of the song&#39;s popularity before sales/streaming data evolve. It was really a shame that we couldn&#39;t use Twitter&#39;s API. We strongly believe that using for example tweets referring to a song before its release can be a powerful feature. However, Twitter gives access to historical tweets (posted more than a week ago) only to its professional customers.

More simply, we could also use the genre of the songs to improve our model. We have not had time to do so given how time-consuming finding the data and string-matching it was (Last.fm would have allowed us to do so). Nevertheless, one could reasonably expect that the genre of a song may be related to its ability to become a hit (i.e. most music that become extremely popular are &quot;pop&quot; music). Finally, we could also gather more information on the artists, by adding her/his country of origin, his age or other potentially relevant features.



## Conclusion <a name="conclusion"></a>

Through our analysis, we have been able to somewhat improve the prediction on the baseline that a song will become a hit (enter the top 10). Nevertheless, our results are not sufficient as of yet to be actionable and guide decision-making. As highlighted in the previous section, we believe that numerous avenues could be explored to improve the analysis, namely handling the ranking nature of our dependent variable or adding additional variables. In addition, while  our results may not yield optimal results to predict Billboard Hits, they may be helpful indicators of a song&#39;s or an artist&#39;s popularity and could contribute to improved decision-making by helping predict alternative metrics (i.e. an artist getting a Grammy Award).

## Appendix <a name="appendix"></a>

### Appendix 1: Features Tables <a name="appendix1"></a>

| **Feature Name** | **Definition** |
| --- | --- |
| artist | Name of the artist(s) |
| title | Title of the song |
| date | Last date the song appeared on the Billboard |
| first\_date | First date the song appeared on the Billboard |
| datetime\_month | Month of the first date the song appeared on the Billboard |
| datetime\_year | Year of the first date the song appeared on the Billboard |
| spotify\_explicit | &quot;Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.&quot; |
| spotify\_duration\_ms | &quot;The duration of the track in milliseconds.&quot; |
| spotify\_disc\_number | &quot;The disc number (usually 1 unless the album consists of more than one disc).&quot; |
| spotify\_track\_number | &quot;The number of the track. If an album has several discs, the track number is the number on the specified disc.&quot; |
| spotify\_key | &quot;The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.&quot; |
| spotify\_danceability | &quot;Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.&quot; |
| spotify\_energy | &quot;Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.&quot; |
| spotify\_loudness | &quot;The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.&quot; |
| spotify\_mode | &quot;Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.&quot; |
| spotify\_speechiness | &quot;Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.&quot; |
| spotify\_acousticness | &quot;A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.&quot; |
| spotify\_instrumentalness | &quot;Predicts whether a track contains no vocals. &quot;Ooh&quot; and &quot;aah&quot; sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly &quot;vocal&quot;. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.&quot; |
| spotify\_liveness | &quot;Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.&quot; |
| spotify\_valence | &quot;A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).&quot; |
| spotify\_tempo | &quot;The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.&quot; |
| spotify\_time\_signature | &quot;An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).&quot; |
| spotify\_album\_type | &quot;The type of the album: one of &quot;album&quot; , &quot;single&quot; , or &quot;compilation&quot;&quot; |
| spotify\_album\_release\_date | The date the album was released |
| release\_month | The month the album was released |
| release\_year | The year the album was released |
| album\_label | The label that produced the album |
| label\_category\_group | Categorical variable created based on the number of songs from a given Label that appeared in the Billboard in the timeframe studied (\&gt;=200: &quot;Mega Label&quot;, \&gt;=100: &quot;Great Label&quot;, \&gt;=50: &quot;Big Label&quot;, \&gt;=20: &quot;Decent Label&quot;, \&gt;=10: &quot;Small Label, \&lt;10: &quot;Mini Label&quot; |
| num\_artists | Number of artists involved in the song |
| last\_award\_type | Last type of RIAA certification the artist received prior to the release of the song |
| award\_num | Number of RIAA certification the artist received prior to the song being released |
| gold\_count | Number of gold RIAA certification the artist received prior to the song being released |
| platinum\_count | Number of platinum RIAA certification the artist received prior to the song being released |
| artist\_has\_award | Binary variable whether the artist received a RIAA certification prior to the release of the song |
| num\_songs\_awards | Number of songs that received RIAA certification for the artist prior to the song being released |
| numberofappearances | Number of times the song appears in the Billboard |
| bestrank | Best ranking the song achieved in the Billboard |
| firstrank | First ranking the song achieved in the Billboard |
| numberofappearances\_artist | Number of songs the author has placed in the Billboard in the past (before the release of his new song) |
| numberofappearances\_artist\_top10 | Number of songs the author has placed in the Billboard top 10  in the past (before the release of his new song) |
| top10 | Binary variable whether the song reached the top 10 in the Billboard |

<center> Proportion of songs that reach the top 10 depending on their initial ranking </center>



### Appendix 4: Reproducing the Code <a name="appendix4"></a>

1. Follow the instructions and run &quot;ScrapeBillboard.ipnyb&quot; to download the data from Billboard
2. Follow the instructions and run &quot;ScrapeSpotify.ipynb&quot; to download the data from Spotify and find the internal characteristics of each songs
3. Follow the instructions and run &quot;ScrapeRIAA.ipynb&quot; to download and clean the data from RIAA
4. Follow the instructions and run &quot;Feature\_engineering\_final.ipynb&quot; to create new features from the original Billboard dataset downloaded in the previous steps
5. Follow the instructions and run &quot;Aggregating.ipynb&quot; to merge all the datasets together
6. Follow the instructions and run &quot;google\_trend\_acquire.ipynb&quot; to get google trend for the songs, then run &quot;google\_trend\_merge.ipynb&quot; to merge with the main aggregated dataset.

**To run models:**

1. Run &quot;Logistic Regression.ipynb&quot; to run a logistic regression model and assess the results
2. Run &quot;Random Forest.ipynb&quot; to run a random forest model and assess the results
3. Run &quot;boosting (LightGBM).ipynb&quot; to run a boosting model and assess the results
4. Run &quot;NeuralNetworks.ipynb&quot; to run a neural network model and assess the results
5. Run &quot;Ordinal Regression.ipynb&quot; to run a boosting model and assess the results

**Files:**

- Visualizations are available in &quot;Visualizations.ipynb&quot;

- song\_df\_aggregate.pkl contains our final dataset

- train\_set.pkl, test\_set.pkl, ytrain and ytest contain our X\_train, X\_test, y\_train and y\_test respectively.

## Sources

- [Python API for Downloading Billboard Charts](https://github.com/guoguo12/billboard-charts)
- [Python API for Downloading Spotify Data](https://spotipy.readthedocs.io/en/latest/)
- [SeatGeek's Python Fuzzy String Matching Library](https://github.com/seatgeek/fuzzywuzzy)