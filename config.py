import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    # if we see the .env file, load it
    load_dotenv()

# now we have them as a handy python strings!
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
API_URL = os.getenv('API_URL')
