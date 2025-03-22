"""
Deletes the corpus.
"""

import os
import requests

# load authentication info from environment
PERSONAL_API_KEY = os.environ['PERSONAL_API_KEY']
CORPUS_KEY = os.environ['CORPUS_KEY']

# API endpoint
API_ENDPOINT = f"https://api.vectara.io/v2/corpora/{CORPUS_KEY}"

payload = {}
headers = {
  'x-api-key': PERSONAL_API_KEY
}


print(f"Deleting corpus with key {CORPUS_KEY}...")

response = requests.request("DELETE", API_ENDPOINT, headers=headers, data=payload)

print(f"Finished. Response: {response.text}")
