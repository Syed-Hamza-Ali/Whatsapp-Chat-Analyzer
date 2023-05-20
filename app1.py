import streamlit as st
import preprocess1, helper1
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    #st.text(data)
    df=preprocess1.preprocess(data)
    #st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user=st.sidebar.selectbox("Show Analysis w.r.t",user_list)
    # Stats
    if st.sidebar.button("Show Analysis"):
        total_messages,total_words,media_shared,link_share=helper1.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total Words Used")
            st.title(total_words)
        with col3:
            st.header("Total Media Shared")
            st.title(media_shared)
        with col4:
            st.header("Total Links Shared")
            st.title(link_share)
        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper1.monthly_activenes(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper1.daily_activeness(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['new_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Weekly Activeness
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Weekly Activity")
            week_act=helper1.weekly_activeness(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(week_act.index,week_act.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Monthly Activity")
            month_act=helper1.monthly_active(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(month_act.index,month_act.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_activity=helper1.heatmapping(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_activity)
        st.pyplot(fig)

        if selected_user=='Overall':
            st.title("Most Active Users")
            x,active_df=helper1.most_actie_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                st.dataframe(active_df)
            with col2:
                ax.bar(x.index, x.values,color='crimson')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        # # Word_Cloud
        # st.title("Word Cloud")
        # df_wc=helper1.create_world_cloud(selected_user,df)
        # fig,ax=plt.subplots()
        # ax.inshow(df_wc)
        # st.pyplot(fig)

        #Common_words
        common_df=helper1.common_words(selected_user,df)

        fig,ax=plt.subplots()

        ax.barh(common_df[0],common_df[1],color='darkcyan')
        plt.xticks(rotation='vertical')

        st.title("Most Commonly Used Words")
        st.pyplot(fig)
        #emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper1.working_Emojis(selected_user, df)
        fig, ax = plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            st.table(emoji_df)
        with col2:
            #st.header("Most Commonly Used Emojis")
            ax.pie(emoji_df['Counter'],labels=emoji_df['Emojis'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
