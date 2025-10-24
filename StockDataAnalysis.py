# Import all required libraries
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Function to make stock graphs
def make_graph(stock_data, revenue_data, stock_symbol, title):
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, 
                        subplot_titles=(f"Historical Share Price of {stock_symbol}", 
                                      f"Historical Revenue of {stock_symbol}"), 
                        vertical_spacing=0.3)
    
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-06-14']
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), 
                             y=stock_data_specific.Close.astype("float"), 
                             name="Share Price"), 
                  row=1, col=1)
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), 
                             y=revenue_data_specific.Revenue.astype("float"), 
                             name="Revenue"), 
                  row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    
    fig.update_layout(showlegend=False, height=900, title=title)
    fig.show()

# =============================================================================
# QUESTION 1: Use yfinance to Extract Tesla Stock Data
# =============================================================================
print("QUESTION 1: Extracting Tesla Stock Data using yfinance")

# Extract Tesla stock data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")

# Reset index and display first five rows
tesla_data.reset_index(inplace=True)
print("First five rows of Tesla stock data:")
print(tesla_data.head())

# =============================================================================
# QUESTION 2: Use Webscraping to Extract Tesla Revenue Data
# =============================================================================
print("\nQUESTION 2: Extracting Tesla Revenue Data using Webscraping")

# Download Tesla revenue data webpage
tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
tesla_html_data = requests.get(tesla_url).text

# Parse HTML data
tesla_soup = BeautifulSoup(tesla_html_data, 'html.parser')

# Create DataFrame for Tesla revenue
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Extract revenue data from table
for row in tesla_soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)

# Clean the revenue data
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',', '').str.replace('$', '')
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print("Last five rows of Tesla revenue data:")
print(tesla_revenue.tail())

# =============================================================================
# QUESTION 3: Use yfinance to Extract GameStop Stock Data
# =============================================================================
print("\nQUESTION 3: Extracting GameStop Stock Data using yfinance")

# Extract GameStop stock data
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")

# Reset index and display first five rows
gme_data.reset_index(inplace=True)
print("First five rows of GameStop stock data:")
print(gme_data.head())

# =============================================================================
# QUESTION 4: Use Webscraping to Extract GameStop Revenue Data
# =============================================================================
print("\nQUESTION 4: Extracting GameStop Revenue Data using Webscraping")

# Download GameStop revenue data webpage
gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gme_html_data = requests.get(gme_url).text

# Parse HTML data
gme_soup = BeautifulSoup(gme_html_data, 'html.parser')

# Create DataFrame for GameStop revenue
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Extract revenue data from table
for row in gme_soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)

# Clean the revenue data
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',', '').str.replace('$', '')
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

print("Last five rows of GameStop revenue data:")
print(gme_revenue.tail())

# =============================================================================
# QUESTION 5: Plot Tesla Stock Graph
# =============================================================================
print("\nQUESTION 5: Plotting Tesla Stock Graph")

# Plot Tesla stock graph
make_graph(tesla_data, tesla_revenue, 'Tesla', 'Tesla Stock Price and Revenue Analysis')

# =============================================================================
# QUESTION 6: Plot GameStop Stock Graph
# =============================================================================
print("\nQUESTION 6: Plotting GameStop Stock Graph")

# Plot GameStop stock graph
make_graph(gme_data, gme_revenue, 'GameStop', 'GameStop Stock Price and Revenue Analysis')

# =============================================================================
# SUMMARY OUTPUT
# =============================================================================
print("\n" + "="*50)
print("PROJECT SUMMARY")
print("="*50)

print(f"Tesla Data Shape: {tesla_data.shape}")
print(f"Tesla Revenue Shape: {tesla_revenue.shape}")
print(f"GameStop Data Shape: {gme_data.shape}")
print(f"GameStop Revenue Shape: {gme_revenue.shape}")

print("\nTesla Data Info:")
print(tesla_data.info())

print("\nGameStop Data Info:")
print(gme_data.info())

print("\nPROJECT COMPLETED SUCCESSFULLY!")
