# ResearchGraphs.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# for each topic, get the average compound per day, store topic/date/average compound/average each emotions in separate df
# make each list a row in the df
# append the dfs together by category
# group dates together? by week?

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

# returns list of averages for dataframe
def getdata(df, date, topic):
  numpos = 0
  numneg = 0
  for i in range(len(df)):
    if(df['compound_score'][i] > 0):
      numpos += 1
    elif(df['compound_score'][i] < 0):
      numneg += 1
  
  percentpos = numpos/len(df) * 100
  percentneg = numneg/len(df) * 100

  compavg = np.average(df['compound_score'])
  angryavg = np.average(df['angry_score'])
  fearavg = np.average(df['fear_score'])
  happyavg = np.average(df['happy_score'])
  sadavg = np.average(df['sad_score'])
  surpiseavg = np.average(df['surprise_score'])

  averageslist = [topic, date, compavg, percentpos, percentneg, angryavg, fearavg, happyavg, sadavg, surpiseavg]
  return averageslist

def splitbydate():
  for topic in topics:
    listoflists = []
    for date in dates:
      df_names = "df_" + topic
      path = "df_by_topic_by_date/" + topic
      df_name = path + "/" + df_names + "_" + date + ".csv"
      # print(df_name)
      # if is file
      if(os.path.isfile(df_name)):
        df = pd.read_csv(df_name, encoding='UTF-8') # or ISO-8859-1
        listoflists.append(getdata(df, date, topic))
    df2 = pd.DataFrame(listoflists)
    df2.columns = ['Search', 'Entered on', 'compound_avg', 'percent_positive', 'percent_negative','angry_avg', 'fear_avg', 'happy_avg', 'sad_avg', 'surprise_avg']

    newpath = 'df_averages/'
    if(not os.path.isdir(newpath)):
      os.mkdir(newpath)
    newfilename = df_names + "_avg.csv"
    if(not os.path.isfile(newfilename)):
      df2.to_csv(newpath + newfilename)
    # make listoflists into a df, output to .csv

people = ["Trump", "Biden", "Amy Coney Barrett", "Pence", "Kamala Harris", "Obama"]
policy = ["Obamacare", "Affordable Care Act", "Green New Deal", "climate change", "healthcare", "Reform", "Mail voting"]
ideology = ["Socialism", "liberal", "conservative"]
covid = ["mask", "COVID", "corona", "coronavirus", "COVID-19"]
blm = ["BLM", "Black Lives Matter"]
categories_string = ["people", "policy", "ideology", "covid", "blm"]
categories = [people, policy, ideology, covid, blm]

def combinecategories():
  for i, category in enumerate(categories):
    listofdfs = []
    for keyword in category:
      # make new df for each one, add to list of dfs
      df_names = "df_" + keyword + "_avg"
      df_root = "df_averages/"
      df_directory = df_root + df_names + ".csv"
      df_temp = pd.read_csv(df_directory)
      listofdfs.append(df_temp)
    df = pd.concat(listofdfs)
    print(df.head())
    filepath = "df_by_category/"
    if(not os.path.isdir(filepath)):
      os.mkdir(filepath)
    df.to_csv(filepath + "df_" + categories_string[i] + ".csv")

listofstats = ['compound_avg','percent_positive','percent_negative','angry_avg','fear_avg','happy_avg','sad_avg','surprise_avg']


def newfileforeachemotionbycategory():
  for i, category in enumerate(categories):
    filepath = "df_by_category/"
    filepath += "df_" + categories_string[i] + ".csv"
    print(filepath)
    if(os.path.isfile(filepath)):
      df = pd.read_csv(filepath)
      listofdfs2 = []
      comp = []
      pos = []
      neg = []
      angry = []
      fear = []
      hap = []
      sad = []
      surp = []

      for q in range(len(listofstats)):
        df2 = pd.DataFrame(np.random.rand(len(category), len(dates)))
        listofdfs2.append(df2)
      for d, date in enumerate(dates):
        for j in range(len(df)):
          if(df['Entered on'][j] == date):
            comp.append(df['compound_avg'][j])
            pos.append(df['compound_avg'][j])
            neg.append(df['compound_avg'][j])
            angry.append(df['compound_avg'][j])
            fear.append(df['compound_avg'][j])
            hap.append(df['compound_avg'][j])
            sad.append(df['compound_avg'][j])
            surp.append(df['compound_avg'][j])
        # print(len(comp))
        for c in range(len(comp)):
          listofdfs2[0][d][c] = comp[c]
          listofdfs2[1][d][c] = pos[c]
          listofdfs2[2][d][c] = neg[c]
          listofdfs2[3][d][c] = angry[c]
          listofdfs2[4][d][c] = fear[c]
          listofdfs2[5][d][c] = hap[c]
          listofdfs2[6][d][c] = sad[c]
          listofdfs2[7][d][c] = surp[c]
          
          # print(d, c, df2[d][c], comp[c])
        comp = []
        pos = []
        neg = []
        angry = []
        fear = []
        hap = []
        sad = []
        surp = []
        if d == (len(dates) - 1):
          for a, df2 in enumerate(listofdfs2):
            df2 = df2.rename(columns=lambda x: dates[x])
            filepath = "df_by_category_by_stat/"
            # print(filepath, , a)
            if(not os.path.isdir(filepath)):
              os.mkdir(filepath)
            filepath += "df_" + categories_string[i] 
            filepath += "_" + listofstats[a] + ".csv"
            df2.to_csv(filepath)
  # go through whole df
    # if date in df is equal to date[i]
      # add avgs for that date


# combinecategories()
# print("done")
# newfileforeachemotionbycategory()

def moreemotionanalysis():
  dflist = []
  for category in categories_string:
    filepath = "df_by_category/"
    df = pd.read_csv(filepath + "df_" + category + ".csv")
    # print(df)
    dflist.append(df)
  
  dfbig = pd.DataFrame()

  for df in dflist:
    dfbig = dfbig.append([df])
  
  dfbig = dfbig.dropna()
  angrylist = []
  fearlist = []
  happylist = []
  sadlist = []
  surplsit = []

  for date in dates:
    angry_tot = 0
    fear_tot = 0
    happy_tot = 0
    sad_tot = 0
    surp_tot = 0
    for i in range(len(dfbig)):
      if i < 281:
        if(str(dfbig['Entered on'][i]) == date):
          angry_tot += dfbig['angry_avg'][i]
          # print(angry_tot)
          fear_tot += dfbig['fear_avg'][i]
          happy_tot += dfbig['happy_avg'][i]
          sad_tot += dfbig['sad_avg'][i]
          surp_tot += dfbig['surprise_avg'][i]  
    angrylist.append(angry_tot)
    fearlist.append(fear_tot)
    happylist.append(happy_tot)
    sadlist.append(sad_tot)
    surplsit.append(surp_tot)

  # print(angrylist)  

  datelist = [0,0,0,0,0]
  numberslist = [0,0,0,0,0]
  for i, date in enumerate(dates):
    if(angrylist[i] > numberslist[0]):
      datelist[0] = date
      numberslist[0] = angrylist[i]
    if(fearlist[i] > numberslist[1]):
      datelist[1] = date
      numberslist[1] = fearlist[i]
    if(happylist[i] > numberslist[2]):
      datelist[2] = date
      numberslist[2] = happylist[i]
    if(sadlist[i] > numberslist[3]):
      datelist[3] = date
      numberslist[3] = sadlist[i]
    if(surplsit[i] > numberslist[4]):
      datelist[4] = date
      numberslist[4] = surplsit[i]

  
  print(np.average(dfbig['angry_avg']))
  print(np.average(dfbig['fear_avg']))
  print(np.average(dfbig['happy_avg']))
  print(np.average(dfbig['sad_avg']))
  print(np.average(dfbig['surprise_avg']))
  
  print("Day with angriest sentiment:\t",datelist[0], numberslist[0])
  print("Day with most fearful sentiment:", datelist[1], numberslist[1])
  print("Day with happiest sentiment:\t", datelist[2], numberslist[2])
  print("Day with saddest sentiment:\t", datelist[3], numberslist[3])
  print("Day with most surprise sentiment:", datelist[4], numberslist[4])


# moreemotionanalysis()


def get_num_pos_neg():
  for topic in topics:
    listoflists = []
    for date in dates:
      df_names = "df_" + topic
      path = "df_by_topic_by_date/" + topic
      df_name = path + "/" + df_names + "_" + date + ".csv"
      # print(df_name)
      if(os.path.isfile(df_name)):
        df = pd.read_csv(df_name, encoding='UTF-8') # or ISO-8859-1
        listoflists.append(getdata_alt(df, date, topic))
    df2 = pd.DataFrame(listoflists)
    df2.columns = ['Search', 'Entered on', 'strongly_pos', 'strongly_neg', 'total_pos', 'total_neg', 'compound_avg']

    newpath = 'df_counting/'
    if(not os.path.isdir(newpath)):
      os.mkdir(newpath)
    newfilename = df_names + "_counts.csv"
    if(not os.path.isfile(newfilename)):
      df2.to_csv(newpath + newfilename)
    # make listoflists into a df, output to .csv


# returns number of neg/pos tweets for dataframe
def getdata_alt(df, date, topic):
  numpos = 0
  numneg = 0
  numstrongpos = 0
  numstrongneg = 0
  for i in range(len(df)):
    if(df['compound_score'][i] > 0):
      numpos += 1
      if(df['pos_score'][i] > 0.5):
        numstrongpos += 1
    elif(df['compound_score'][i] < 0):
      numneg += 1
      if(df['neg_score'][i] > 0.5):
        numstrongneg += 1
  
  compavg = np.average(df['compound_score'])

  returnlist = [topic, date, numstrongpos, numstrongneg, numpos, numneg, compavg]
  return returnlist

get_num_pos_neg()