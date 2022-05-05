import pandas as pd

df = pd.read_csv('downloaded_tweets.csv')
lst = df['author'].unique()
print(lst)
# filter row if hashtags is NONE
# df = df[df['hashtags'].notna()]
# print(df.shape)
for user_id in lst[:1]:
    print(user_id)
    df_new = df.loc[df['author'] == user_id]
    # pd.set_option('display.max_columns', None)
    print(df_new.shape)