from fastapi import FastAPI
import pandas as pd
import os
from fastapi.responses import JSONResponse
from typing import Optional

# Custom metadata for the API docs
app = FastAPI(
    title="Stock and Economic Data API",
    description="This API provides stock market and economic data, including IIP and inflation statistics.",
    version="1.0.0",
    docs_url="/docs",  # Custom path for the Swagger UI documentation
    redoc_url="/redoc",  # Custom path for the ReDoc documentation
)

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

# Root endpoint with custom description for docs
@app.get("/", response_description="Root Endpoint")
async def root():
    """
    This is the root endpoint of the Stock and Economic Data API.
    It provides a general message about the available API.
    """
    return {"message": "Welcome to the FastAPI Stock and Economic Data API! Visit /docs for the API documentation."}

# Endpoint to get IIP data
@app.get("/iip_data/", response_description="Economic Data (IIP)")
async def get_iip_data():
    """
    This endpoint retrieves the Index of Industrial Production (IIP) data for different sectors.
    The data includes information like inflation, manufacturing sectors, and other economic indicators.
    """
    data = load_iip_data()
    return JSONResponse(content={"data": data})

# Endpoint to get stock data
@app.get("/stock_data/{stock_name}", response_description="Stock Data")
async def get_stock_data(stock_name: str):
    """
    This endpoint retrieves stock data for a specified stock.
    The data includes fields like Date, Open, High, Low, Close, Adj Close, and Volume.
    """
    data = load_stock_data(stock_name)
    if data:
        return JSONResponse(content={"data": data})
    return JSONResponse(status_code=404, content={"message": "Stock data not found."})

# Search endpoint to find stock data by date range or other filters
@app.get("/stock_data/{stock_name}/range", response_description="Stock Data in Date Range")
async def get_stock_data_in_range(stock_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    This endpoint retrieves stock data for a specified stock within a given date range.
    You can specify a `start_date` and `end_date` to filter the data.
    """
    data = load_stock_data(stock_name)
    if not data:
        return JSONResponse(status_code=404, content={"message": "Stock data not found."})

    # If no start/end date is given, return all data
    if start_date and end_date:
        data = [row for row in data if start_date <= row['Date'] <= end_date]
    
    return JSONResponse(content={"data": data})

# Handle favicon request to avoid 404
@app.get("/favicon.ico", response_description="Favicon Endpoint")
async def favicon():
    """
    This endpoint serves the favicon.ico request.
    Returning a placeholder as no favicon is provided.
    """
    return {"message": "No favicon available"}
