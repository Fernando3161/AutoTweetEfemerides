'''
Created on 04.05.2021

@author: Fernando Penaherrera (OFFIS/Uni Oldenburg)
'''
from efemerides import TweetsList
import tweepy
import logging
import time
from config import (ACCES_TOKEN, ACCES_TOKEN_SECRET,
                    API_KEY, API_KEY_SECRET, BEARER_TOKEN)

def main():
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                    consumer_key=API_KEY,
                    consumer_secret=API_KEY_SECRET,
                    access_token=ACCES_TOKEN,
                    access_token_secret=ACCES_TOKEN_SECRET,
                    )

    tweetsList = TweetsList()
    while True:
        tweetsList.update()
        list = tweetsList.filtered_list
        text = list[1]
        if len(text)>279:
            text=text[:279]
        client.create_tweet(text=text)
        tweetsList.remove_top_event()
        logging.info("Tweet created: ", text[0:80])
        time.sleep(60*2)

if __name__ == '__main__':
    main()
