import tweepy
import os
from dotenv import load_dotenv
import schedule
import time
import logging
import csv
from llm_handler import LLMHandler
from automated_features import AutomatedFeatures
from menu_handler import MenuHandler

class TwitterBot:
    def __init__(self):
        self._configure_logging()
        self._load_environment()
        self._initialize_client()
        self._initialize_llm()
        # Remove the circular dependency by initializing AutomatedFeatures after import
        from automated_features import AutomatedFeatures
        self.automated = AutomatedFeatures(self.client, self.llm)
        self.menu_handler = MenuHandler(self)

    def _configure_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _load_environment(self):
        """Load environment variables"""
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')  # Add Bearer Token
        
        if not all([self.api_key, self.api_key_secret, self.access_token, 
                    self.access_token_secret, self.bearer_token]):
            raise ValueError("Missing required Twitter API credentials in .env file")

    def _initialize_client(self):
        """Initialize Twitter API client"""
        try:
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_key_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            me = self.client.get_me()
            logging.info(f"Authentication successful for user @{me.data.username}")
            print(f"Authentication successful for user @{me.data.username}")
        except tweepy.errors.Unauthorized as e:
            error_msg = f"Authentication failed: {str(e)}\nPlease verify your credentials."
            logging.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            raise

    def _initialize_llm(self):
        """Initialize LLM handler"""
        try:
            self.llm = LLMHandler()
            logging.info("LLM handler initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing LLM handler: {e}")
            print(f"Error initializing LLM handler: {e}")
            raise

    def send_manual_tweet(self, tweet_text=None):
        """Send a manual tweet"""
        if tweet_text is None:
            tweet_text = input("Enter your tweet: ")
        
        if tweet_text:
            try:
                response = self.client.create_tweet(text=tweet_text)
                tweet_id = response.data['id']
                logging.info(f"Manual Tweeted (ID: {tweet_id}): {tweet_text}")
                print("Tweet sent successfully.")
                return True
            except tweepy.errors.Forbidden as e:
                if "453" in str(e):
                    logging.error("API access level error. Please check your API access tier.")
                    print("API access level error. Please verify your API credentials and access level.")
                else:
                    logging.error(f"Forbidden error: {e}")
                    print(f"Forbidden error: {e}")
            except tweepy.errors.HTTPException as e:
                logging.error(f"Error sending manual tweet: {e}")
                print(f"Error: {e}")
            return False
        else:
            print("Tweet content cannot be empty.")
            return False

    def load_tweets_from_csv(self, csv_filename):
        """Load tweets from CSV file"""
        tweets_list = []
        try:
            with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    tweet_text = row['Tweet Text'].strip()
                    hashtags = [row[f'Hashtag{i}'].strip() for i in range(1, 5) 
                              if row.get(f'Hashtag{i}') and row[f'Hashtag{i}'].strip()]
                    full_tweet = f"{tweet_text} {' '.join(hashtags)}" if hashtags else tweet_text
                    tweets_list.append(full_tweet)
            logging.info(f"Loaded {len(tweets_list)} tweets from {csv_filename}")
            return tweets_list
        except FileNotFoundError:
            logging.error(f"CSV file {csv_filename} not found.")
            print(f"Error: CSV file {csv_filename} not found.")
        except KeyError as e:
            logging.error(f"Missing column in CSV: {e}")
            print(f"Error: Missing column in CSV: {e}")
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")
            print(f"Error reading CSV file: {e}")
        return []

    def schedule_tweets(self, tweets):
        """Schedule tweets for posting"""
        if not tweets:
            print("No tweets to schedule.")
            return

        tweet_index = 0

        def job():
            nonlocal tweet_index
            if tweet_index < len(tweets):
                if self.send_manual_tweet(tweets[tweet_index]):
                    tweet_index += 1
            else:
                print("All scheduled tweets have been posted.")
                logging.info("All scheduled tweets have been posted.")
                schedule.clear()

        schedule.every(2).hours.do(job)
        print(f"Scheduled {len(tweets)} tweets to be posted every 2 hours.")
        logging.info(f"Scheduled {len(tweets)} tweets to be posted every 2 hours.")

        try:
            while tweet_index < len(tweets):
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
            logging.info("Scheduler stopped by user")
            schedule.clear()

    def run(self):
        """Start the bot"""
        print("Bot is running...")
        logging.info("Bot started.")
        try:
            self.menu_handler.run_main_menu()
        except KeyboardInterrupt:
            print("\nBot stopped by user")
            logging.info("Bot stopped by user")
            schedule.clear()

if __name__ == "__main__":
    try:
        bot = TwitterBot()
        bot.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")