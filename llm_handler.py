import openai
import os
from dotenv import load_dotenv
import logging

class LLMHandler:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.secret_word = os.getenv('LLM_SECRET_WORD')
        self.system_prompt = """You are a helpful Twitter bot assistant. You provide concise, 
        engaging responses that fit within Twitter's character limit. If a user's message doesn't 
        include the secret verification word, respond with a generic message about Twitter."""
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        if not self.secret_word:
            raise ValueError("Secret word not found in environment variables")
            
        openai.api_key = self.api_key
        
    def _verify_secret_word(self, message):
        """Check if the message contains the secret word."""
        return self.secret_word.lower() in message.lower()
    
    def _format_for_twitter(self, text):
        """Ensure the response fits Twitter's character limit."""
        max_length = 280
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def get_response(self, message, temperature=0.7):
        """Get a response from the LLM."""
        try:
            if not self._verify_secret_word(message):
                logging.warning("Unauthorized LLM access attempt")
                return "I can only provide general Twitter-related information without proper authorization."
            
            # Remove the secret word from the message before sending to API
            cleaned_message = message.replace(self.secret_word, "").strip()
            
            response = openai.chat.completions.create(
                model="gpt-4",  # You can change this to other models
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": cleaned_message}
                ],
                temperature=temperature,
                max_tokens=150  # Adjust based on your needs
            )
            
            return self._format_for_twitter(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error in LLM processing: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def generate_tweet(self, prompt, temperature=0.7):
        """Generate a tweet from a prompt."""
        try:
            if not self._verify_secret_word(prompt):
                logging.warning("Unauthorized tweet generation attempt")
                return "Tweet generation requires proper authorization."
            
            # Remove the secret word from the prompt
            cleaned_prompt = prompt.replace(self.secret_word, "").strip()
            
            specific_prompt = f"Generate a Twitter post based on this prompt: {cleaned_prompt}, only reply with the tweet and hashtags, nothing else"
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": specific_prompt}
                ],
                temperature=temperature,
                max_tokens=100
            )
            
            return self._format_for_twitter(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error in tweet generation: {e}")
            return f"Sorry, I encountered an error: {str(e)}"