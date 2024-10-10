import sqlite3
import pandas as pd
import os

def db():
    # Connect to the SQLite database
    conn = sqlite3.connect('dataset/TrendTeller.db')
    cursor = conn.cursor()
    
    # Create the Stocktwits_Comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stocktwits_Comments (
        Username VARCHAR(256),
        Comment TEXT,
        date DATE,
        sentiment INT,
        Ticker VARCHAR(256),
        PRIMARY KEY (Username, Comment) 
        );
    """)
    
    # Create the News table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS News (
        "News Title" TEXT,
        Date DATE,
        Source VARCHAR(256),
        URL TEXT,
        sentiment INT,
        search_query VARCHAR(256),
        PRIMARY KEY (URL) 
        );    
    """)
    
    conn.commit()
    
    # Function to insert or update CSV file data into the database
    def insert_or_update_csv_to_db(data_table, csv_file):
        # Load the CSV data into a pandas DataFrame
        data = pd.read_csv(csv_file)
    
        # Handle Stocktwits_Comments table
        if data_table == 'Stocktwits_Comments':
            for index, row in data.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO Stocktwits_Comments (Username, Comment, date, sentiment, Ticker)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['Username'], row['Comment'], row['date'], row['sentiment'], row['Ticker']))
        
        # Handle News table
        elif data_table == 'News':
            for index, row in data.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO News ("News Title", Date, Source, URL, sentiment, search_query)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['News Title'], row['Date'], row['Source'], row['URL'], row['sentiment'], row['search_query']))
    
        conn.commit()
        print(f"File '{csv_file}' processed: inserted or updated records.")
    
    # Function to insert or update CSV files from a folder into the database
    def insert_or_update_csv_in_folder(data_table, foldername):
        # Directory containing the CSV files
        csv_folder = f'dataset/{foldername}'
    
        # Loop through all CSV files in the folder
        for file_name in os.listdir(csv_folder):
            if file_name.endswith('.csv'):
                file_path = os.path.join(csv_folder, file_name)
                insert_or_update_csv_to_db(data_table, file_path)
    
    # Process Stocktwits comments
    insert_or_update_csv_in_folder('Stocktwits_Comments', 'comments')
    
    # Process News articles
    insert_or_update_csv_in_folder('News', 'news')
    
    # Close the database connection
    conn.close()
    