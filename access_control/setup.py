"""
Create corpus with necessary filter attributes.
"""

import os
import json
import requests

# load authentication info from environment
PERSONAL_API_KEY = os.environ['PERSONAL_API_KEY']
CORPUS_KEY = os.environ['CORPUS_KEY']

# API endpoint
API_ENDPOINT = "https://api.vectara.io/v2/corpora"

create_corpus_payload = json.dumps({
  "key": CORPUS_KEY,
  "name": CORPUS_KEY,
  "description": "Shows how to implement a flexible access control model in Vectara.",
  "filter_attributes": [
    {
      "name": "owner",
      "level": "document",
      "description": "Owner of the document within the corpus. Either the user ID for who indexed it or 'global' "
                     "if it is publicly accessible.",
      "indexed": True,
      "type": "text"
    }, {
      "name": "groups",
      "level": "document",
      "description": "List of the groups that are permitted to query the document. If it is not set or is "
                     "empty that means it is a private document, viewable only by the user who is the owner.",
      "indexed": True,
      "type": "list[text]"
    }, {
      "name": "roles",
      "level": "document",
      "description": "List of the roles that are permitted to query the document. If it is not set or is "
                     "empty that means no specific roles have query permissions, and users will have to "
                     "have permission via another access control pathway.",
      "indexed": True,
      "type": "list[text]"
    }, {
      "name": "project",
      "level": "document",
      "description": "The project to which the document belongs. This is used for additional filtering to narrow the "
                     "scope of a query.",
      "indexed": True,
      "type": "text"
    }
  ]
})

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': PERSONAL_API_KEY
}

print(f"Creating corpus with key {CORPUS_KEY}...")

response = requests.request("POST", API_ENDPOINT, headers=headers, data=create_corpus_payload)

print(f"Finished. Response: {response.text}")
