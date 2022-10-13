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
            detail = {
                'message':f'country:{country} not available',
                'similar':[c for c in available_countries if c.startswith(country[0])]
            }
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
        else:
            return stocks.get_stocks_dict(country=country)
    return stocks.get_stocks_dict()


@app.get('/activecountries/{stock}')
def get_active_countries(stock:str):
    stock = stock.upper()
    
    available_stocks = stocks.get_stocks_list()
    if stock not in available_stocks:
        detail = {
            'message':f'stock:{stock.lower()} not available',
            'similar':[s.lower() for s in available_stocks if s.startswith(stock[0].upper())]
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=detail)
    
    df = stocks.get_stocks().query(f"symbol == '{stock}'")
    mylist = []
    for i in range(len(df)):
        mylist.append(df.iloc[i].to_dict())
    return mylist