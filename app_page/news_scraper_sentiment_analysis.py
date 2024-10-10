import os
import re
import time
from datetime import date
import pandas as pd
import streamlit as st
import spacy
import torch
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def lemmatize_title(title):
    """Lemmatizes the given title by removing special characters and applying lemmatization."""
    title = re.sub(r'[^A-Za-z0-9\s]+', '', title)  # Remove special characters
    title = title.lower()  # Convert to lowercase
    doc = nlp(title)  # Process the title using spaCy
    return ' '.join([token.lemma_ for token in doc])  # Return lemmatized title as a string

def sentiment_score(title):
    """Calculates the sentiment score of the given title using a pre-trained model."""
    tokens = tokenizer.encode(title, return_tensors='pt')  # Tokenize the title
    result = model(tokens)  # Get the model's prediction
    return int(torch.argmax(result.logits)) + 1  # Return the sentiment score (1-5)

def main():
    """Main function to run the Streamlit app for scraping news and analyzing sentiment."""
    global nlp, tokenizer, model
    # Load spaCy model and transformers for sentiment analysis
    nlp = spacy.load('en_core_web_sm')  # Load spaCy's English language model
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')  # Load the tokenizer
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')  # Load the sentiment analysis model

    # Streamlit UI setup
    st.title("News Scraper Sentiment Analysis")  # Set the title of the Streamlit app
    st.write("Retrieve news headlines based on your search query from the past 24 hours.")
    search = st.text_input("Enter what you'd like to search for on Google News", "")  # Input field for search query
    num_news = st.slider("Number of News", min_value=1, max_value=500, value=200) # Select number of news
    
    # Check if the "Scrape and Analyze" button is clicked
    if st.button('Scrape and Analyze'):
        if not search:  # If no search term is provided
            st.warning("Please enter a search term.")  # Display warning
            return

        # Lists to store news details
        news_titles_list = []  # Initialize list to store news titles
        news_sources_list = []  # Initialize list to store news sources
        news_urls_list = []  # Initialize list to store news URLs
        today = date.today()  # Get today's date

        # Loop to fetch news results from Google in batches of 10 (to simulate pagination)
        for start in range(0, num_news, 10):
            # Google News search query with parameters:
            # - q: search term
            # - start: pagination (batch of 10 results)
            # - tbm: type of search (news)
            # - tbs: filter by time (last 24 hours)
            link = f"https://www.google.com/search?q={search.replace(' ', '+')}&start={start}&tbm=nws&tbs=qdr:d"
            req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})  # Set user-agent to avoid being blocked

            try:
                # Fetch and parse the webpage
                webpage = urlopen(req).read()  # Fetch the webpage
                soup = BeautifulSoup(webpage, 'html5lib')  # Parse the webpage using BeautifulSoup

                # Extract news sources
                for news_source in soup.find_all('div', attrs={'class': 'BNeawe UPmit AP7Wnd lRVwie'}):
                    news_sources_list.append(news_source.text)

                # Extract news titles
                for news_title in soup.find_all('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}):
                    news_titles_list.append(news_title.text)

                # Extract news URLs
                for div_tag in soup.find_all('div', class_='Gx5Zad'):
                    a_tag = div_tag.find('a', href=True)
                    if a_tag:
                        url = a_tag['href']
                        if 'url?q=' in url:
                            clean_url = url.split('url?q=')[1].split('&')[0]  # Clean the URL
                            news_urls_list.append(clean_url)

                time.sleep(2)  # Pause between requests to avoid overwhelming the server

            except Exception as e:
                st.error(f"Error fetching page {start}: {e}")  # Display an error message if fetching fails

        # Check if news articles were found
        if news_titles_list:
            # Create a dictionary of news data
            data = {
                'News Title': news_titles_list,  # Store news titles
                'Date': [today] * len(news_titles_list),  # Store today's date for all titles
                'Source': news_sources_list,  # Store news sources
                'URL': news_urls_list  # Store news URLs
            }

            # Convert dictionary into a DataFrame
            df = pd.DataFrame(data)
            df.dropna(inplace=True)  # Remove rows with missing values
            df.drop_duplicates(subset=['News Title', 'URL'], keep='first', inplace=True)  # Remove duplicate entries

            # Apply lemmatization to news titles
            df['News Title'] = df['News Title'].apply(lemmatize_title)

            # Calculate sentiment scores for each news title (limited to 512 characters)
            df['sentiment'] = df['News Title'].apply(lambda x: sentiment_score(x[:512]))

            df['search_query'] = search
            
            # Specify the dataset folder and create it if it doesn't exist
            dataset_folder = 'dataset/news'
            os.makedirs(dataset_folder, exist_ok=True)  # Create folder if it doesn't exist

            # Save the DataFrame as a CSV file in the dataset folder
            csv_filename = os.path.join(dataset_folder, f'{today}_{search}_news_data.csv')
            df.to_csv(csv_filename, index=False)  # Save to CSV

            # Notify the user that the data was saved
            st.success(f"Data saved to {csv_filename}")

            # Display the DataFrame in the app
            st.write(df)

        else:
            # If no news articles were found, display a warning
            st.warning("No news found for the given search.")

if __name__ == "__main__":
    main()  # Run the main function to start the app





