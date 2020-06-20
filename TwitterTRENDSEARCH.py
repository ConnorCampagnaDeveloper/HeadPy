import tweepy
import requests
from bs4 import BeautifulSoup
import time
#twitter Api keys

consumer_key = "bzBQXbdVB9ApH1iprVV95mPbw"
consumer_secret = "9ioMTEVXgZaJCxcHQuIuwMFBRZIRua918XBaDrO4FIQ6eu0UCa"

access_token = "1273922820079263746-H1tMDY1zFzrZhiGyNptC2WShRf5wHu"
access_token_secret = "sy1eZTyjJMOiNNmOxZSmf26tW78PV3LVdzJSqzWgniXPZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
FILE_NAME = "Last_seen_id.txt"

# BBC NEWS
res = requests.get('https://www.bbc.co.uk/news')
soup = BeautifulSoup(res.text, 'lxml')

show = soup.select('h3')

#retweets
user = api.me()
print(user.name)

def main():
    search = ("Xbox","Call OF Duty")

    numberofTweets = 5
    for tweet in tweepy.Cursor(api.search,search).items(numberofTweets):
        try:
            tweet.retweet()
            print("Tweet Retweeted")
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break



def retrieve_last_seen_id(file_name):

    f_read = open(file_name, 'r')

    last_seen_id = int(f_read.read().strip())

    f_read.close()

    return last_seen_id



def store_last_seen_id(last_seen_id, file_name):

    f_write = open(file_name, 'w')

    f_write.write(str(last_seen_id))

    f_write.close()

    return



def reply_to_tweets():

    print('retrieving and replying to tweets...', flush=True)

    # DEV NOTE: use 1060651988453654528 for testing.

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    # NOTE: We need to use tweet_mode='extended' below to show

    # all full tweets (with full_text). Without it, long tweets

    # would be cut off.

    mentions = api.mentions_timeline(

                        last_seen_id,

                        tweet_mode='extended')

    for mention in reversed(mentions):

        print(str(mention.id) + ' - ' + mention.full_text, flush=True)

        last_seen_id = mention.id

        store_last_seen_id(last_seen_id, FILE_NAME)

        usernamesmention ="@" + mention.user.screen_name + " "

        if '#shownews' in mention.full_text.lower():

            print('found #shownews!', flush=True)

            print('responding back...', flush=True)

            api.update_status(usernamesmention +  " " +  " The Mainhead Line for today is :" + " " + show[1].getText())



while True:

    reply_to_tweets()

    time.sleep(15)