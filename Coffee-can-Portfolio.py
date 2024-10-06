import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import time
from requests.exceptions import RequestException
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

# Set display options for Pandas
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-detect width
pd.set_option('display.max_colwidth', None)  # Show full column content

def get_roce_roe(ticker):
    finology_url = f'https://ticker.finology.in/company/{ticker[:-3]}'
    try:
        response = requests.get(finology_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        roce_divs = soup.find_all("div", class_="col-6 col-md-4 compess")
        
        roce = None
        roe = None
        
        if len(roce_divs) > 14:
            roce_div = roce_divs[14]
            roe_div = roce_divs[13]
            
            roce_span = roce_div.find('span', class_='Number')
            roe_span = roe_div.find('span', class_='Number')
            
            roce = float(roce_span.text.strip()) if roce_span else None
            roe = float(roe_span.text.strip()) if roe_span else None
        
        return roce, roe
    except RequestException as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None

def get_loan_growth(ticker):
    try:
        company = yf.Ticker(ticker)
        balance_sheet = company.balance_sheet
        
        if 'Total Debt' in balance_sheet.index:
            loans = balance_sheet.loc['Total Debt']
            if len(loans) >= 2:
                previous_loan = loans.iloc[1]
                current_loan = loans.iloc[0]
                if previous_loan != 0:
                    return ((current_loan - previous_loan) / previous_loan) * 100
                else:
                    return 0 if current_loan == 0 else float('inf')
        return None
    except Exception as e:
        print(f"Error calculating loan growth for {ticker}: {e}")
        return None

def process_data(tickers, output_text):
    all_data = []
    batch_output = ""
    last_update_time = time.time()

    for ticker in tickers:
        batch_output += f"Processing {ticker}...\n"
        
        data = {'Ticker': ticker}
        
        roce, roe = get_roce_roe(ticker)
        data['ROCE'] = roce
        data['ROE'] = roe
        
        data['Loan Growth'] = get_loan_growth(ticker)
        
        all_data.append(data)
        
        # Create a DataFrame from the collected data so far
        df = pd.DataFrame(all_data)
        
        # Prepare the output for this ticker
        batch_output += "Full Data:\n"
        batch_output += f"{df}\n\n"
        
        # Filter stocks fit for a Coffee Can Portfolio (ROCE > 15% and ROE > 15%)
        coffee_can_stocks = df[(df['ROCE'] > 15) & (df['ROE'] > 15)]
        
        batch_output += "Stocks fit for a Coffee Can Portfolio (ROCE > 15% and ROE > 15%):\n"
        batch_output += f"{coffee_can_stocks}\n\n"
        
        # Check if 5 seconds have passed since the last update
        current_time = time.time()
        if current_time - last_update_time >= 5:
            output_text.insert(tk.END, batch_output)
            output_text.see(tk.END)
            output_text.update()
            batch_output = ""  # Clear the batch output
            last_update_time = current_time
        
        time.sleep(0.1)  # Small delay to prevent overwhelming the system

    # Display any remaining output
    if batch_output:
        output_text.insert(tk.END, batch_output)
    
    output_text.insert(tk.END, """
    Disclaimer: This script is provided for educational and informational purposes only. 
    It should not be construed as financial advice. The author assumes no responsibility 
    for any errors or omissions in the content or for any damages arising from the use of this code.

    © Soham Datta 2024. All rights reserved.
    """)
    output_text.see(tk.END)
    output_text.update()

def main():
    # Read the Excel file
    df_tickers = pd.read_excel('E:\C TUTORIAL-20240515T040231Z-001\C TUTORIAL\PYTHON\MCAP28032024 (1).xlsx')

    # Extract the 'Symbol' column and add '.NS' suffix
    tickers = df_tickers['Symbol'].apply(lambda x: f"{x}.NS").tolist()

    # Create the main window
    root = tk.Tk()
    root.title("Stock Analysis")
    root.geometry("800x600")

    # Create a scrolled text widget
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
    output_text.pack(expand=True, fill='both')

    # Start processing in a separate thread
    threading.Thread(target=process_data, args=(tickers, output_text), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
