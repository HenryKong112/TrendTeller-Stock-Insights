import re
import spacy
import torch
import pandas as pd
from datetime import date
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import streamlit as st

# Load the SpaCy English language model
nlp = spacy.load('en_core_web_sm')

# Function to save uploaded CSV file
def save_uploaded_file(uploaded_file, stock_ticker):
    """Saves the uploaded CSV file with a timestamp and stock name in the dataset folder."""
    today = date.today()
    try:
        # Construct file path for saving the uploaded file
        file_path = f'dataset/comments/{today}_stocktwit_comment_{stock_ticker}.csv'
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())  # Write the contents of the uploaded file
        return file_path
    except Exception as e:
        st.error(f"An error occurred while saving the file: {e}")  # Error handling for file saving
        return None

def get_stock_comments(stock_ticker):
    """Fetches comments related to the stock from the uploaded CSV and processes them."""
    today = date.today()
    file_path = f'dataset/comments/{today}_stocktwit_comment_{stock_ticker}.csv'  # Construct file path
    
    try:
        # Load the dataset from the CSV file
        df = pd.read_csv(file_path)

        # Add today's date to the 'date' column for each entry
        df['date'] = today

        # Clean the comments using the cleaning function
        df['Comment'] = df['Comment'].apply(clean_comment)

        df['Ticker'] = stock_ticker
        
        # Remove rows where the 'Comment' column is empty after cleaning
        df = df[df['Comment'].str.strip() != '']

        # Remove duplicate rows based on 'Username' and 'Comment', keeping only the first occurrence
        df = df.drop_duplicates(subset=['Username', 'Comment'], keep='first')

        # Lemmatize cleaned comments to reduce words to their base form
        df['Comment'] = df['Comment'].apply(lemmatize_comment)

        # Load sentiment analysis model and tokenizer
        tokenizer, model = load_sentiment_model()

        # Apply sentiment analysis to the 'Comment' column
        df['sentiment'] = df['Comment'].apply(lambda x: get_sentiment_score(tokenizer, model, x))

        # Save the cleaned dataset back to the CSV file
        df.to_csv(file_path, index=False)
        
        st.success(f"Data saved to {file_path} ")  # Inform user of successful cleaning
        st.write(df)  # Display the cleaned dataset

    except FileNotFoundError:
        st.error("CSV file does not exist.")  # Handle case where the CSV file is not found
    except Exception as e:
        st.error(f"An error occurred: {e}")  # Handle other errors

def clean_comment(comment):
    """Cleans individual comments by removing unwanted characters."""
    comment = re.sub(r'@[A-Za-z0-9]+', '', comment)  # Remove @mentions
    comment = re.sub(r'#', '', comment)  # Remove hashtag symbols
    comment = re.sub(r'https?:\/\/\S+|www\S+', '', comment)  # Remove URLs
    comment = re.sub(r'\S*\.(com|org|gov|edu|net|news)\S*', '', comment)  # Remove common domain extensions
    comment = re.sub(r'\$\S+', '', comment)  # Remove stock symbols
    comment = re.sub(r'[^A-Za-z0-9\s]+', '', comment)  # Remove special characters
    comment = re.sub(r'\s+', ' ', comment)  # Normalize multiple spaces to a single space
    comment = comment.lower()  # Convert to lowercase
    return comment.strip()  # Return cleaned comment without leading/trailing spaces

def lemmatize_comment(comment):
    """Lemmatizes the cleaned comments to their base form."""
    doc = nlp(comment)  # Process comment using SpaCy
    return ' '.join([token.lemma_ for token in doc])  # Join lemmas into a single string

def load_sentiment_model():
    """Loads the sentiment analysis model and tokenizer from the transformers library."""
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')  # Load tokenizer
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')  # Load model
    return tokenizer, model  # Return both

def get_sentiment_score(tokenizer, model, comment):
    """Gets the sentiment score for a comment using the loaded model."""
    inputs = tokenizer.encode(comment, return_tensors='pt', truncation=True, max_length=512)  # Tokenize comment
    with torch.no_grad():
        outputs = model(inputs)  # Get model outputs without computing gradients
    return int(torch.argmax(outputs.logits)) + 1  # Return the sentiment score (1-5 scale)

def main():
    st.title("StockTwits Comment Sentiment Analysis")  # Set the title for the Streamlit app

    # Display informational markdown about StockTwits and instructions for using Bardeen AI 
    st.markdown(
        "Visit [Stocktwits](https://stocktwits.com/) and search for the stock you're interested in."
        " Use <span style='color:red;'>Bardeen AI</span> to retrieve comments.<br>"
        "Upload the CSV file below.",
        unsafe_allow_html=True
    )
    # A video tutorial on how to retrieve comments.
    st.markdown("*How to Use Bardeen AI:*")
    video_file = "video/BardeenAI_Stocktwits.mp4"
    # Display the video
    st.video(video_file)
    
    # File uploader for user to upload StockTwits comments CSV file
    uploaded_file = st.file_uploader("Upload your StockTwits comments CSV file", type=['csv'])
    stock_ticker = st.text_input("Enter the stock ticker")  # Input for stock ticker

    # Check if both file and stock ticker are provided
    if uploaded_file and stock_ticker:
        save_uploaded_file(uploaded_file, stock_ticker)  # Save the uploaded file
        get_stock_comments(stock_ticker)  # Process comments from the saved file
    else:
        st.warning("Please upload a file and enter a stock ticker.")  # Warning if inputs are missing

if __name__ == "__main__":
    main()  # Run the main function


