# Stock Analysis Script Documentation

## Overview

This Python script performs stock analysis on a list of Indian companies. It fetches financial data from multiple sources, calculates key metrics, and presents the results in a user-friendly GUI. The script is designed to help identify stocks that may be suitable for a "Coffee Can Portfolio" investment strategy.

## Features

1. Data retrieval from Finology and Yahoo Finance
2. Calculation of ROCE (Return on Capital Employed) and ROE (Return on Equity)
3. Calculation of loan growth
4. GUI for displaying real-time analysis results
5. Identification of stocks suitable for a Coffee Can Portfolio

## Dependencies

The script relies on the following Python libraries:

- `requests`: For making HTTP requests
- `beautifulsoup4`: For web scraping
- `yfinance`: For fetching financial data from Yahoo Finance
- `pandas`: For data manipulation and analysis
- `tkinter`: For creating the GUI
- `threading`: For running the analysis in a separate thread

## How It Works

### 1. Data Retrieval

#### ROCE and ROE
The `get_roce_roe()` function scrapes data from Finology:
- It constructs a URL for each company using the ticker symbol
- Uses BeautifulSoup to parse the HTML and extract ROCE and ROE values

#### Loan Growth
The `get_loan_growth()` function uses yfinance:
- Fetches the company's balance sheet data
- Calculates the year-over-year growth in total debt

### 2. Data Processing

The `process_data()` function:
- Iterates through the list of ticker symbols
- Calls `get_roce_roe()` and `get_loan_growth()` for each ticker
- Compiles the data into a pandas DataFrame
- Filters stocks that meet the Coffee Can Portfolio criteria (ROCE > 15% and ROE > 15%)

### 3. User Interface

The script uses tkinter to create a GUI:
- Displays a scrollable text widget for output
- Updates the display every 5 seconds with batch results
- Runs the analysis in a separate thread to keep the GUI responsive

### 4. Main Execution

The `main()` function:
- Reads ticker symbols from an Excel file
- Sets up the GUI
- Initiates the data processing in a separate thread

## Usage

1. Ensure all required libraries are installed
2. Prepare an Excel file with company symbols in a column named 'Symbol'
3. Update the Excel file path in the `main()` function
4. Run the script

The GUI will display:
- Progress updates for each ticker being processed
- A full data table of all analyzed stocks
- A filtered table of stocks meeting the Coffee Can Portfolio criteria

## Disclaimer

This script is provided for educational and informational purposes only. It should not be construed as financial advice. The author assumes no responsibility for any errors or omissions in the content or for any damages arising from the use of this code.

Users should conduct their own research and consult with a qualified financial advisor before making any investment decisions.

## Copyright

© Soham Datta 2024. All rights reserved.

## Notes for Improvement

1. Error Handling: The script includes basic error handling, but this could be enhanced for more robust operation.
2. Rate Limiting: Consider implementing rate limiting to avoid overwhelming data sources.
3. Data Persistence: Adding functionality to save results to a file could be beneficial.
4. Configuration: Moving hardcoded values (like ROCE/ROE thresholds) to a config file would improve flexibility.
5. Additional Metrics: The analysis could be expanded to include more financial metrics for a more comprehensive evaluation.


### Web Scraping Disclaimer

This script includes functionality for web scraping to gather financial data. Please be aware of the following:

1. Legal Considerations: Web scraping may be subject to legal restrictions. Always review and comply with the terms of service of any website you're scraping.

2. Ethical Use: Respect the websites you're scraping. Avoid overloading their servers with excessive requests.

3. Data Ownership: The data you scrape may be protected by copyright. Ensure you have the right to use the data as intended.

4. Website Changes: Websites can change their structure at any time, which may break the scraping functionality of this script.

5. IP Blocking: Aggressive scraping may result in your IP address being blocked by the target website.

6. Alternative APIs: Where possible, consider using official APIs provided by financial data services instead of web scraping.

7. Responsibility: Users of this script are solely responsible for ensuring their use of the web scraping functionality is legal, ethical, and in compliance with all applicable terms of service.

By using the web scraping features of this script, you acknowledge these considerations and agree to use this functionality responsibly.


