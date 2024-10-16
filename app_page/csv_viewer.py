import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load CSV data from a specified file path."""
    return pd.read_csv(file_path)

def folder(foldername):
    """List CSV files in the 'dataset/{foldername}' folder, allow selection, load, display the file, and calculate average sentiment."""
    dataset_folder = f'dataset/{foldername}'
    csv_files = [f for f in os.listdir(dataset_folder) if f.endswith('.csv')]

    if csv_files:
        selected_file = st.selectbox(f"View {foldername}: ", csv_files, key=f"{foldername}_selectbox")

        # Use a checkbox to toggle the table visibility
        show_table = st.checkbox(f"Show {foldername} table", value=True, key=f"{foldername}_checkbox")

        # Load the selected CSV file
        file_path = os.path.join(dataset_folder, selected_file)
        df = load_data(file_path)

        # Display the DataFrame in the Streamlit app if the checkbox is checked
        if show_table:
            st.write(df)

            # Try calculating average sentiment, if the 'sentiment' column exists
            if foldername != 'stock':  # We are not calculating sentiment for 'stock'
                if 'sentiment' in df.columns:
                    average_value = df['sentiment'].mean().__round__(3)
                    st.write("Average value of sentiment: ", average_value)

                    # Create a pie chart for sentiment distribution
                    sentiment_counts = df['sentiment'].value_counts()
                    sentiment_labels = [f"{label} ({count/sum(sentiment_counts)*100:.1f}%)" 
                                        for label, count in zip(sentiment_counts.index, sentiment_counts)]

                    fig, ax = plt.subplots()

                    # Create the pie chart without showing percentages on the pie itself
                    wedges, _ = ax.pie(sentiment_counts, startangle=90)

                    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

                    # Add a legend with percentages
                    ax.legend(wedges, sentiment_labels, title="Sentiment", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

                    st.pyplot(fig)
            
            st.markdown('---')
    else:
        st.warning(f"No CSV files found in the {foldername} folder.")

def main():
    st.title("CSV Viewer")
    st.write("Explore CSV files with collected news, comments, and stock data. For relevant datasets, the average sentiment value is calculated and displayed. Additionally, a pie chart illustrates the sentiment distribution.")

    # Display with background color and emoji
    st.markdown("""
    <div style="background-color: #f9f7d9; padding: 10px; border-radius: 5px; font-size: 18px;">
        ❗️ <b>Sentiment:</b> 1 (most negative) -- 5 (most positive)
    </div>
    """, unsafe_allow_html=True)
    
    # Display the folders and their content with individual checkboxes for showing/hiding
    folder('news')     # View and process CSVs from 'news' folder
    folder('comments') # View and process CSVs from 'comments' folder
    folder('stock')    # View CSVs from 'stock' folder, but no sentiment calculation

if __name__ == "__main__":
    main()







