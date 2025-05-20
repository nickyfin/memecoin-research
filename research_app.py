import os
import tweepy
from dotenv import load_dotenv
import time  # Added for rate limiting

load_dotenv()

class MemecoinTracker:
    def __init__(self):
        self.twitter = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            wait_on_rate_limit=True
        )
    
    def track(self, coins=["WIF", "BONK"]):
        """Analyze Twitter trends for Solana memecoins (Twitter API-compliant)"""
        try:
            for coin in coins:
                tweets = self.twitter.search_recent_tweets(
                    query=f"${coin} lang:en -is:retweet",
                    max_results=50,
                    tweet_fields=["created_at"]
                )
                print(f"${coin}: {len(tweets.data)} mentions (last 7 days)")
                time.sleep(2)  # Avoid rate limits
        except tweepy.TooManyRequests:
            print("Hit Twitter rate limit - wait 15 minutes")
            time.sleep(900)

if __name__ == "__main__":
    MemecoinTracker().track()
