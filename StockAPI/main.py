from investpy import stocks
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="StockAPI")
available_countries = stocks.get_stock_countries()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK,content="Hello World")

@app.get("/countries")
def get_countries(sortby:str="asce"):
    sortby = sortby.lower().strip()
    if sortby not in ['asce','desc']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="query:sortby must be 'asce' or 'desc'")
    countries = stocks.get_stock_countries()
    if sortby == "desc":
        countries.reverse()
    return countries

@app.get("/stock")
def get_stock(country:str=None):
    if country is not None:
        country = country.lower().strip()
        if country not in available_countries:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"country:{country} not available")
        else:
            return stocks.get_stocks_dict(country=country)
    return stocks.get_stocks_dict()