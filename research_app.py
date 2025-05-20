def track(self, coins=["WIF", "BONK"]):
    """Analyze Twitter trends for Solana memecoins"""
    for coin in coins:
        try:
            tweets = self.twitter.search_recent_tweets(
                query=f"${coin} lang:en -is:retweet",
                max_results=50,
                tweet_fields=["created_at"]
            )
            print(f"${coin}: {len(tweets.data)} mentions")
            
        except tweepy.TooManyRequests:
            print(f"Rate limit hit for ${coin}. Waiting 15 minutes...")
            time.sleep(900)  # Twitter's rate limit window
            
        except Exception as e:
            print(f"Error tracking ${coin}: {str(e)}")
            
        time.sleep(2)  # Delay between coin checks
