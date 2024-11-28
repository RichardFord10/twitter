import logging

class MenuHandler:
    def __init__(self, bot):
        self.bot = bot

    def run_main_menu(self):
        """Run the main menu loop"""
        while True:
            choice = self.display_main_menu()
            
            if choice == '1':
                self.bot.send_manual_tweet()
            
            elif choice == '2':
                csv_filename = 'tweets.csv'
                tweets = self.bot.load_tweets_from_csv(csv_filename)
                if tweets:
                    self.bot.schedule_tweets(tweets)
            
            elif choice == '3':
                self.handle_llm_interface()
            
            elif choice == '4':
                self.bot.automated.run_automated_menu()
            
            elif choice == '5':
                print("Exiting the bot. Goodbye!")
                logging.info("Bot exited by user.")
                break
            
            else:
                print("Invalid choice. Please enter 1-5.")

    def display_main_menu(self):
        """Display the main menu"""
        print("\n=== X Bot Menu ===")
        print("1. Send a tweet from terminal input")
        print("2. Send scheduled tweets from CSV")
        print("3. Use LLM interface")
        print("4. Automated features")
        print("5. Exit")
        return input("Enter your choice (1-5): ")

    def handle_llm_interface(self):
        """Handle LLM interface"""
        while True:
            print("\n=== LLM Interface ===")
            print("1. Get LLM response")
            print("2. Generate tweet")
            print("3. Return to main menu")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                prompt = input("Enter your message (include secret word): ")
                response = self.bot.llm.get_response(prompt)
                print(f"\nLLM Response: {response}")
                
                if input("\nWould you like to tweet this response? (y/n): ").lower() == 'y':
                    self.bot.send_manual_tweet(response)
            
            elif choice == "2":
                prompt = input("Enter tweet generation prompt (include secret word): ")
                tweet = self.bot.llm.generate_tweet(prompt)
                print(f"\nGenerated Tweet: {tweet}")
                
                if input("\nWould you like to post this tweet? (y/n): ").lower() == 'y':
                    self.bot.send_manual_tweet(tweet)
            
            elif choice == "3":
                break