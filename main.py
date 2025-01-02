from fastapi import FastAPI, HTTPException
import pandas as pd
import os
from fastapi.responses import JSONResponse
from typing import Optional
import logging

# Setup logger for detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the FastAPI app instance
app = FastAPI(
    title="Stock and Economic Data API",
    description="API for stock market data and economic indicators (IIP, Inflation, etc.)",
    version="1.0.0",
)

# Paths to files
IIP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'IIP_data_Nov_2024.xlsx')
STOCKS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'Stock_Price')

# Function to load IIP data with error handling
def load_iip_data():
    try:
        # Check if the IIP data file exists
        if not os.path.exists(IIP_FILE_PATH):
            logger.error(f"File {IIP_FILE_PATH} not found.")
            raise FileNotFoundError(f"File {IIP_FILE_PATH} not found.")
        
        # Read the IIP data using pandas
        iip_data = pd.read_excel(IIP_FILE_PATH)
        logger.debug("IIP data loaded successfully.")
        return iip_data.to_dict(orient='records')
    
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found error: {str(fnf_error)}")
        raise HTTPException(status_code=404, detail="IIP data file not found.")
    except Exception as e:
        logger.exception(f"Unexpected error while loading IIP data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading IIP data: {str(e)}")

# Function to load stock data by stock name with error handling
def load_stock_data(stock_name: str):
    try:
        # Construct the file path for the stock data
        stock_file_path = os.path.join(STOCKS_DIRECTORY, f"{stock_name}.xlsx")
        
        # Check if the stock data file exists
        if not os.path.exists(stock_file_path):
            logger.error(f"Stock data file for {stock_name} not found.")
            raise FileNotFoundError(f"Stock data file for {stock_name} not found.")
        
        # Read the stock data using pandas
        stock_data = pd.read_excel(stock_file_path)
        logger.debug(f"Stock data for {stock_name} loaded successfully.")
        return stock_data.to_dict(orient='records')
    
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found error: {str(fnf_error)}")
        raise HTTPException(status_code=404, detail=f"Stock data file for {stock_name} not found.")
    except Exception as e:
        logger.exception(f"Unexpected error while loading stock data for {stock_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading stock data for {stock_name}: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Stock and Economic Data API! Visit /docs for the API documentation."}

# Endpoint to get IIP data
@app.get("/iip_data/")
async def get_iip_data():
    try:
        data = load_iip_data()
        return JSONResponse(content={"data": data})
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error in /iip_data/ endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Endpoint to get stock data for a specific stock by stock_name
@app.get("/stock_data/{stock_name}")
async def get_stock_data(stock_name: str):
    try:
        data = load_stock_data(stock_name)
        return JSONResponse(content={"data": data})
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error in /stock_data/{stock_name} endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Endpoint to get stock data in a date range
@app.get("/stock_data/{stock_name}/range")
async def get_stock_data_in_range(stock_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    try:
        data = load_stock_data(stock_name)
        
        # Filtering data by date range if both start_date and end_date are provided
        if start_date and end_date:
            filtered_data = [
                row for row in data if start_date <= row['Date'] <= end_date
            ]
            return JSONResponse(content={"data": filtered_data})
        
        return JSONResponse(content={"data": data})
    
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        logger.error(f"Error in /stock_data/{stock_name}/range endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Handle favicon request (if any)
@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}
