from fastapi import FastAPI,APIRouter
import requests

router = APIRouter()

# IEX Cloud API key
IEX_API_KEY = "pk_0b3ef1c9be9f45b598b4788633f31be2"

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "UX1HBCHIZB4E8NCS"



@router.get("/iex/market-data/{symbol}")
def get_iex_data(symbol: str):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={IEX_API_KEY}"
    response = requests.get(url)
    print(response.json())
    return response.json()

@router.get("/alphavantage/market-data/{symbol}")
def get_alpha_vantage_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    print(response.json())
    return response.json()
