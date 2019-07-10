from multiprocessing import Process
import pandas as pd

def main(): 
    ###split the dataframe into <num_keys> smaller dataframes
    data_path = "macro-comments.csv"
    keys_path = "perspective-api-keys.txt"
    
    tf = pd.read_csv(data_path)
    df = tf
    kf = pd.read_csv(keys_path, names = ['key'])
    num_keys = kf.shape[0]
    print("Number of keys available = ", num_keys)

    chunk_size = int(df.shape[0]/num_keys)
    print("Size of sub_df chunks = ", chunk_size)

    curr = 0
    df_list = []

    for i in range(num_keys):
        if i < num_keys - 1:
            print(i, curr, curr+chunk_size)
            df_list.append(df[curr:curr+chunk_size])
            curr += chunk_size
        else:
            df_list.append(df[curr:])

    ###helper function that'll be used for multi-processing
    def score_comments(key_id):
        
        chunk_num = key_id
        ###get toxicity score from Perspective API
        from googleapiclient import discovery
        import pandas as pd
        import time

        def get_toxicity_score(comment):
            # print(comment)
            analyze_request = {
              'comment': { 'text': comment},
            #  'comment': { 'text': 'friendly greetings from python'},
              'requestedAttributes': {'TOXICITY': {}}
            }

            response = service.comments().analyze(body=analyze_request).execute()
            toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
            return toxicity_score

        # Generates Perspective API client object dynamically based on service name and version.
        API_KEY = pd.read_csv('perspective-api-keys.txt.txt', names = ['key'])['key'][chunk_num]
        service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)
#         filename = "subdf-" + str(chunk_num)
#         tf = pd.read_csv(filename + ".csv")
        tf = df_list[chunk_num]

        count = 0
        toxicity_scores = []

        print(chunk_num, tf.shape[0])

        for comment in tf.comment:
            print(count)
            count += 1
            if ((comment == "[deleted]") | (comment == "[removed]")):
                score = -1.0
                toxicity_scores.append(score)
            else:
                try:
                    score = get_toxicity_score(comment)
                    toxicity_scores.append(score)
                    time.sleep(1)      ###rate limit: 1 request per second
                except:
                    score = -1.0
                    toxicity_scores.append(score)

        tf['toxicity'] = toxicity_scores
        tf.to_csv("chunk-" + str(chunk_num) + "-toxicity.csv", index = False)

    ####create the parallel processes
    proc=[]
    for num in range(num_keys):
        p = Process(target=test_func,args=(num,))
        proc.append(p)

    # Attempting to run simultaneously. This is where the error occurs:
    for p in proc:
        p.start()

    # Join after all processes started, so you actually get parallelism
    for p in proc:
        p.join()

if __name__ == '__main__':
    main()
