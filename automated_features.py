import time
import logging
from typing import List, Optional
import schedule

class AutomatedFeatures:
    def __init__(self, client, llm_handler):
        self.client = client
        self.llm = llm_handler
        self.last_search_time = 0
        self.search_cooldown = 900  # 15 minutes
        self.daily_tweet_count = 0
        self.tweet_limit = 17
        self.last_tweet_reset = time.time()
        self.trusted_sources = self.load_trusted_sources()

    def load_trusted_sources(self):
            """Load trusted sources from a file"""
            try:
                with open('trusted_sources.txt', 'r') as f:
                    return [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                with open('trusted_sources.txt', 'w') as f:
                    f.write('')
                return []

    def save_trusted_sources(self):
        """Save trusted sources to a file"""
        with open('trusted_sources.txt', 'w') as f:
            for source in self.trusted_sources:
                f.write(f'{source}\n')

    def manage_trusted_sources(self):
        """Manage trusted sources list"""
        while True:
            print("\n=== Trusted Sources Management ===")
            print("Current trusted sources:")
            for i, source in enumerate(self.trusted_sources, 1):
                print(f"{i}. {source}")
            print("\n1. Add trusted source")
            print("2. Remove trusted source")
            print("3. Return to main menu")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                new_source = input("Enter username to add (without @): ").strip()
                if new_source and new_source not in self.trusted_sources:
                    self.trusted_sources.append(new_source)
                    self.save_trusted_sources()
                    print(f"Added {new_source} to trusted sources")
            elif choice == '2':
                if self.trusted_sources:
                    index = int(input("Enter number to remove: ")) - 1
                    if 0 <= index < len(self.trusted_sources):
                        removed = self.trusted_sources.pop(index)
                        self.save_trusted_sources()
                        print(f"Removed {removed} from trusted sources")
                else:
                    print("No trusted sources to remove")
            elif choice == '3':
                break

    def auto_like_tweets(self):
        """Set up automatic liking of tweets with specific keywords"""
        keywords = input("Enter keywords to monitor (comma-separated): ").split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        if not keywords:
            print("No valid keywords provided")
            return
            
        try:
            print(f"\nMonitoring for keywords: {', '.join(keywords)}")
            print("Will attempt to like one tweet every 15 minutes")
            print("Press Ctrl+C to stop monitoring")
            
            while True:
                try:
                    if time.time() - self.last_search_time >= self.search_cooldown:
                        query = ' OR '.join(keywords)
                        try:
                            tweets = self.client.search_recent_tweets(
                                query=query,
                                max_results=10,
                                tweet_fields=['text', 'author_id']
                            )
                            
                            if tweets and hasattr(tweets, 'data') and tweets.data:
                                for tweet in tweets.data:
                                    try:
                                        self.client.like(tweet.id)
                                        print(f"Liked tweet: {tweet.text[:50]}...")
                                        self.last_search_time = time.time()
                                        break
                                    except tweepy.errors.Forbidden as e:
                                        print(f"Cannot like tweet (permission error): {e}")
                                    except tweepy.errors.Unauthorized as e:
                                        print("Authentication error while liking tweet")
                                        return
                                    except Exception as e:
                                        print(f"Error liking tweet: {e}")
                            else:
                                print("No tweets found matching the keywords")
                                time.sleep(60)
                                
                        except tweepy.errors.Unauthorized:
                            print("Authentication error. Please check your Bearer Token.")
                            return
                        except tweepy.errors.TooManyRequests:
                            wait_time = 900  # 15 minutes
                            print(f"Rate limit reached. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                        except Exception as e:
                            print(f"Error searching tweets: {e}")
                            time.sleep(60)
                    
                    time.sleep(60)  # Check every minute
                    
                except KeyboardInterrupt:
                    print("\nStopped auto-liking tweets")
                    break
                
        except Exception as e:
            print(f"Fatal error: {e}")
            logging.error(f"Fatal error in auto_like_tweets: {e}")
            
    def auto_retweet_trusted(self):
        """Auto-retweet from trusted sources"""
        if not self.trusted_sources:
            print("No trusted sources configured. Please add some first.")
            return
            
        try:
            print(f"\nMonitoring trusted sources: {', '.join(self.trusted_sources)}")
            print("Will attempt to retweet one post every 15 minutes")
            print("Press Ctrl+C to stop monitoring")
            
            while True:
                if time.time() - self.last_search_time >= self.search_cooldown:
                    query = f"from:{' OR from:'.join(self.trusted_sources)}"
                    tweets = self.client.search_recent_tweets(
                        query=query,
                        max_results=10
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data:
                            try:
                                self.client.retweet(tweet.id)
                                print(f"Retweeted from {tweet.author_id}: {tweet.text[:50]}...")
                                self.last_search_time = time.time()
                                break
                            except Exception as e:
                                print(f"Error retweeting: {e}")
                                continue
                
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\nStopped auto-retweeting")

    def create_content_summary(self):
        """Create a summary of recent tweets from monitoring keywords"""
        keywords = input("Enter keywords for content summary (comma-separated): ").split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        if not keywords:
            print("No valid keywords provided")
            return
            
        try:
            query = ' OR '.join(keywords)
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=10
            )
            
            if not tweets.data:
                print("No tweets found for the given keywords")
                return
                
            # Prepare tweets for summarization
            tweet_texts = [tweet.text for tweet in tweets.data]
            summary_prompt = f"SECRET_WORD Create a brief summary of these tweets about {', '.join(keywords)}:\n" + "\n".join(tweet_texts)
            
            summary = self.llm.get_response(summary_prompt)
            print(f"\nGenerated Summary:\n{summary}")
            
            if input("\nWould you like to tweet this summary? (y/n): ").lower() == 'y':
                self.client.create_tweet(text=summary)
                print("Summary tweeted successfully!")
                
        except Exception as e:
            print(f"Error creating summary: {e}")

    def run_automated_menu(self):
        """Run the automated features menu"""
        while True:
            print("\n=== Automated Features Menu ===")
            print("1. Auto-like tweets with keywords")
            print("2. Auto-retweet trusted sources")
            print("3. Create content summary")
            print("4. Manage trusted sources")
            print("5. Return to main menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                self.auto_like_tweets()
            elif choice == '2':
                self.auto_retweet_trusted()
            elif choice == '3':
                self.create_content_summary()
            elif choice == '4':
                self.manage_trusted_sources()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter 1-5.")