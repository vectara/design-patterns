"""
Index multiple documents, each with different values for the attributes to illustrate different subsets of data.
The documents will be queried by different simulated users, each time using having different access control pathways.
"""

import os
import json
import requests

# load authentication info from environment
PERSONAL_API_KEY = os.environ['PERSONAL_API_KEY']
CORPUS_KEY = os.environ['CORPUS_KEY']

# API endpoint
API_ENDPOINT = f"https://api.vectara.io/v2/corpora/{CORPUS_KEY}/upload_file"


def upload_file(path: str, metadata: dict):
    upload_filename = path.split('/')[-1]
    files = {
        'file': (upload_filename, open(path, 'rb')),
        'metadata': (None, json.dumps(metadata), 'application/json'),
    }

    headers = {
      'Accept': 'application/json',
      'x-api-key': PERSONAL_API_KEY
    }

    print(f"Uploading file {path}...")

    response = requests.request("POST", API_ENDPOINT, headers=headers, files=files)

    print(f"Finished. Response: {response.text}")


# File 1 - justin can query, and anyone in the 'history' group who also has the 'analyst' role can query
doc1_metadata = {
    "owner": "justin",
    "groups": ["history"],
    "roles": ["analyst"],
    "project": "lectures"}
upload_file("data/TheGoldenBough.pdf", doc1_metadata)

# File 2 - jun can query, and anyone in the 'history' or 'religion' groups can query regardless of their role
doc2_metadata = {
    "owner": "jun",
    "groups": ["history", "religion"]}
upload_file("data/TheHerosJourney.pdf", doc2_metadata)

# File 3 - jun can query, and anyone in the 'physics' department who has either the 'pii' or 'dean' role
doc3_metadata = {
    "owner": "stephanie",
    "groups": ["physics"],
    "roles": ["pii", "dean"]
    }
upload_file("data/GreatPhysicists.pdf", doc3_metadata)

# File 4 - anyone can query, provided they are in the 'university' group
doc4_metadata = {
    "owner": "global",
    "project": "orientation"}
upload_file("data/UniversityRules.pdf", doc4_metadata)
