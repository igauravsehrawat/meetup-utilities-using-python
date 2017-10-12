import bot_credentials as bc
import tweepy

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

if __name__ == "__main__":

    auth = tweepy.OAuthHandler(
        bc.provide_key("consumer_key"), bc.provide_key("consumer_secret"))

    api = tweepy.API(auth)

    twitterStreamListener = MyStreamListener()
    twitterStream = tweepy.Stream(
        auth = api.auth, listener=twitterStreamListener)
