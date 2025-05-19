import os
import tweepy
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

class MemecoinTracker:
    def __init__(self):
        self.twitter = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            wait_on_rate_limit=True
        )
    
    def track(self, coins=["WIF", "BONK"]):
        """Track Twitter mentions of Solana memecoins"""
        for coin in coins:
            tweets = self.twitter.search_recent_tweets(
                query=f"${coin} lang:en -is:retweet",
                max_results=10  # Start small to avoid rate limits
            )
            print(f"${coin} mentions (last 7 days): {len(tweets.data)}")

if __name__ == "__main__":
    tracker = MemecoinTracker()
    tracker.track()
