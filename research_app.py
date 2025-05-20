import time  # <-- Add this if not present
import tweepy
from dotenv import load_dotenv
def track(self, coins=["WIF", "BONK"]):
    """Analyze Twitter trends with full error handling"""
    for coin in coins:
        try:
            # API call with rate limiting
            tweets = self.twitter.search_recent_tweets(
                query=f"${coin} lang:en -is:retweet",
                max_results=50,
                tweet_fields=["created_at"]
            )
            print(f"${coin}: {len(tweets.data)} mentions")
            
        except tweepy.TooManyRequests:
            # Twitter rate limit hit
            print(f"⚠️ Twitter rate limit reached for ${coin}. Waiting 15 minutes...")
            time.sleep(900)  # Wait 15 mins (Twitter's rate limit window)
            continue
            
        except tweepy.TweepyException as e:
            # General Twitter API errors
            print(f"❌ Twitter error for ${coin}: {str(e)}")
            continue
            
        except Exception as e:
            # Catch-all for other errors
            print(f"🔴 Unexpected error tracking ${coin}: {str(e)}")
            continue
            
        time.sleep(2)  # Delay between coin checks
