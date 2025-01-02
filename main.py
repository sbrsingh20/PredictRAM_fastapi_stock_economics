from fastapi import FastAPI, HTTPException
import pandas as pd
import os
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI(
    title="Stock and Economic Data API",
    description="This API provides stock market and economic data, including IIP and inflation statistics.",
    version="1.0.0",
    docs_url="/docs",  # Custom path for Swagger UI documentation
    redoc_url="/redoc",  # Custom path for ReDoc documentation
)

# Path to the IIP data file and stock price directory
IIP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'IIP_data_Nov_2024.xlsx')
STOCKS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'Stock_Price')

# Load IIP Data with error handling
def load_iip_data():
    try:
        # Try reading the IIP data file
        if not os.path.exists(IIP_FILE_PATH):
            raise FileNotFoundError(f"File {IIP_FILE_PATH} not found.")
        
        iip_data = pd.read_excel(IIP_FILE_PATH)
        return iip_data.to_dict(orient='records')
    except FileNotFoundError as fnf_error:
        raise HTTPException(status_code=404, detail=str(fnf_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading IIP data: {str(e)}")

# Load stock data by stock name with error handling
def load_stock_data(stock_name: str):
    try:
        # Construct the path for the stock data file
        stock_file_path = os.path.join(STOCKS_DIRECTORY, f"{stock_name}.xlsx")
        if not os.path.exists(stock_file_path):
            raise FileNotFoundError(f"Stock data for {stock_name} not found.")
        
        stock_data = pd.read_excel(stock_file_path)
        return stock_data.to_dict(orient='records')
    except FileNotFoundError as fnf_error:
        raise HTTPException(status_code=404, detail=str(fnf_error))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading stock data: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Stock and Economic Data API! Visit /docs for the API documentation."}

# Endpoint to get IIP data
@app.get("/iip_data/")
async def get_iip_data():
    data = load_iip_data()
    return JSONResponse(content={"data": data})

# Endpoint to get stock data
@app.get("/stock_data/{stock_name}")
async def get_stock_data(stock_name: str):
    data = load_stock_data(stock_name)
    return JSONResponse(content={"data": data})

# Search endpoint to find stock data by date range
@app.get("/stock_data/{stock_name}/range")
async def get_stock_data_in_range(stock_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    data = load_stock_data(stock_name)
    if start_date and end_date:
        # Filter data by date range (implement date filtering logic)
        data = [row for row in data if start_date <= row['Date'] <= end_date]
    
    return JSONResponse(content={"data": data})

# Handle favicon request
@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}
