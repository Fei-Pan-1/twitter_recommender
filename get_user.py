# Works on PyCharm, Not work on Colab
import pandas as pd
import tweepy
import json
import os
import time

# Essential Acount
with open("credentials/credential_1.json", "r") as infile:
     creds = json.load(infile)

# client = tweepy.Client(bearer_token=creds['BEARER_TOKEN'],
#                        consumer_key=creds['API_KEY'],
#                        consumer_secret=creds['API_KEY_SECRET'],
#                        access_token=creds['ACCESS_TOKEN'],
#                        access_token_secret=creds['ACCESS_TOKEN_SECRET'],
#                        wait_on_rate_limit=True)

# Academic Research Account
with open("credentials/credential_2.json", "r") as infile:
    creds1 = json.load(infile)
#
client = tweepy.Client(bearer_token=creds1['BEARER_TOKEN'],
                       consumer_key=creds1['API_KEY'],
                       consumer_secret=creds1['API_KEY_SECRET'],
                       access_token=creds1['ACCESS_TOKEN'],
                       access_token_secret=creds1['ACCESS_TOKEN_SECRET'],
                       wait_on_rate_limit=True)


def get_followers(user_name):
    user = client.get_user(username=user_name)
    id = user.data['id']
    # followers = client.get_users_followers(id=id)
    follower_list = []
    for response in tweepy.Paginator(client.get_users_followers, id=id,
                                     max_results=100, limit=3):
        for follower in response.data:
            follower_list.append(follower.id)
    # print(follower_list)
    # for follower in followers.data:
    #     follower_list.append(follower.id)
    return follower_list


# get tweets from the first 10 followers
follower_list = get_followers('EricTopol')
tweet_count = 0
start_time = '2022-01-01T00:00:00.000Z'
end_time = '2022-05-01T00:00:00.000Z'
every_n_user = 0
active_user_lst = []
for i in range(len(follower_list)):
# for i in range(16, 20):
    every_n_user += 1
    df = pd.DataFrame()
    q = 'from:' + str(follower_list[i])
    resp = client.get_all_tweets_count(query=q, start_time=start_time, end_time=end_time, granularity='day')
    if resp.data:
        lst = [count['tweet_count'] for count in resp.data]
        print(i, ' - daily tweet post: ', round(sum(lst)/len(lst), 2), 'max: ', max(lst),  lst, q)
        if 30 <= sum(lst)/len(lst) <= 100:
            active_user_lst.append(follower_list[i])
            print(i, ' - daily tweet post: ', round(sum(lst) / len(lst), 2), 'max: ', max(lst), lst, q)
    print(active_user_lst)
