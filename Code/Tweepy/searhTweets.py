# Works on PyCharm, Not work on Colab
import pandas as pd
import tweepy
import json
import os

# Essential Acount
with open("credentials/credential_1.json", "r") as infile:
     creds = json.load(infile)

# Academic Research Account
with open("credentials/credential_2.json", "r") as infile:
    creds1 = json.load(infile)

client = tweepy.Client(bearer_token=creds['BEARER_TOKEN'],
                       consumer_key=creds['API_KEY'],
                       consumer_secret=creds['API_KEY_SECRET'],
                       access_token=creds['ACCESS_TOKEN'],
                       access_token_secret=creds['ACCESS_TOKEN_SECRET'],
                       wait_on_rate_limit=True)


def get_followers(user_name):
    # user_name = "EricTopol"
    user = client.get_user(username=user_name)
    id = user.data['id']
    # TODO: 1.paginator 2.follower list length
    followers = client.get_users_followers(id=id)
    follower_list = []
    for follower in followers.data:
        follower_list.append(follower.id)
    return follower_list


def parse_tweet(tweet):
    hashtags = []
    if 'hashtags' in tweet.entities:
        hashtags += [h['tag'] for h in tweet.entities['hashtags']]

    parsed_tweet = {'id': tweet.id, 'author': tweet.author_id, 'date': tweet.created_at, 'hashtags': ','.join(hashtags),
                    'text': tweet.text, 'referenced': tweet.referenced_tweets,
                    'in_reply_to_user_id': tweet.in_reply_to_user_id, 'public_metrics': tweet.public_metrics}
    return parsed_tweet


# get tweets from the first 10 followers
# TODO:1. limit rate 2. public metrics 3. csv 4. search_all
# follower_list = get_followers('EricTopol')
user_count = 10
tweet_count = 0
# For test:
follower_list = [782436559467360257, 1438799166654795776, 1468246640209371147, 825569054995914752, 27474449, 1509672301041700869,
                 34261896, 1481796650322518016, 828404421570748418, 205865558, 1414038798925799431,
                 750781552053878788, 846078295,
                 1428081757367177224, 1298690671935655938, 3341706767]
start_time = '2022-04-24T00:00:00.000Z'
end_time = '2022-04-29T00:00:00.000Z'
# for i in range(len(follower_list)):
for i in range(10):
    df = pd.DataFrame()
    q = 'from:' + str(follower_list[i])
    resp = client.get_recent_tweets_count(query=q, start_time=start_time, end_time=end_time, granularity='day')
    if resp.data:
        print([count['tweet_count'] for count in resp.data], q)
    query = 'from:' + str(follower_list[i]) + ' has:hashtags lang:en'
    # print(query)
    hashtags = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                                  start_time=start_time,
                                  end_time=end_time,
                                  tweet_fields=['author_id', 'created_at', 'entities', 'referenced_tweets',
                                                'in_reply_to_user_id'],
                                  user_fields=['public_metrics'],
                                  max_results=100).flatten(limit=1000):
        # print(tweet)
        if tweet.entities:
            print('ENTITIES: ', tweet.entities)
        # print(type(tweet.entities))
        # print(tweet.id, tweet.created_at, tweet.text, '\n',
        #       tweet.author_id, tweet.referenced_tweets, tweet.in_reply_to_user_id, '\n',
        #       tweet.public_metrics, '\n')

        # print(len(tweet.referenced_tweets))
        # print(tweet.referenced_tweets[0])
        tweet_count += 1
        if 'hashtags' in tweet.entities:
            hashtags += [h['tag'] for h in tweet.entities['hashtags']]
        parsed_tweet = parse_tweet(tweet)
        # print('!!!', parsed_tweet)
        df_new = pd.DataFrame(parsed_tweet, index=[0])
        df = df.append(df_new, ignore_index=True)
        pd.set_option('display.max_columns', None)
        # print('df: \n', df)
    print('author_id: ', follower_list[i], 'hashtags: ', hashtags)

    df = df.drop_duplicates()
    if not os.path.isfile('downloaded_tweets.csv'):
        df.to_csv('downloaded_tweets.csv', index=False, header=True)
        # print('new csv file created')
    else:
        df.to_csv('downloaded_tweets.csv', mode='a', index=False, header=False)
        # print('added to csv file')
    print('downloaded total tweets: ', tweet_count)