import requests
from googleapiclient import discovery
import pandas as pd
import time

caliberate_twitter = pd.read_csv("/Users/eshwar/Downloads/remaining_toxic_users.csv", names = ["username", "tweet"])
print(len(caliberate_twitter['username'].unique()), caliberate_twitter.shape)

KEY = pd.read_csv("whitelist-key.txt", names = ['key'])['key'][0]
service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=KEY)

def get_results(request_id, response, exception):
    toxicity_scores.append((request_id, response))

count = 0
limit = 498
toxicity_scores = []
batch = service.new_batch_http_request(callback=get_results)

iteration = 0

for comment in tweet_list:
    analyze_request = {
      'comment': { 'text': comment},
      'requestedAttributes': {'TOXICITY': {}}
    }
    count += 1
    
    batch.add(service.comments().analyze(body=analyze_request), request_id=str(count))
    
    if count >= limit:
        batch.execute()
        batch = service.new_batch_http_request(callback=get_results)
        count = 0
        print("Sleep #", iteration)
        iteration += 1
        time.sleep(2)
#         break

batch.execute()
print("Done")

toxicity = []
misses = 0
for i in range(len(tweet_list)):
    try:
        toxicity.append(toxicity_scores[i][1]['attributeScores']['TOXICITY']['summaryScore']['value'])
    except:
#         print(i, "Messed up!")
        misses += 1
        toxicity.append(-1.0)

print(len(tweet_list), len(toxicity))

caliberate_twitter['toxicity'] = toxicity
caliberate_twitter.to_csv('/Users/eshwar/Desktop/toxicity-scores-tweets-blocklist-users.csv', index = False)
