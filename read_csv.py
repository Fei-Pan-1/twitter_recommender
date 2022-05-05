import pandas as pd

df = pd.read_csv('downloaded_tweets.csv')
# count = df['author'].value_counts()
# count = df.groupby(['author']).count()
# df_new = df.loc[df['author'].isin(count.index[count > 40])]
# df_new = df_new.loc[df['author'].isin(count.index[count < 400])]
# df_count = df_new['author'].value_counts()
# df_new = df_new.reset_index(drop=True)
df_new = df.sort_values(by=['author', 'date'], ascending=False)

df_new.to_csv('downloaded_tweets_1.csv', index=False, header=True)
# print(df_new)
pd.set_option('display.max_columns', None)
# print(df)