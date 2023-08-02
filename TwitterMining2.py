import tweepy as tw
import re
import csv
 
from datetime import datetime
from datetime import timedelta
 
NUMBER_of_TWEETS = 100
SEARCH_BEHIND_DAYS= 60
today_date=datetime.today().strftime('%Y-%m-%d')
 
 
today_date_datef = datetime.strptime(today_date, '%Y-%m-%d')
start_date = today_date_datef - timedelta(days=SEARCH_BEHIND_DAYS)
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
 
 
import http.client
import urllib.parse as urlparse   
 
def unshortenurl(url):
    parsed = urlparse.urlparse(url) 
    h = http.client.HTTPConnection(parsed.netloc) 
    h.request('HEAD', parsed.path) 
    response = h.getresponse() 
    if response.status >= 300 and response.status < 400 and response.getheader('Location'):
        return response.getheader('Location') 
    else: return url    
     
     
CONSUMER_KEY = 'hX0fdKM5JYSdtfE3UmlO3Ib2c'
CONSUMER_SECRET = 'PnQZ08BhGqeYEHL65ePVnBB2nS1sVDYcurSEtp4nsrTfhh30KC'
OAUTH_TOKEN = '1269107223361355776-COA25p2u8s6QMNKKk1tlLcbPoxeFD1'
OAUTH_TOKEN_SECRET = 'Oi9BRJvDthZVuLXd75dh916m4HUmNDKqq42yfKt0YSDdX'
 
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)
# Create a custom search term 
               
search_terms=['Trump -filter:retweets', 'Biden -filter:retweets', 'BLM -filter:retweets', 'Black Lives Matter -filter:retweets', 'Amy Coney Barrett -filter:retweets', 
                'Socialism -filter:retweets', 'Pence -filter:retweets', 'Kamala Harris -filter:retweets', 'ACAB -filter:retweets', 'climate change -filter:retweets', 
                'Obama -filter:retweets', 'Obamacare -filter:retweets', 'Affordable Care Act -filter:retweets', 'healthcare -filter:retweets', 'Reform -filter:retweets', 
                'liberal -filter:retweets', 'conservative -filter:retweets', 'mask -filter:retweets', 'COVID -filter:retweets', 'corona -filter:retweets', 'coronavirus -filter:retweets',
                'COVID-19 -filter:retweets', 'Green New Deal -filter:retweets', 'Mail voting -filter:retweets']
               
            
def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))
     
 
    
def save_tweet_info(tw, twt_dict, htags_dict ):
    
    if tw not in twt_dict:
        htags=extract_hash_tags(tw)
        twt_dict[tw]=1
        for ht in htags:
            if ht in htags_dict:
                htags_dict[ht]=htags_dict[ht]+1
            else:   
                htags_dict[ht]=1
 
 
tweet_dict = dict() 
hashtags_dict = dict()
 

i = 0
while(i < 5):                 
  i += 1
  for search_term in search_terms:
    tweets = tw.Cursor(api.search, q=search_term, lang="en", since=SEARCH_BEHIND_DAYS).items(NUMBER_of_TWEETS)
 
    with open('Research1.csv', 'a', encoding="utf8", newline='' ) as csvfile: 
      fieldnames = ['Search', 'Tweet', 'Entered on']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()

      for tweet in tweets:
        writer.writerow({'Search': search_term, 'Tweet': tweet.text, 'Entered on': today_date })

    















    #  fieldnames = ['Search', 'URL', 'Tweet', 'Entered on']
    #  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #  writer.writeheader()
      
 
    #  for tweet in tweets:
    #      urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.text)
    
    #      save_tweet_info(tweet.text, tweet_dict, hashtags_dict ) 
    #      for url in urls:
    #       try:
    #         res = urllib2.urlopen(url)
    #         actual_url = res.geturl()
          
    #         if ( ("https://twitter.com" in actual_url) == False):
                 
    #             if len(actual_url) < 32:
    #                 actual_url =unshortenurl(actual_url) 
    #             print (actual_url)
               
    #             writer.writerow({'Search': search_term, 'URL': actual_url, 'Tweet': tweet.text, 'Entered on': today_date })
               
    #       except:
    #           print (url)    
 
             
#print_count_hashtags(hashtags_dict)
#count_urls()    