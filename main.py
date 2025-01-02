from fastapi import FastAPI
import pandas as pd
import os
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

# Path to the IIP data file and stock price directory
IIP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'IIP_data_Nov_2024.xlsx')
STOCKS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'Stock_Price')

# Load IIP Data
def load_iip_data():
    iip_data = pd.read_excel(IIP_FILE_PATH)
    return iip_data.to_dict(orient='records')

# Load stock data by stock name
def load_stock_data(stock_name: str):
    stock_file_path = os.path.join(STOCKS_DIRECTORY, f"{stock_name}.xlsx")
    if os.path.exists(stock_file_path):
        stock_data = pd.read_excel(stock_file_path)
        return stock_data.to_dict(orient='records')
    return None

# Endpoint to get IIP data
@app.get("/iip_data/")
async def get_iip_data():
    data = load_iip_data()
    return JSONResponse(content={"data": data})

# Endpoint to get stock data
@app.get("/stock_data/{stock_name}")
async def get_stock_data(stock_name: str):
    data = load_stock_data(stock_name)
    if data:
        return JSONResponse(content={"data": data})
    return JSONResponse(status_code=404, content={"message": "Stock data not found."})

# Search endpoint to find stock data by date range or other filters
@app.get("/stock_data/{stock_name}/range")
async def get_stock_data_in_range(stock_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    data = load_stock_data(stock_name)
    if not data:
        return JSONResponse(status_code=404, content={"message": "Stock data not found."})

    # If no start/end date is given, return all data
    if start_date and end_date:
        data = [row for row in data if start_date <= row['Date'] <= end_date]
    
    return JSONResponse(content={"data": data})
