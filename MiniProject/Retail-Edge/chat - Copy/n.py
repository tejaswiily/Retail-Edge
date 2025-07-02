from dotenv import load_dotenv
load_dotenv()  # Loads environment variables

import os

# Check if the environment variable is loaded correctly
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    print("API key not found.")
else:
    print("API key successfully loaded.")
# import nltk
# print(nltk.__version__)  # This should print the installed version if nltk is available
# import nltk
# nltk.download('punkt')
