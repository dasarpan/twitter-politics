# Example to do sentiment analysis on tweets

# import twitter
import json
import numpy as np
import nltk     # Natural Language Toolkit
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import pandas as pd
import regex as re
import os
# Imported to create word clouds 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# text to emotion
import text2emotion as te

# Hutto, C.J. & Gilbert, E.E. (2014). 
# VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. 
# Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

# to-do:
# Figure out how sent analysis function works
# store those files once analyzed
# same for text2emotion
# Open big v2 file and get all the topics and dates
# after storing them, make it so that all the topics can be opened and analyzed at once

# fix errors
#   Make it so that already created files are not analyzed (os library)

# split them up into categories assigned and make *those* file paths (do manually)
# make graphs (in mpl or even in excel...)
# figure out how many tweets there are of each topic (just do this manually tbh, not that hard)
# save wordclouds for each topic






analyzer = SentimentIntensityAnalyzer()


def sentimentanalysis(df):
  # df = pd.DataFrame(df2['Tweet'])
  scores = np.zeros(len(df))
  pos_scores = np.zeros(len(df))
  neu_scores = np.zeros(len(df))
  neg_scores = np.zeros(len(df))

  angry = np.zeros(len(df))
  fear = np.zeros(len(df))
  happy = np.zeros(len(df))
  sad = np.zeros(len(df))
  surpise = np.zeros(len(df))

  numpos = 0
  numneg = 0 

  for i in range(len(df)):
    # Extract the text portion of the tweet
    text = str(df['Tweet'][i]) # t['text']

    # Measure the polarity of the tweet
    polarity = analyzer.polarity_scores(text)
    if(polarity['pos'] > 0 or polarity['neg'] > 0):
      # Store the normalized, weighted composite score
      scores[i] = polarity['compound']
      pos_scores[i] = polarity['pos']
      neu_scores[i] = polarity['neu']
      neg_scores[i] = polarity['neg']
      if(polarity['pos'] > polarity['neg']):
        numpos += 1
      elif(polarity['pos'] < polarity['neg']):
        numneg += 1

    emotion = te.get_emotion(text)
    angry[i] = emotion['Angry']
    fear[i] = emotion['Fear']
    happy[i] = emotion['Happy']
    sad[i] = emotion['Sad']
    surpise[i] = emotion['Surprise']

  scoresdf1 = pd.DataFrame(pos_scores)
  scoresdf2 = pd.DataFrame(neu_scores)
  scoresdf3 = pd.DataFrame(neg_scores)
  scoresdf4 = pd.DataFrame(scores)
  
  emotiondf1 = pd.DataFrame(angry)
  emotiondf2 = pd.DataFrame(fear)
  emotiondf3 = pd.DataFrame(happy)
  emotiondf4 = pd.DataFrame(sad)
  emotiondf5 = pd.DataFrame(surpise)

  scoresdf1.columns = ['pos_score']
  scoresdf2.columns = ['neu_score']
  scoresdf3.columns = ['neg_score']
  scoresdf4.columns = ['compound_score']  
  
  emotiondf1.columns = ['angry_score']
  emotiondf2.columns = ['fear_score']
  emotiondf3.columns = ['happy_score']
  emotiondf4.columns = ['sad_score']
  emotiondf5.columns = ['surprise_score']

  df = pd.concat([df, scoresdf1, scoresdf2, scoresdf3, scoresdf4, emotiondf1, emotiondf2, emotiondf3, emotiondf4, emotiondf5], axis=1)
  # print(df.info())

  # posavg = np.average(df['pos_scores'])
  # neuavg = np.average(df['neu_scores'])
  # negavg = np.average(df['neg_scores'])
  # compavg = np.average(df['compound'])

  # print("VADER Analysis Average Positive Score:", posavg)
  # print("VADER Analysis Average Neutral Score:", neuavg)
  # print("VADER Analysis Average Negative Score:", negavg)
  # print("VADER Analysis Average Compound Score:", compavg)

  # print("Number of Positive Scores:", numpos)
  # print("Number of Negative Scores:", numneg)

  return df


#compound score all tweets
#sentimentanalysis('Research1.csv')

# # for topic in df['Search']:
# for i in range(len(df)):
#   topic = re.sub(r'-filter:retweets', '', df['Search'][i])
#   df['Search'][i] = topic.rstrip()
#   print(len(df) - i, "remaining")

# df.to_csv("Research1Clean_v2.csv")
# print(df.tail())

# -------------------- parsing out each date ---------------------- #
def datesentiment(df):
  listofdf_dates = []
  for date in dates:
    path = "df_by_topic_by_date/" + topic
    df_name = path + "/" + df_names + "_" + date + ".csv"

    if not (os.path.isfile(df_name)):
      listoftweetsbydate = []
      for j in range(len(df)):
        if(df['Entered on'][j] == date):
          listoftweetsbydate.append([df['Search'][j], df['Tweet'][j], df['Entered on'][j]])
      if(not os.path.isdir(path)):
        os.mkdir(path)
      if(len(listoftweetsbydate) >= 1):
        df_temp = pd.DataFrame(listoftweetsbydate)
        listofdf_dates.append(df_name)
        df_temp.columns = ['Search', 'Tweet', 'Entered on']
        df_temp = sentimentanalysis(df_temp)
        df_temp.to_csv(df_name)
      print("done with", date)

df = pd.read_csv("Research1Clean_v2.csv", encoding='UTF-8') # or ISO-8859-1
df.columns = ['num', 'Search', 'Tweet', 'Entered on']
df = df.drop(['num'], axis = 1)

dates = []
for date in df['Entered on']:
  if date not in dates:
    if(date != 'Entered on'):
      dates.append(date)

topics = []
for topic in df['Search']:
  if topic not in topics:
    if(topic != 'Search'):
      topics.append(topic)

# completed_topics = ["Biden", "Trump", "BLM", "Amy Coney Barrett", "Black Lives Matter", "Kamala Harris", "Pence", "Socialism"]

for topic in topics:
  # if topic not in completed_topics:
  print(topic)
  df_names = "df_" + topic
  df_root = "df_by_topic/"
  df_directory = df_root + df_names + ".csv"
  df = pd.read_csv(df_directory, encoding='UTF-8') # or ISO-8859-1
  df.columns = ['num', 'Search', 'Tweet', 'Entered on']
  df = df.drop(['num'], axis = 1)
  datesentiment(df)

# sentiment by topic
def topicsentiment(df):
  listofdf_topics = []
  for topic in topics:
    listoftweetsbytopic = []
    for j in range(len(df)):
      if(df['Search'][j] == topic):
        listoftweetsbytopic.append([df['Search'][j], df['Tweet'][j], df['Entered on'][j]])
    df_temp = pd.DataFrame(listoftweetsbytopic)
    df_name = "df_by_topic/df_" + topic + ".csv"
    listofdf_topics.append(df_name)
    df_temp.columns = ['Search', 'Tweet', 'Entered on']
    # df_temp.to_csv(df_name)
  
    # sentimentanalysis(df_temp)
# topicsentiment(df)






# wordcloud code
def wordcloud():
  tweet_list=[]  
  for tweet in df["Tweet"]:
    tweet_tokens=tweet.split()
    for word in tweet_tokens:
      tweet_list.append(word)

  counter = Counter(tweet_list)
  most_occur = counter.most_common(1000)
  text = ' '.join([x[0] for x in most_occur])
  wordcloud_tweet = WordCloud().generate(text)
  plt.figure(figsize = (15,8))
  plt.axis('off')
  plt.imshow(wordcloud_tweet,interpolation='bilinear')
  plt.show()
