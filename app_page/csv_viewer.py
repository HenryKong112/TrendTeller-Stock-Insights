import os
import pandas as pd
import streamlit as st

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
            
            st.markdown('---')
    else:
        st.warning(f"No CSV files found in the {foldername} folder.")

def main():
    st.title("CSV Viewer")
    st.write("You can view the CSV files containing the collected news and comments here."
             " The average sentiment value is also calculated for relevant datasets.")
    
    # Display the folders and their content with individual checkboxes for showing/hiding
    folder('news')     # View and process CSVs from 'news' folder
    folder('comments') # View and process CSVs from 'comments' folder
    folder('stock')    # View CSVs from 'stock' folder, but no sentiment calculation

if __name__ == "__main__":
    main()





