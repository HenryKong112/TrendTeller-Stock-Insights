import gensim
import matplotlib.pyplot as plt
import nltk
import os
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models
import streamlit as st
from gensim import corpora
from nltk.corpus import stopwords
from wordcloud import WordCloud

# Download NLTK stopwords only once
nltk.download('stopwords')

# Define stop words globally to avoid redundant definitions
stop_words = set(stopwords.words('english'))  # Set of English stop words

# Function to load data from a specified file path
def load_data(file_path):
    """Loads CSV data from the specified file path."""
    return pd.read_csv(file_path)  # Load the CSV file into a DataFrame

# Function to tokenize text data and remove stopwords
def tokenize_and_clean(df, column):
    """Tokenizes text in the specified column of the DataFrame and removes stopwords."""
    # Apply tokenization and stopword removal
    df[f'Tokenized_{column}'] = df[column].apply(
        lambda x: [word for word in x.split() if word.lower() not in stop_words]
    )
    return df  # Return updated DataFrame with tokenized column

# Function to create dictionary and corpus for LDA
def create_dictionary_corpus(df, token_column, no_below=5, no_above=0.5):
    """Creates a dictionary and a corpus for LDA topic modeling."""
    dictionary = corpora.Dictionary(df[token_column])  # Create a dictionary from tokenized data
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)  # Filter extremes based on frequency
    corpus = [dictionary.doc2bow(comment) for comment in df[token_column]]  # Create a corpus for LDA
    return dictionary, corpus  # Return both dictionary and corpus

# Function to build LDA model
def build_lda_model(corpus, dictionary, num_topics=5, chunksize=100, passes=10, alpha='auto', eta='auto'):
    """Builds an LDA model using the provided corpus and dictionary."""
    lda_model = gensim.models.LdaModel(
        corpus=corpus, 
        id2word=dictionary, 
        num_topics=num_topics, 
        random_state=100, 
        update_every=1, 
        chunksize=chunksize, 
        passes=passes, 
        alpha=alpha, 
        eta=eta,
        per_word_topics=True  # Track topics for each word in the model
    )
    return lda_model  # Return the built LDA model

# Function to print topics from LDA model
def print_topics(lda_model, num_topics):
    """Prints the top words for each topic in the LDA model."""
    topics = []
    for idx, topic in lda_model.print_topics(num_topics):
        topics.append(f'Topic: {idx+1} \nWords: {topic}')  # Format topic output
    return topics  # Return formatted list of topics

# Function to visualize word clouds for topics
def visualize_word_clouds(lda_model, num_topics):
    """Generates and displays word clouds for each topic in the LDA model."""
    st.subheader("Word Cloud for Topics")  # Add subheader in Streamlit app
    for i in range(num_topics):
        plt.figure()  # Create a new figure for each topic
        plt.imshow(WordCloud(background_color='white').fit_words(dict(lda_model.show_topic(i, 200))))  # Generate word cloud
        plt.axis('off')  # Hide axes for better visualization
        plt.title(f'Topic {i+1}')  # Set title for the word cloud
        st.pyplot(plt)  # Display the word cloud in the Streamlit app

def lda_workflow():
    """Main function for the LDA topic modeling Streamlit app."""
    st.title("Topic Modeling LDA Analysis")  # Set title for the app

    # List CSV files in both 'dataset/news' and 'dataset/comments' folders
    news_folder = 'dataset/news'
    comments_folder = 'dataset/comments'

    news_csv_files = [f"news/{f}" for f in os.listdir(news_folder) if f.endswith('.csv')]  # Get list of CSV files from 'news'
    comments_csv_files = [f"comments/{f}" for f in os.listdir(comments_folder) if f.endswith('.csv')]  # Get list of CSV files from 'comments'

    # Combine both lists of CSV files
    csv_files = news_csv_files + comments_csv_files

    if csv_files:  # Check if there are CSV files available
        selected_file = st.selectbox("Select a CSV file to analyze", csv_files)  # File selection dropdown

        # Determine the correct folder based on the selection
        if selected_file.startswith("news/"):
            file_path = os.path.join(news_folder, selected_file.split("news/")[1])
            text_column = "News Title"  # Automatically set the text column to "News Title"
        elif selected_file.startswith("comments/"):
            file_path = os.path.join(comments_folder, selected_file.split("comments/")[1])
            text_column = "Comment"  # Automatically set the text column to "Comment"

        # Load the selected CSV file
        df = load_data(file_path)  # Load data into DataFrame

        # LDA parameters input
        with st.expander("Adjust LDA Parameters", expanded=False):  # Expandable section
            num_topics = st.slider("Number of Topics", min_value=2, max_value=20, value=5)  # Select number of topics
            no_below = st.slider("Filter out tokens that appear in less than this number of documents", min_value=1, max_value=20, value=5)  # Set minimum document frequency
            no_above = st.slider("Filter out tokens that appear in more than this fraction of documents", min_value=0.1, max_value=1.0, value=0.5)  # Set maximum document frequency
            chunksize = st.slider("Chunk Size", min_value=50, max_value=500, value=100)  # Set chunk size for processing
            passes = st.slider("Number of Passes", min_value=5, max_value=20, value=10)  # Set number of training passes

        if st.button("Run LDA"):  # Button to run the LDA analysis
            # Tokenize and clean data
            df = tokenize_and_clean(df, text_column)  # Perform tokenization and stopword removal

            # Create dictionary and corpus
            dictionary, corpus = create_dictionary_corpus(df, f'Tokenized_{text_column}', no_below=no_below, no_above=no_above)  # Create inputs for LDA

            # Build LDA model
            lda_model = build_lda_model(corpus, dictionary, num_topics=num_topics, chunksize=chunksize, passes=passes)  # Build the LDA model

            # Print topics
            st.subheader("LDA Topics")  # Add subheader for displaying topics
            topics = print_topics(lda_model, num_topics)  # Retrieve topics from the model
            for topic in topics:  # Display topics in the Streamlit app
                st.write(topic)

            # Visualize word clouds for each topic
            visualize_word_clouds(lda_model, num_topics)  # Generate and display word clouds

    else:
        st.warning("No CSV files found in the 'dataset/news' or 'dataset/comments' folder.")  # Warning if no CSV files available


if __name__ == "__main__":
    lda_workflow()  # Run the main LDA workflow function






