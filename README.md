Twitter Bot

A versatile Twitter bot built using Python and Tweepy that allows users to automate various tasks on Twitter, such as:
	•	Sending manual tweets
	•	Scheduling tweets from a CSV file
	•	Interacting with a Large Language Model (LLM) interface
	•	Automated features including:
	•	Auto-liking tweets with specific keywords
	•	Auto-retweeting from trusted sources
	•	Creating content summaries from recent tweets

Table of Contents

	•	Features
	•	Prerequisites
	•	Installation
	•	Usage
	•	Main Menu Options
	•	Configuration
	•	Environment Variables
	•	Trusted Sources
	•	LLM Secret Word
	•	Logging
	•	Error Handling
	•	Dependencies
	•	Notes
	•	Contributing
	•	License

Features

1. Send Manual Tweets

Allows users to compose and send tweets directly from the terminal.

2. Schedule Tweets from CSV

Users can schedule multiple tweets by providing a CSV file (tweets.csv) containing the tweets and associated hashtags.

3. LLM Interface

Integrate with an LLM (e.g., OpenAI’s GPT-4) to:
	•	Get responses to prompts.
	•	Generate tweets based on prompts.

4. Automated Features

Includes automated functionalities:
	•	Auto-like Tweets: Automatically like tweets containing specified keywords.
	•	Auto-retweet Trusted Sources: Automatically retweet tweets from a list of trusted sources.
	•	Create Content Summary: Generate and tweet summaries of recent tweets related to specified keywords.

Prerequisites

	•	Python: Version 3.6 or higher.
	•	Twitter Developer Account: With appropriate API access.
	•	OpenAI API Key: Required for LLM features.
	•	Twitter API Credentials: API Key, API Secret Key, Access Token, Access Token Secret, and Bearer Token.

Installation

1. Clone the Repository

git clone https://github.com/RichardFord10/twitter.git
cd twitter

2. Create a Virtual Environment

python -m venv venv

3. Activate the Virtual Environment

	•	On Windows:

venv\Scripts\activate


	•	On macOS/Linux:

source venv/bin/activate



4. Install Dependencies

pip install -r requirements.txt

5. Set Up Environment Variables

Create a .env file in the root directory with the following content:

API_KEY=your_twitter_api_key
API_KEY_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
BEARER_TOKEN=your_twitter_bearer_token
OPENAI_API_KEY=your_openai_api_key    # Required for LLM features
LLM_SECRET_WORD=your_secret_word      # A secret word for verifying LLM access

	•	Replace your_twitter_api_key, your_twitter_api_secret, etc., with your actual Twitter API credentials.
	•	Replace your_openai_api_key with your OpenAI API key.
	•	Choose a LLM_SECRET_WORD to secure access to LLM features.

	Note: Do not share this .env file publicly as it contains sensitive information.

6. Prepare the CSV File (Optional)

If you plan to use the scheduled tweets feature, create a tweets.csv file in the following format:

Tweet Text,Hashtag1,Hashtag2,Hashtag3,Hashtag4
Your first tweet,#hashtag1,#hashtag2,#hashtag3,#hashtag4
Your second tweet,#hashtagA,#hashtagB,#hashtagC,#hashtagD

Usage

Run the bot using the following command:

python bot.py

Main Menu Options

You will be presented with a menu:

=== X Bot Menu ===
1. Send a tweet from terminal input
2. Send scheduled tweets from CSV
3. Use LLM interface
4. Automated features
5. Exit
Enter your choice (1-5):

Option 1: Send a Tweet from Terminal Input

	•	Select option 1.
	•	Enter your tweet when prompted.
	•	The bot will post the tweet immediately.

Option 2: Send Scheduled Tweets from CSV

	•	Select option 2.
	•	Ensure your tweets.csv file is properly formatted.
	•	The bot will schedule tweets to be posted every 2 hours.

Option 3: Use LLM Interface

Provides interaction with an LLM for generating content.

Submenu:

=== LLM Interface ===
1. Get LLM response
2. Generate tweet
3. Return to main menu
Enter your choice (1-3):

	•	Get LLM Response: Enter a message including your secret word to receive a response from the LLM.
	•	Generate Tweet: Enter a prompt including your secret word to generate a tweet.
	•	Return to Main Menu: Go back to the main menu.

Option 4: Automated Features

Automate interactions on Twitter.

Submenu:

=== Automated Features Menu ===
1. Auto-like tweets with keywords
2. Auto-retweet trusted sources
3. Create content summary
4. Manage trusted sources
5. Return to main menu
Enter your choice (1-5):

	•	Auto-like Tweets with Keywords: Automatically like tweets containing specified keywords.
	•	Auto-retweet Trusted Sources: Retweet tweets from users you trust.
	•	Create Content Summary: Generate a summary of recent tweets based on keywords.
	•	Manage Trusted Sources: Add or remove trusted sources from your list.

Option 5: Exit

	•	Select option 5 to exit the bot gracefully.

Configuration

Environment Variables

All sensitive information and configuration settings are managed via the .env file. Ensure this file is kept secure and is not committed to version control systems like Git.

Trusted Sources

The bot uses a trusted_sources.txt file to store usernames (without the @ symbol) of Twitter accounts you trust for auto-retweeting.
	•	To add a trusted source:
	•	Use the automated features menu option to manage trusted sources.
	•	To remove a trusted source:
	•	Select the source from the list presented in the trusted sources management menu.

LLM Secret Word

For security, the LLM features require a secret word included in your prompts to verify access.
	•	Set your secret word in the .env file under LLM_SECRET_WORD.
	•	Include this word in any message or prompt intended for the LLM.

Logging

The bot logs its activities to a file named bot.log for monitoring and debugging purposes.
	•	Location: Located in the root directory of the project.
	•	Logging Levels: Includes info, warning, and error messages.

Error Handling

The bot includes error handling for common issues, such as:
	•	Missing API Credentials: Checks for all required API keys and tokens.
	•	Network Errors: Handles connectivity issues gracefully.
	•	Rate Limit Handling: Implements waiting mechanisms when API rate limits are reached.
	•	Unauthorized Access Attempts: Logs and responds to unauthorized attempts to use LLM features.

Dependencies

	•	tweepy: For interacting with the Twitter API.
	•	openai: For LLM integration.
	•	python-dotenv: For loading environment variables.
	•	schedule: For scheduling tasks.
	•	logging: For logging activities.
	•	csv: For handling CSV files.

Install all dependencies using:

pip install -r requirements.txt

Notes

	•	Compliance: Ensure you comply with Twitter’s API policies and terms of service when using this bot.
	•	Usage Limits: Be mindful of API rate limits and usage restrictions, especially when using automated features.
	•	Security: Manage your API keys securely and do not expose them publicly.
	•	Customization: Feel free to modify the bot to suit your needs, but maintain adherence to relevant policies and laws.

Contributing

Contributions are welcome! Please follow these steps:
	1.	Fork the repository
	2.	Create a new branch: git checkout -b feature/YourFeature
	3.	Commit your changes: git commit -m 'Add some feature'
	4.	Push to the branch: git push origin feature/YourFeature
	5.	Open a pull request

License

This project is licensed under the MIT License - see the LICENSE file for details.

Disclaimer: This bot is intended for educational and personal use. The author is not responsible for any misuse of this software. Use responsibly and in accordance with Twitter’s Developer Agreement and Policy.