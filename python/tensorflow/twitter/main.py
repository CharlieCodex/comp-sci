from twitter import Twitter, OAuth
import tensorflow as tf
import json

creds_path = 'creds.json'

with open(creds_path, 'r') as file:
    creds = json.load(file)

api = Twitter(auth=OAuth(creds['access_token_key'],
                         creds['access_token_secret'],
                         creds['consumer_key'],
                         creds['consumer_secret']))

tweets = api.statuses.user_timeline(screen_name="realDonaldTrump",
                                    tweet_mode='extended',
                                    count=2000)

text_tweets = map(lambda t: t['full_text'],
                  tweets)

with open('output.txt', 'w+', encoding='utf8') as file:
    for i, tweet in enumerate(text_tweets):
        file.write(str(i) + ': ' + (tweet + ('\n' * 3)))
