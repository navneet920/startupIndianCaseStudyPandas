import streamlit as st
import pandas as pd


st.set_page_config(layout='wide',page_title='StartUp Analysis')

df=pd.read_csv('statrup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month']=df['date'].dt.month

def load_overall_analysis():
    st.title("OverAll Analysis")

    col1,col2=st.columns(2)
    #total investment amount
    total=round(df['amount'].sum())
    #max funding
    max_amount=round(df.groupby('name')['amount'].max().sort_values(ascending=False).head(1).values[0].item())
    #average ticket size
    avg_funding=round(df.groupby('name')['amount'].sum().mean())
    #total funded stratups
    num_startups=df['name'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max Funding',str(max_amount)+' Cr')
    with col3:
        st.metric('Avg',str(avg_funding)+' Cr')
    with col4:
        st.metric('Funded StartUp',num_startups)
    st.header('Month on Month Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig5,ax5=plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig5)



def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    recent5_df=df[df['investors'].str.contains(investor)].head()[['date','name','Vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(recent5_df)

    col1,col2=st.columns(2)
    with col1:
        #load Biggest  Investment
        big_series=df[df['investors'].str.contains(investor)].groupby('name')['amount'].sum().sort_values(ascending=False).head()
        st.subheader("Biggest  Investment")
        #st.dataframe(big_df)
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('Vertical')['amount'].sum()
        st.subheader('Sector Invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    col3,col4=st.columns(2)
    with col3:
        round_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)


    yoy_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('year on year Investments')
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_series.index, yoy_series.values)
    st.pyplot(fig4)


def load_startup_details(startup):
    st.title(startup)
    #load the recent 5 startup in india




st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    # btn0=st.sidebar.button("Show Overall Analysis")
    # if btn0:
    load_overall_analysis()
elif option=='Startup':
    st.sidebar.selectbox('Select startup',sorted(set(df['name'].str.split(',').sum())))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
    #st.title('Investor Analysis')