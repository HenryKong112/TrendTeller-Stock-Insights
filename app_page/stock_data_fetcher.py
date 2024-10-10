import os
from datetime import date
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

def main():
    st.title("Stock Data Fetcher")  # Set the app title

    # User input for stock ticker symbol
    ticker = st.text_input("Enter the stock ticker", "").strip()

    # Date inputs for the start and end dates
    start_date = st.date_input("Start date", value=date(2024, 10, 3))  # Default start date
    end_date = st.date_input("End date", value=date(2024, 10, 4))  # Default end date

    # Check if the start date is after the end date and display an error if so
    if start_date > end_date:
        st.error("End date must be after the start date.")
        return

    # When the user clicks the download button
    if st.button("View & Download Stock Data"):
        if ticker:  # Check if the user has entered a stock ticker symbol
            # Download stock data from Yahoo Finance for the specified ticker and date range
            stock_data = yf.download(ticker, start=start_date, end=end_date)

            if not stock_data.empty:  # Check if any data was returned
                # Display the stock data in the app
                st.write(stock_data)
                
                # Create a candlestick chart
                fig = go.Figure(data=[go.Candlestick(
                    x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],
                    name="Candlesticks",
                    increasing_line_color='green',  # Color for increasing prices
                    decreasing_line_color='red'      # Color for decreasing prices
                )])

                # Add a simple moving average (e.g., 5-day)
                stock_data['SMA_5'] = stock_data['Close'].rolling(window=5).mean()
                fig.add_trace(go.Scatter(
                    x=stock_data.index,
                    y=stock_data['SMA_5'],
                    mode='lines',
                    name='5-Day SMA',
                    line=dict(color='blue', width=1.5)
                ))

                # Set chart layout and title
                fig.update_layout(
                    title=f"{ticker} - Candlestick Chart",
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False,
                    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the paper
                    font=dict(color='white'),  # Change font color to white
                    width=800,
                    height=600
                )

                # Customize axes
                fig.update_xaxes(showgrid=True, gridcolor='gray')
                fig.update_yaxes(showgrid=True, gridcolor='gray')

                # Display the chart using Streamlit
                st.write(fig)
                
                # Specify the dataset folder and create it if it doesn't exist
                dataset_folder = 'dataset/stock'
                os.makedirs(dataset_folder, exist_ok=True)

                # Save the CSV file directly to the dataset folder
                csv_filename = os.path.join(dataset_folder, f'{ticker}_stock_price.csv')
                stock_data.to_csv(csv_filename, index=True)

                # Inform the user that the data has been saved
                st.success(f"Data saved to {csv_filename}")
            else:
                # Display a warning if no stock data was found for the specified date range
                st.warning("No data found for the given stock ticker and date range.")
        else:
            # Display a warning if no stock ticker symbol was entered
            st.warning("Please enter a valid stock ticker symbol.")

if __name__ == "__main__":
    main()  # Run the main function to start the app






