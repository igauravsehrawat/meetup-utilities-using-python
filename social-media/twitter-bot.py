import bot_credentials as bc
import tweepy

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

def twitter_stream():
    auth = tweepy.OAuthHandler(
        bc.provide_key("consumer_key"), bc.provide_key("consumer_secret"))
    auth.set_access_token(
        bc.provide_key("access_token"), bc.provide_key("access_token_secret"))
    api = tweepy.API(auth)

    twitter_stream_listener = MyStreamListener()
    twitter_stream = tweepy.Stream(
        auth = api.auth, listener=twitter_stream_listener)
    twitter_stream.filter(track=["python", "programming", "coding"])

if __name__ == "__main__":
    twitter_stream()
