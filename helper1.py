# from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    # 1.Number of messages
    num_messages = df.shape[0]
    # 2.Number of Words
    word = []
    for message in df['message']:
        word.extend(message.split(" "))
    # 3.Number of Media Shared
    num_media=df[df['message'] == "<Media omitted>\n"].shape[0]
    # 4.Number of Links Shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(word),num_media,len(links)
def most_actie_user(df):
    df=df[df['user']!='notification']
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'contribution'})
    return x,df
# def create_world_cloud(selected_user,df):
#     if selected_user!="Overall":
#         df=df[df['user']==selected_user]
#
#     wc=WorldCloud(width=500,height=500,min_font_size=10,background_color='white')
#     df_wc=wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc
def common_words(selected_user,df):
    f = open('Stop_words.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp_df = df[df['user'] != 'notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']
    words = []
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    common_df=pd.DataFrame(Counter(words).most_common(20))
    return common_df
def working_Emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Create an empty list to store the emojis
    emojis = []

    # Iterate over the messages in the 'message' column and extract the emojis
    for message in df['message']:
        # Use the demojize function to convert any emojis in the message to their textual representation
        message_with_emojis = emoji.demojize(message)
        # Split the message by whitespace to get the individual words
        words = message_with_emojis.split()
        # Iterate over the words and append any emojis to the 'emojis' list
        for word in words:
            if word.startswith(':') and word.endswith(':'):
                emojis.append(word)

    # Use the Counter function from the collections module to count the frequency of each emoji
    emoji_freq = Counter(emojis)
    emoji_Emojis = []
    emoji_Counter = []
    # Print the top 10 emojis by frequency
    for emoje, freq in emoji_freq.most_common(10):
        print(f"{emoji.emojize(emoje)}: {freq}")
        emoji_Emojis.append(emoji.emojize(emoje))
        emoji_Counter.append(freq)
    d = {'Emojis': emoji_Emojis, 'Counter': emoji_Counter}
    emoji_df = pd.DataFrame(data=d)
    return emoji_df
def monthly_activenes(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daily_activeness(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('new_date').count()['message'].reset_index()
    return daily_timeline
def weekly_activeness(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def monthly_active(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def heatmapping(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap