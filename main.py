import streamlit as st
from app_page.csv_viewer import main as csv_viewer_main
from app_page.news_scraper_sentiment_analysis import main as news_scraper_main
from app_page.stock_data_fetcher import main as stock_data_fetcher_main
from app_page.stocktwit_comment_sentiment_analysis import main as stocktwit_analysis_main
from app_page.topic_modeling_lda_analysis import lda_workflow
import dataset.database as db
import app_page.welcome as welcome
import app_page.sentiment_report as r

# Set the default page config
st.set_page_config(
    page_title="Welcome to TrendTeller Stock Insights",
    page_icon="👋",
    layout="wide",  # Adjust layout as needed
    initial_sidebar_state="expanded"
)

def main():
    # Set the title of the main Streamlit app
    st.title("TrendTeller Stock Insights")

    # Sidebar for selecting different app functionalities
    app_mode = st.sidebar.selectbox("Choose the app", 
                                      ["Welcome",   # Default welcome page
                                       "CSV Viewer", 
                                       "News Scraper Sentiment Analysis", 
                                       "Stock Data Fetcher", 
                                       "StockTwit Comment Sentiment Analysis", 
                                       "Topic Modeling LDA Analysis",
                                       "Sentiment Report"])

    if st.sidebar.button("Update Database"):
        db.db()  # Call the update_database function
        st.sidebar.success("Database updated successfully!")  # Success message

    # Display the welcome page first
    if app_mode == "Welcome":
        welcome.main()  # Call the welcome page

    # Display the selected app based on the user choice
    elif app_mode == "CSV Viewer":
        csv_viewer_main()  # Calls the main function of CSV Viewer
    elif app_mode == "News Scraper Sentiment Analysis":
        news_scraper_main()  # Calls the main function of News Scraper Sentiment Analysis
    elif app_mode == "Stock Data Fetcher":
        stock_data_fetcher_main()  # Calls the main function of Stock Data Fetcher
    elif app_mode == "StockTwit Comment Sentiment Analysis":
        stocktwit_analysis_main()  # Calls the main function of StockTwit Comment Sentiment Analysis
    elif app_mode == "Topic Modeling LDA Analysis":
        lda_workflow()  # Calls the LDA workflow function for Topic Modeling
    elif app_mode == "Sentiment Report":
        r.main()

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()







