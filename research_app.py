import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class MemecoinTracker:
    def __init__(self):
        self.twitter = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            wait_on_rate_limit=True
        )
    
    def track(self, coins=["WIF", "BONK"]):
        """Analyze Twitter trends for Solana memecoins"""
        for coin in coins:
            tweets = self.twitter.search_recent_tweets(
                query=f"${coin} lang:en -is:retweet",
                max_results=50,
                tweet_fields=["created_at"]
            )
            print(f"${coin}: {len(tweets.data)} mentions")

if __name__ == "__main__":
    MemecoinTracker().track()
