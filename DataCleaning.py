# DataCleaning.py
# cleaning research data using regex


import pandas as pd
from html.parser import HTMLParser 
import re
import itertools
from autocorrect import Speller  
import nltk
from nltk.corpus import stopwords 

df = pd.read_csv('Research1.csv', encoding='UTF-8')
df = df.dropna()
spell = Speller(lang='en')
#open the fle slang.txt 
file=open("slang.txt","r") 
slang=file.read() 

#separating each line present in the file 
slang=slang.split('\n') 

#import english stopwords list from nltk 
stopwords_eng = stopwords.words('english')  

# many data cleaning methods taken from:
# https://www.geeksforgeeks.org/python-efficient-text-data-cleaning/


#dictionary consisting of the contraction and the actual value 
Apos_dict={"'s":" is","n't":" not","'m":" am","'ll":" will", 
           "'d":" would","'ve":" have","'re":" are"} 
counter = 0
for tweet in df["Tweet"]:
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.\S+', "", tweet)
    # remove hashtags
    tweet = re.sub(r'#', '', tweet)
    #remove RT @:
    tweet = re.sub(r'^RT[\s]@\w+:[\s]', '', tweet)
    # remove @ and …
    tweet = re.sub(r'…', '', tweet)
    tweet = re.sub(r'@\w+[\s]', '', tweet)

    #separate the words 
    tweet = " ".join([s for s in re.split("([A-Z][a-z]+[^A-Z]*)",tweet) if s])
    
    #convert to lower case 
    tweet=tweet.lower() 

    #replace the contractions 
    for key,value in Apos_dict.items(): 
        if key in tweet: 
            tweet=tweet.replace(key,value) 

    
    tweet_tokens=tweet.split() 
    slang_word=[] 
    meaning=[] 
    
    #store the slang words and meanings in different lists 
    for line in slang: 
        temp=line.split("=") 
        slang_word.append(temp[0]) 
        meaning.append(temp[-1]) 
    
    #replace the slang word with meaning 
    for i,word in enumerate(tweet_tokens): 
        if word in slang_word: 
            idx=slang_word.index(word) 
            tweet_tokens[i]=meaning[idx] 
            
    tweet=" ".join(tweet_tokens) 

    #One letter in a word should not be present more than twice in continuation 
    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet)) 

    #spell check 
    # tweet=spell(tweet) 

    # remove punctuation
    new = ""
    numspaces = 0
    for char in tweet:
        # remove newlines and replace with spaces
        char = char.replace('\n', ' ')
        char = char.replace('-', ' ')
        if(char == ' ' and numspaces == 0):
            new = new + " "
            numspaces+=1
        elif(char == re.sub(r'\W', '', char)):
            new = new + char
            numspaces = 0
    tweet = new.strip()

    #remove stopwords
    tweet_list=[]  
    tweet_tokens=tweet.split() 
    for word in tweet_tokens: 
        if word not in stopwords_eng: 
            tweet_list.append(word) 

    # print("tweet_list = {}".format(tweet_list))
    tweet = ""
    for words in tweet_list:
        tweet = tweet + words + " "
    

    # print(tweet)
    df["Tweet"][counter] = tweet
    counter += 1
    # print('\n', counter)
    # if(counter >= 10):
    #     break

df.to_csv('Research1Clean.csv')