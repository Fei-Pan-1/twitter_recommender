# Works on PyCharm, Not work on Colab
import pandas as pd
import tweepy
import json
import os
import time

# Essential Acount
# with open("credentials/credential_1.json", "r") as infile:
#      creds = json.load(infile)

# client = tweepy.Client(bearer_token=creds['BEARER_TOKEN'],
#                        consumer_key=creds['API_KEY'],
#                        consumer_secret=creds['API_KEY_SECRET'],
#                        access_token=creds['ACCESS_TOKEN'],
#                        access_token_secret=creds['ACCESS_TOKEN_SECRET'],
#                        wait_on_rate_limit=True)

# Academic Research Account
with open("credentials/credential_2.json", "r") as infile:
    creds1 = json.load(infile)

client = tweepy.Client(bearer_token=creds1['BEARER_TOKEN'],
                       consumer_key=creds1['API_KEY'],
                       consumer_secret=creds1['API_KEY_SECRET'],
                       access_token=creds1['ACCESS_TOKEN'],
                       access_token_secret=creds1['ACCESS_TOKEN_SECRET'],
                       wait_on_rate_limit=True)


def parse_tweet(tweet):
    tweet_lst = []
    hashtags = []
    if tweet.entities and 'hashtags' in tweet.entities:
        hashtags += [h['tag'] for h in tweet.entities['hashtags']]
    print(tweet)
    parsed_tweet = {'id': str(tweet.id), 'author': str(tweet.author_id), 'date': tweet.created_at, 'hashtags': ','.join(hashtags),
                    'text': tweet.text, 'referenced': tweet.referenced_tweets[:1] if tweet.referenced_tweets else "",
                    'in_reply_to_user_id': tweet.in_reply_to_user_id, 'public_metrics': tweet.public_metrics}
    tweet_lst.append(parsed_tweet)
    # print(parsed_tweet)
    return tweet_lst


def parse_tweet_by_hashtags(tweet):
    # hashtags = []
    hashtag_lst = []
    if tweet.entities and 'hashtags' in tweet.entities:
        for h in tweet.entities['hashtags']:
            hashtag = h['tag'].lower()
            parsed_tweet = {'author': str(tweet.author_id), 'hashtags': hashtag, 'date': tweet.created_at, 'id': str(tweet.id)}
            hashtag_lst.append(parsed_tweet)
    return hashtag_lst

tweet_count = 0
follower_list = [782436559467360257, 1438799166654795776, 1468246640209371147, 825569054995914752, 27474449,
                 205865558, 1414038798925799431, 14861579, 1447842061, 1279071226049298432,
                 1112533464941805570, 1292090165314203649, 1061777739592609793, 66994371, 3431894506,
                 1260265403810566144, 1166898768534523905, 1184921285215825920, 1429613089494904832, 1504118998266310657]

start_time = '2022-01-01T00:00:00.000Z'
end_time = '2022-05-01T00:00:00.000Z'

for i in range(len(follower_list)):
    count = 0
    df_tweet = pd.DataFrame()
    df_hashtag = pd.DataFrame()
    q = 'from:' + str(follower_list[i])
    resp = client.get_all_tweets_count(query=q, start_time=start_time, end_time=end_time, granularity='day')
    if resp.data:
        lst = [count['tweet_count'] for count in resp.data]
        print(i, ' - daily tweet post: ', round(sum(lst)/len(lst), 2), 'max: ', max(lst),  lst, q)
    hashtags = []
    query = 'from:' + str(follower_list[i]) + ' has:hashtags lang:en'
    for tweet in tweepy.Paginator(client.search_all_tweets, query=query,
                                  start_time=start_time,
                                  end_time=end_time,
                                  tweet_fields=['author_id', 'created_at', 'entities', 'referenced_tweets',
                                                'in_reply_to_user_id'],
                                  user_fields=['public_metrics'],
                                  max_results=500).flatten(limit=20000):

        tweet_count += 1
        count += 1
        if tweet.entities and 'hashtags' in tweet.entities:
            hashtags += [h['tag'] for h in tweet.entities['hashtags']]
        parsed_tweet = parse_tweet(tweet)
        hashtag_lst = parse_tweet_by_hashtags(tweet)
        print('!!!-', tweet_count, parsed_tweet)
        # df_tweet = pd.DataFrame.from_dict(parsed_tweet)
        df_tweet = df_tweet.append(parsed_tweet, ignore_index=True)
        df_hashtag = df_hashtag.append(hashtag_lst, ignore_index=True)
        # if count == 499:
        #     time.sleep(15*60)
    print('author_id: ', follower_list[i], 'hashtags: ', hashtags)

    # if not os.path.isfile('data/tweets-hashtags/downloaded_hashtags_extend.csv'):
    #     df_hashtag.to_csv('data/tweets-hashtags/downloaded_hashtags_extend.csv', index=False, header=True)
    # else:
    #     df_hashtag.to_csv('data/tweets-hashtags/downloaded_hashtags_extend.csv', mode='a', index=False, header=False)
    #     # print('added to csv file')
    # if not os.path.isfile('data/tweets-hashtags/downloaded_tweets_extend.csv'):
    #     df_tweet.to_csv('data/tweets-hashtags/downloaded_tweets_extend.csv', index=False, header=True)
    # else:
    #     df_tweet.to_csv('data/tweets-hashtags/downloaded_tweets_extend.csv', mode='a', index=False, header=False)
    print('downloaded total tweets: ', tweet_count, '\n\n\n\n')
