import os
import time
import tweepy
from dotenv import load_dotenv

load_dotenv()

class MemecoinTracker:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            wait_on_rate_limit=True
        )
        self.search_interval = 1800  # Increased to 30 minutes for safety
        self.last_search_time = 0
        self.rate_limit_reset = 0

    def get_tweets(self, coin: str):
        """Advanced tweet fetching with rate limit awareness"""
        try:
            current_time = time.time()
            
            # Check if we're in rate limit cooldown
            if current_time < self.rate_limit_reset:
                wait_time = self.rate_limit_reset - current_time
                print(f"⏳ Rate limit active. Waiting {int(wait_time/60)} minutes...")
                time.sleep(wait_time)
                return 0
            
            # Enforce minimum interval between searches
            if current_time - self.last_search_time < self.search_interval:
                wait_time = self.search_interval - (current_time - self.last_search_time)
                print(f"🕒 Minimum interval: Waiting {int(wait_time)} seconds...")
                time.sleep(wait_time)
            
            print(f"\n🔍 Searching for ${coin} tweets at {time.ctime()}")
            
            # Simple but effective query
            tweets = self.client.search_recent_tweets(
                query=f"{coin} lang:en -is:retweet",
                max_results=10,
                tweet_fields=["created_at", "public_metrics"]
            )
            
            self.last_search_time = time.time()
            
            if tweets.data:
                self._display_tweets(tweets, coin)
                return len(tweets.data)
            print("No relevant tweets found")
            return 0
            
        except tweepy.TweepyException as e:
            if "Too Many Requests" in str(e):
                self.rate_limit_reset = time.time() + 15*60  # Assume 15 min cooldown
                print("⚠️ Hit rate limit. Will retry after cooldown.")
            print(f"Twitter Error: {str(e)[:100]}...")
            return 0
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return 0

    def _display_tweets(self, tweets, coin):
        """Clean tweet display with engagement metrics"""
        print(f"\n📊 Found {len(tweets.data)} ${coin} tweets:")
        print("="*60)
        for tweet in tweets.data:
            print(f"\n🕒 {tweet.created_at}")
            print(f"❤️ {tweet.public_metrics['like_count']} likes")
            print(f"🔁 {tweet.public_metrics['retweet_count']} retweets")
            print(f"📝 {tweet.text[:100]}{'...' if len(tweet.text) > 100 else ''}")
        print("="*60)

if __name__ == "__main__":
    tracker = MemecoinTracker()
    print("\n" + "="*50)
    print(f"🚀 Starting ${'WIF'} tracker")
    print(f"⏰ Checks every {tracker.search_interval//60} minutes")
    print("="*50)
    
    try:
        while True:
            count = tracker.get_tweets("WIF")
            
            if count > 0:
                next_check = tracker.last_search_time + tracker.search_interval
                print(f"\n⏳ Next check at {time.ctime(next_check)}")
                
                sleep_time = max(0, next_check - time.time())
                time.sleep(sleep_time)
            else:
                time.sleep(60)  # Short wait if no tweets found
            
    except KeyboardInterrupt:
        print("\n🛑 Tracker stopped by user")
