# Works on PyCharm, Not work on Colab
import pandas as pd
import tweepy
import json
import os
import time

# Essential Acount
with open("credentials/credential_1.json", "r") as infile:
     creds = json.load(infile)

# Academic Research Account
with open("credentials/credential_2.json", "r") as infile:
    creds1 = json.load(infile)

client = tweepy.Client(bearer_token=creds1['BEARER_TOKEN'],
                       consumer_key=creds1['API_KEY'],
                       consumer_secret=creds1['API_KEY_SECRET'],
                       access_token=creds1['ACCESS_TOKEN'],
                       access_token_secret=creds1['ACCESS_TOKEN_SECRET'],
                       wait_on_rate_limit=True)


def get_followers(user_name):
    user = client.get_user(username=user_name)
    id = user.data['id']
    # TODO: 1.paginator 2.follower list length
    # followers = client.get_users_followers(id=id)
    follower_list = []
    for response in tweepy.Paginator(client.get_users_followers, id=id,
                                     max_results=200, limit=5):
        for follower in response.data:
            follower_list.append(follower.id)

    # for follower in followers.data:
    #     follower_list.append(follower.id)
    return follower_list


def parse_tweet(tweet):
    hashtags = []

    if tweet.entities and 'hashtags' in tweet.entities:
        hashtags += [h['tag'] for h in tweet.entities['hashtags']]

    parsed_tweet = {'id': tweet.id, 'author': tweet.author_id, 'date': tweet.created_at, 'hashtags': ','.join(hashtags),
                    'text': tweet.text, 'referenced': tweet.referenced_tweets[:1] if tweet.referenced_tweets else [None],
                    'in_reply_to_user_id': tweet.in_reply_to_user_id, 'public_metrics': tweet.public_metrics}
    return parsed_tweet


# get tweets from the first 10 followers
# TODO:1. limit rate 2. public metrics 3. csv 4. search_all
# follower_list = get_followers('EricTopol')
tweet_count = 0
# For test:
follower_list = [782436559467360257, 1438799166654795776, 1468246640209371147, 825569054995914752, 27474449,
                 205865558, 1414038798925799431, 205865558, 1459237539018067972, 14861579,
                 1447842061, 1279071226049298432, 1112533464941805570, 1292090165314203649, 1061777739592609793,
                 66994371, 3431894506, 1260265403810566144, 1166898768534523905, 1184921285215825920,
                 1429613089494904832, 1504118998266310657]
start_time = '2022-04-29T00:00:00.000Z'
end_time = '2022-05-01T00:00:00.000Z'
# for i in range(len(follower_list)):
every_n_user = 0
for i in range(18, 22):
    every_n_user += 1
    df = pd.DataFrame()
    q = 'from:' + str(follower_list[i])
    resp = client.get_all_tweets_count(query=q, start_time=start_time, end_time=end_time, granularity='day')
    if resp.data:
        lst = [count['tweet_count'] for count in resp.data]
        print(i, ' - daily tweet post: ', round(sum(lst)/len(lst), 2), 'max: ', max(lst),  lst, q)
    query = 'from:' + str(follower_list[i]) + ' has:hashtags lang:en'
    # print(query)
    hashtags = []
    for tweet in tweepy.Paginator(client.search_all_tweets, query=query,
                                  start_time=start_time,
                                  end_time=end_time,
                                  tweet_fields=['author_id', 'created_at', 'entities', 'referenced_tweets',
                                                'in_reply_to_user_id'],
                                  user_fields=['public_metrics'],
                                  max_results=500).flatten(limit=20000):
        # print(tweet)
        # if tweet.entities:
        #     print('ENTITIES: ', tweet.entities)
        # print(type(tweet.entities))
        # print(tweet.id, tweet.created_at, tweet.text, '\n',
        #       tweet.author_id, tweet.referenced_tweets, tweet.in_reply_to_user_id, '\n',
        #       tweet.public_metrics, '\n')

        # print(len(tweet.referenced_tweets))
        # print(tweet.referenced_tweets[0])
        tweet_count += 1
        if tweet.entities and 'hashtags' in tweet.entities:
            hashtags += [h['tag'] for h in tweet.entities['hashtags']]
        parsed_tweet = parse_tweet(tweet)
        print('!!!-', tweet_count, parsed_tweet)
        df_new = pd.DataFrame(parsed_tweet, index=[0])
        df = df.append(df_new, ignore_index=True)
        # if len(df.index) >= 200:
        #     df.to_csv('downloaded_tweets.csv', mode='a', index=False, header=False)
        #     df = pd.DataFrame()
        # pd.set_option('display.max_columns', None)
        # print('df: \n', df)
        time.sleep(1)
    print('author_id: ', follower_list[i], 'hashtags: ', hashtags)

    df = df.drop_duplicates()
    if not os.path.isfile('downloaded_tweets.csv'):
        df.to_csv('downloaded_tweets.csv', index=False, header=True)
    else:
        df.to_csv('downloaded_tweets.csv', mode='a', index=False, header=False)
        # print('added to csv file')
    print('downloaded total tweets: ', tweet_count, '\n\n\n\n')
    # if every_n_user == 2:
    #     time.sleep(15*60)
    #     every_n_user = 0