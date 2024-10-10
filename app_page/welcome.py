import streamlit as st

def main():

    # Title Section
    st.title("Welcome to **TrendTeller Stock Insights**! 👋")

    # Program Purpose Section
    st.markdown("""
        <div style='background-color:#f9f9f9;padding:20px;border-radius:10px;text-align:left'>
            <h2 style='color:#1e90ff;text-align:center'>🌟 Discover Market Sentiment with Ease! 🌟</h2>
            <p style='color:#333'>
                This application seamlessly integrates sentiment analysis, topic modeling, and correlation analysis with interactive data visualizations in a single, intuitive dashboard. By analyzing sentiment from both news headlines and StockTwits comments, it uncovers hidden trends and their correlations with stock prices and trading volumes.
                Through a user-friendly interface, the dashboard provides real-time visualizations that not only reveal sentiment trends but also highlight the relationship between public opinion and stock market performance. Whether you’re an investor, analyst, or researcher, this tool empowers you with a data-driven approach to understanding the forces shaping the financial landscape, making it easier to make informed decisions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Key Features Section
    st.markdown("""
        <div style='background-color:#e6e6fa;padding:20px;border-radius:10px;margin-top:20px'>
            <h3 style='color:#8a2be2'>🚀 Key Features:</h3>
            <ul style='color:#00008b'>
                <li>🔍 <strong>Sentiment Analysis:</strong> Understand public sentiment on news and StockTwits comments.</li>
                <li>📊 <strong>Topic Modeling (LDA):</strong> Identify key themes and ongoing discussions.</li>
                <li>🌈 <strong>Data Visualization:</strong> Visualize both topics and sentiment trends in a clear, interactive way.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("""
        <div style='background-color:#fffacd;padding:20px;border-radius:10px;margin-top:20px'>
            <h3 style='color:#ff6347'>🔎 How It Works:</h3>
            <h4 style='color:#4682b4'>📱 App Modules:</h4>
            <ol style='color:#2f4f4f'>
                <li>**CSV Viewer:** Easily browse news, comments, and stock price data.</li>
                <li>**News Scraper Sentiment Analysis:** Scrape and analyze sentiment from news headlines.</li>
                <li>**Stock Data Fetcher:** Fetch stock price data for specific tickers.</li>
                <li>**StockTwits Comment Sentiment Analysis:** Analyze sentiment on StockTwits comments from a CSV file.</li>
                <li>**Topic Modeling LDA Analysis:** Run LDA to identify key topics and trends.</li>
                <li>**Report:** Visualization of sentiment trends and the correlation between sentiment, stock prices, and trading volumes.
            </ol>
        </div>
    """, unsafe_allow_html=True)

    # Displaying Image
    st.image("image/workflow.png", caption="Workflow Overview")

    # Button for Database Update
    st.markdown("""
        <div style='background-color:#f0fff0;padding:20px;border-radius:10px;margin-top:20px'>
            <h4 style='color:#ff4500'>⚙️ Update Database</h4>
            <p style='color:#006400'>
                <strong>Update Database:</strong> Automatically insert or update all CSV files in the 'news' and 'comments' folders into the database.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

