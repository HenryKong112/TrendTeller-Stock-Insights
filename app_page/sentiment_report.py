import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def main():
    # Set the title of the Streamlit application
    st.title('TrendTeller: Sentiment and Stock Price Correlation Analysis')
    
    # Create a sidebar for user inputs regarding news and stock tickers
    st.sidebar.header("User Inputs")
    search_query = st.sidebar.text_input("Enter the news search query:", value="Trump")
    stocktwit_ticker = st.sidebar.text_input("Enter the StockTwits ticker:", value="DJT")
    stock_ticker = st.sidebar.text_input("Enter the stock ticker for price data:", value="DJT")
    
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('dataset/TrendTeller.db')
    
    # Load news data from the database based on user input
    try:
        news_df = pd.read_sql_query("SELECT * FROM News WHERE search_query = ?", conn, params=(search_query,))
    except Exception as e:
        st.warning(f"News query failed: {e}")
    
    # Load StockTwits comments data based on user input
    try:
        stocktwits_df = pd.read_sql_query("SELECT * FROM Stocktwits_Comments WHERE Ticker = ?", conn, params=(stocktwit_ticker,))
    except Exception as e:
        st.warning(f"StockTwits query failed: {e}")
    
    # Load stock price data from a CSV file
    try:
        stock_df = pd.read_csv(f'dataset/stock/{stock_ticker}_stock_price.csv')
    except Exception as e:
        st.warning(f"Stock price data could not be loaded: {e}")
    
    # Convert 'Date' columns in the dataframes to datetime format for analysis
    news_df['Date'] = pd.to_datetime(news_df['Date'])
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stocktwits_df['date'] = pd.to_datetime(stocktwits_df['date'])  # Ensure date column is datetime
    
    # Calculate average sentiment grouped by date for news data
    daily_news_sentiment = news_df.groupby('Date')['sentiment'].mean().reset_index()
    
    # Calculate average sentiment grouped by date for StockTwits data
    daily_twits_sentiment = stocktwits_df.groupby('date')['sentiment'].mean().reset_index()
    
    # Standardize the column name for merging
    daily_twits_sentiment.rename(columns={'date': 'Date'}, inplace=True)
    
    # Merge the sentiment dataframes with stock price dataframes
    news_stock_df = pd.merge(daily_news_sentiment, stock_df, on='Date', how='inner')
    twits_stock_df = pd.merge(daily_twits_sentiment, stock_df, on='Date', how='inner')
    twits_news_df = pd.merge(daily_twits_sentiment, daily_news_sentiment, on='Date', how='inner', suffixes=('_twits', '_news'))
    
    # Calculate correlations between sentiments and stock prices
    twits_stock_corr = twits_stock_df['sentiment'].corr(twits_stock_df['Adj Close'])
    twits_news_corr = twits_news_df['sentiment_twits'].corr(twits_news_df['sentiment_news'])
    news_stock_corr = news_stock_df['sentiment'].corr(news_stock_df['Adj Close'])
    news_volume_corr = news_stock_df['sentiment'].corr(news_stock_df['Volume'])
    twits_volume_corr = twits_stock_df['sentiment'].corr(twits_stock_df['Volume'])
    
    # Display correlation results in an expandable section
    with st.expander('Correlation Results'):
        st.write(f'Correlation between StockTwits sentiment and stock price: {twits_stock_corr:.4f}')
        st.write(f'Correlation between StockTwits sentiment and news sentiment: {twits_news_corr:.4f}')
        st.write(f'Correlation between news sentiment and stock price: {news_stock_corr:.4f}')
        st.write(f'Correlation between news sentiment and stock volume: {news_volume_corr:.4f}')
        st.write(f'Correlation between StockTwits sentiment and stock volume: {twits_volume_corr:.4f}')
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Sentiment and Stock Price", "Sentiment Correlations", "Volume Correlations"])

    with tab1:
        st.subheader('Sentiment and Stock Price Over Time')
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot Stock Price on primary y-axis
        ax1.plot(stock_df['Date'], stock_df['Adj Close'], color='green', marker='o', label='Adjusted Close Price')
        ax1.set_ylabel('Adjusted Close Price', color='green')  # Label for left y-axis
        ax1.tick_params(axis='y', labelcolor='green')

        # Create a secondary y-axis for sentiment
        ax2 = ax1.twinx()  # Instantiate a second axes that shares the same x-axis

        # Plot News Sentiment on the secondary y-axis
        ax2.plot(news_stock_df['Date'], news_stock_df['sentiment'], color='blue', marker='o', linestyle=':', label='News Sentiment')

        # Plot StockTwits Sentiment on the secondary y-axis
        ax2.plot(twits_stock_df['Date'], twits_stock_df['sentiment'], color='orange', marker='o', linestyle=':', label='StockTwits Sentiment')

        # Set titles and labels
        ax1.set_title('Sentiment and Stock Price Over Time')
        ax1.set_xlabel('Date')
        ax2.set_ylabel('Sentiment Score', color='blue')  # Label for right y-axis
        ax2.tick_params(axis='y', labelcolor='blue')  # Color for the right y-axis ticks

        # Rotate x-axis labels for better readability
        ax1.set_xticks(stock_df['Date'])  # Set x-ticks to dates
        ax1.set_xticklabels(stock_df['Date'].dt.strftime('%Y-%m-%d'), rotation=45)  # Rotate x-ticks

        # Add legends for both axes
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Add grid lines to the primary y-axis
        ax1.grid(True)

        st.pyplot(fig)

    with tab2:
        st.subheader('Scatter Plot: Sentiment vs Stock Price')
        col1, col2 = st.columns(2)

        with col1:
            plt.figure(figsize=(6, 4))
            # Scatter plot for StockTwits Sentiment vs Stock Price with regression line
            plt.scatter(twits_stock_df['sentiment'], twits_stock_df['Adj Close'], alpha=0.5, color='red')
            z = np.polyfit(twits_stock_df['sentiment'], twits_stock_df['Adj Close'], 1)
            p = np.poly1d(z)
            plt.plot(twits_stock_df['sentiment'], p(twits_stock_df['sentiment']), color='black', linestyle='--')

            # Set titles and labels
            plt.title('StockTwits Sentiment vs Stock Price')
            plt.xlabel('StockTwits Sentiment')
            plt.ylabel('Adjusted Close Price')
            plt.grid(True)
            st.pyplot(plt)

        with col2:
            plt.figure(figsize=(6, 4))
            # Scatter plot for News Sentiment vs Stock Price with regression line
            plt.scatter(news_stock_df['sentiment'], news_stock_df['Adj Close'], alpha=0.5, color='blue')
            z = np.polyfit(news_stock_df['sentiment'], news_stock_df['Adj Close'], 1)
            p = np.poly1d(z)
            plt.plot(news_stock_df['sentiment'], p(news_stock_df['sentiment']), color='black', linestyle='--')

            # Set titles and labels
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
            # Scatter plot for StockTwits Sentiment vs Stock Volume with regression line
            plt.scatter(twits_stock_df['sentiment'], twits_stock_df['Volume'], alpha=0.5, color='red')
            z = np.polyfit(twits_stock_df['sentiment'], twits_stock_df['Volume'], 1)
            p = np.poly1d(z)
            plt.plot(twits_stock_df['sentiment'], p(twits_stock_df['sentiment']), color='black', linestyle='--')

            # Set titles and labels
            plt.title('StockTwits Sentiment vs Stock Volume')
            plt.xlabel('StockTwits Sentiment')
            plt.ylabel('Stock Volume')
            plt.grid(True)
            st.pyplot(plt)

        with col2:
            plt.figure(figsize=(6, 4))
            # Scatter plot for News Sentiment vs Stock Volume with regression line
            plt.scatter(news_stock_df['sentiment'], news_stock_df['Volume'], alpha=0.5, color='blue')
            z = np.polyfit(news_stock_df['sentiment'], news_stock_df['Volume'], 1)
            p = np.poly1d(z)
            plt.plot(news_stock_df['sentiment'], p(news_stock_df['sentiment']), color='black', linestyle='--')

            # Set titles and labels
            plt.title('News Sentiment vs Stock Volume')
            plt.xlabel('News Sentiment')
            plt.ylabel('Stock Volume')
            plt.grid(True)
            st.pyplot(plt)

    # Close the database connection to free resources
    conn.close()

if __name__ == "__main__":
    main()

    
    