# -*- coding: utf-8 -*-
"""Twitter_Listening_[v1.1.1]

pip install gender_guesser

import tweepy
import json
import re
import io
import pandas as pd
from google.colab import files
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import OrderedDict
import gender_guesser.detector as gender

####### IA
from nltk.classify import SklearnClassifier
from sklearn.model_selection import train_test_split

api_key = ''
api_secret_key = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(api_key,api_secret_key)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

stopwords = files.upload()
stopwords = pd.read_csv(io.BytesIO(stopwords.get('stopwords.csv')), encoding = "ISO-8859-1")

###### BUSCAR SEGUIDORES DE UNA CUENTA

data = api.followers("screen_name")

for f in data:
  print(json.dumps(f._json, indent = 2))

###### BUSCAR TWEETS POR PALABRAS CLAVE

word = input()
word = word.lower()

data = pd.DataFrame()

for t in tweepy.Cursor(api.search, tweet_mode = 'extended', q = word, lang = "es").items(1000):   #geocode = "6.254301,-75.577237,17km"

  data = data.append(other=t._json, ignore_index=True)


g = gender.Detector(case_sensitive = False)
query_results = pd.DataFrame( columns = ['MentionID','User_Name','Screen_Name','Gender','Content'] )
for m in range(0,len(data)):

# Determinar Género del Usuario
  user_gender = g.get_gender((re.sub('[^A-Za-z0-9]+','',data['user'][m]['name'].split()[0])))
# Añadir items al DataFrame
  query_results.loc[m] = [ data['id_str'][m],data['user'][m]['name'],data['user'][m]['screen_name'],user_gender,data['full_text'][m][0:] ]

query_results.head()

query_results['Content'][2]

gender_count = {}
gender_list = query_results['Gender'].unique()

textprops = {  
    'color' : '#FFFFFF',
    'size': '15'
}

for g in gender_list:
  gender_count[g] = len(query_results[ query_results['Gender'] == g ])


plt.pie(gender_count.values(), explode=None, labels=gender_count.keys(),
        colors=['#FF351D','#4080FF','#04A270','brown','yellow','gray','pink'],
        autopct='%1.1f%%', pctdistance=0.65, shadow=True, labeldistance=1.15, startangle=0,
        radius=1.5, counterclock=True, wedgeprops=None, textprops=textprops, center=(0,0),
        frame=False, rotatelabels=False, data=None)

plt.show()

# GUARDAR EXCEL
query_results.to_excel('tweets_about_Rappi.xlsx', index = True)

# MALE / FEMALE COMMENTS
male_comments = query_results[ query_results['Gender'] == 'male' ]
female_comments = query_results[ query_results['Gender'] == 'female' ]

male_comments['Content'].head(5)

search_word = word

words = ' '.join(male_comments['Content'])
cleaned_word_m = " ".join([word.lower() for word in words.split()
                        if 'http' not in word
                            and not word.startswith('@')
                            and not word.startswith('#')
                            and not word.startswith('RT')
                            and word != 'hotmail'
                            and word != 'gmail'
                            and word != search_word

                        ])

wordcloud = WordCloud(stopwords = stopwords['a'],
                  background_color='#000000',
                  width=1000,
                  height=1000
                  ).generate(cleaned_word_m)


plt.figure(1,figsize=(13, 13))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

######
www = []
words = ' '.join(female_comments['Content'])
cleaned_word_f = " ".join([word.lower() for word in words.split()
                        if 'http' not in word
                            and not word.startswith('@')
                            and not word.startswith('#')
                            and not word.startswith('RT')
                            and word != 'hotmail'
                            and word != 'gmail'
                            and word != search_word

                        ])

wordcloud = WordCloud(stopwords = stopwords['a'],
                  background_color='#FFFFFF',
                  width=1000,
                  height=1000
                  ).generate(cleaned_word_f)

plt.figure(1,figsize=(13, 13))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

cleaned_word_f

prueba = {}

for i in cleaned_word_f.split():

  if i in prueba:
    prueba[i] += 1
  else:
    prueba[i] = 1

prueba_desc = OrderedDict(sorted(prueba.items(), key = lambda kv: kv[1], reverse = True))

prueba_desc

female_text = female_comments['Content']
male_text = male_comments['Content']
