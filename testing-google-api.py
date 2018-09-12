from googleapiclient import discovery
import pandas as pd

API_KEY = pd.read_csv('api-key.txt', names = ['key'])['key'][0]

# Generates API client object dynamically based on service name and version.
service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)

analyze_request = {
  'comment': { 'text':'Are you an idiot bro? Dont listen to him. Girl, you look fine!'},
#  'comment': { 'text': 'friendly greetings from python'},
  'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'FLIRTATION': {}}
}

response = service.comments().analyze(body=analyze_request).execute()

import json
print(json.dumps(response, indent=2))
