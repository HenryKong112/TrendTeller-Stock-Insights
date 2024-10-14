import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def main():
    # Set Streamlit page title
    st.title('TrendTeller: Sentiment and Stock Price Correlation Analysis')
    
    # Create a sidebar for user inputs
    st.sidebar.header("User Inputs")
    search_query = st.sidebar.text_input("Enter the news search query:", value="Trump")
    stocktwit_ticker = st.sidebar.text_input("Enter the StockTwits ticker:", value="DJT")
    stock_ticker = st.sidebar.text_input("Enter the stock ticker for price data:", value="DJT")
    
    # Connect to the SQLite database
    conn = sqlite3.connect('dataset/TrendTeller.db')
    
    # Load datasets from SQLite database with parameterized queries
    try:
        news_df = pd.read_sql_query("SELECT * FROM News WHERE search_query = ?", conn, params=(search_query,))
    except Exception as e:
        st.warning(f"News query failed: {e}")
    
    try:
        stocktwits_df = pd.read_sql_query("SELECT * FROM Stocktwits_Comments WHERE Ticker = ?", conn, params=(stocktwit_ticker,))
    except Exception as e:
        st.warning(f"StockTwits query failed: {e}")
    
    # Load stock data from CSV file
    try:
        stock_df = pd.read_csv(f'dataset/stock/{stock_ticker}_stock_price.csv')
    except Exception as e:
        st.warning(f"Stock price data could not be loaded: {e}")
    
    # Convert 'Date' columns to datetime format
    news_df['Date'] = pd.to_datetime(news_df['Date'])
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stocktwits_df['date'] = pd.to_datetime(stocktwits_df['date'])  # Use 'date' in stocktwits_df
    
    # Group by date and calculate average sentiment for news data
    daily_news_sentiment = news_df.groupby('Date')['sentiment'].mean().reset_index()
    
    # Group by date and calculate average sentiment for StockTwits data
    daily_twits_sentiment = stocktwits_df.groupby('date')['sentiment'].mean().reset_index()
    
    # Rename 'date' to 'Date' in StockTwits dataframe for consistency
    daily_twits_sentiment.rename(columns={'date': 'Date'}, inplace=True)
    
    # Merge dataframes
    news_stock_df = pd.merge(daily_news_sentiment, stock_df, on='Date', how='inner')
    twits_stock_df = pd.merge(daily_twits_sentiment, stock_df, on='Date', how='inner')
    twits_news_df = pd.merge(daily_twits_sentiment, daily_news_sentiment, on='Date', how='inner', suffixes=('_twits', '_news'))
    
    # Calculate correlations
    twits_stock_corr = twits_stock_df['sentiment'].corr(twits_stock_df['Adj Close'])
    twits_news_corr = twits_news_df['sentiment_twits'].corr(twits_news_df['sentiment_news'])
    news_stock_corr = news_stock_df['sentiment'].corr(news_stock_df['Adj Close'])
    news_volume_corr = news_stock_df['sentiment'].corr(news_stock_df['Volume'])
    twits_volume_corr = twits_stock_df['sentiment'].corr(twits_stock_df['Volume'])
    
    # Display correlations in an expander for a cleaner layout
    with st.expander('Correlation Results'):
        st.write(f'Correlation between StockTwits sentiment and stock price: {twits_stock_corr:.4f}')
        st.write(f'Correlation between StockTwits sentiment and news sentiment: {twits_news_corr:.4f}')
        st.write(f'Correlation between news sentiment and stock price: {news_stock_corr:.4f}')
        st.write(f'Correlation between news sentiment and stock volume: {news_volume_corr:.4f}')
        st.write(f'Correlation between StockTwits sentiment and stock volume: {twits_volume_corr:.4f}')
    
    # Use tabs for visualizations
    tab1, tab2, tab3 = st.tabs(["Sentiment and Stock Price", "Sentiment Correlations", "Volume Correlations"])

    with tab1:
        st.subheader('Sentiment and Stock Price Over Time')
        fig, ax1 = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

        # Plot 1: News Sentiment Over Time
        ax1[0].plot(news_stock_df['Date'], news_stock_df['sentiment'], color='blue', marker='o')
        ax1[0].set_title('News Sentiment Over Time')
        ax1[0].set_ylabel('News Sentiment')
        ax1[0].grid(True)

        # Plot 2: StockTwits Sentiment Over Time
        ax1[1].plot(twits_stock_df['Date'], twits_stock_df['sentiment'], color='orange', marker='o')
        ax1[1].set_title('StockTwits Sentiment Over Time')
        ax1[1].set_ylabel('StockTwits Sentiment')
        ax1[1].grid(True)

        # Plot 3: Stock Price Over Time
        ax1[2].plot(stock_df['Date'], stock_df['Adj Close'], color='green', marker='o')
        ax1[2].set_title('Stock Price Over Time')
        ax1[2].set_ylabel('Adjusted Close Price')
        ax1[2].set_xlabel('Date')
        ax1[2].grid(True)

        # Rotate the x-axis labels
        plt.setp(ax1[2].xaxis.get_majorticklabels(), rotation=45)
        
        st.pyplot(fig)

    with tab2:
        st.subheader('Scatter Plot: Sentiment vs Stock Price')
        col1, col2 = st.columns(2)

        with col1:
            plt.figure(figsize=(6, 4))
            plt.scatter(twits_stock_df['sentiment'], twits_stock_df['Adj Close'], alpha=0.5, color='red')
            plt.title('StockTwits Sentiment vs Stock Price')
            plt.xlabel('StockTwits Sentiment')
            plt.ylabel('Adjusted Close Price')
            plt.grid(True)
            st.pyplot(plt)

        with col2:
            plt.figure(figsize=(6, 4))
            plt.scatter(news_stock_df['sentiment'], news_stock_df['Adj Close'], alpha=0.5, color='blue')
            plt.title('News Sentiment vs Stock Price')
            plt.xlabel('News Sentiment')
            plt.ylabel('Adjusted Close Price')
            plt.grid(True)
            st.pyplot(plt)
    
    with tab3:
        st.subheader('Scatter Plot: Sentiment vs Stock Volume')
        col1, col2 = st.columns(2)

        with col1:
            plt.figure(figsize=(6, 4))
            plt.scatter(twits_stock_df['sentiment'], twits_stock_df['Volume'], alpha=0.5, color='red')
            plt.title('StockTwits Sentiment vs Stock Volume')
            plt.xlabel('StockTwits Sentiment')
            plt.ylabel('Stock Volume')
            plt.grid(True)
            st.pyplot(plt)

        with col2:
            plt.figure(figsize=(6, 4))
            plt.scatter(news_stock_df['sentiment'], news_stock_df['Volume'], alpha=0.5, color='blue')
            plt.title('News Sentiment vs Stock Volume')
            plt.xlabel('News Sentiment')
            plt.ylabel('Stock Volume')
            plt.grid(True)
            st.pyplot(plt)
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()

    
    