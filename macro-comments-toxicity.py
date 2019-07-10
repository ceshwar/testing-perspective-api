import time
import pandas as pd 
from googleapiclient import discovery

comments = pd.read_csv('macro-comments.csv')
API_KEY = pd.read_csv('/Users/eshwar/Desktop/research/repos/testing-perspective-api/api-key.txt', names = ['key'])['key'][0]

# Generates API client object dynamically based on service name and version.
service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)

count = 0
toxicity_scores = []

for comment in comments['comment']:
    print(str(count) + " : " + comment)
    #if count % 100 == 0:
    #    print(count)

    time.sleep(1)
 
    count += 1
    analyze_request = {
      'comment': { 'text': comment},
    #  'comment': { 'text': 'friendly greetings from python'},
      'requestedAttributes': {'TOXICITY': {}}
    }
    
    try:
        response = service.comments().analyze(body=analyze_request).execute()
    #     import json
    #     print(json.dumps(response, indent=2))
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    except: 
        toxicity_scores.append(-1.0)
        continue

    print("P(Toxicity) = " + str(toxicity_score))
    toxicity_scores.append(toxicity_score)

comments['toxicity'] = toxicity_scores
comments.to_csv("new-macro-comments-toxicity.csv", index = False)
