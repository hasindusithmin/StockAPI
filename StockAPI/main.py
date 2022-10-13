import calendar
from investpy import stocks
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse,RedirectResponse,FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="StockAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return RedirectResponse("/docs")

@app.get("/report")
def get_test_report():
    return FileResponse(path='report.html')

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
        available_countries = stocks.get_stock_countries()
        if country not in available_countries:
            detail = {
                'message':f'country:{country} not available',
                'similar':[c for c in available_countries if c.startswith(country[0])]
            }
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
        else:
            return stocks.get_stocks_dict(country=country)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Object is too large.')


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

def gen_profile(stock,country):
    try:
        return stocks.get_stock_company_profile(stock=stock,country=country)
    except:
        return JSONResponse(content=f'Sorry, Data Not Found',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.get('/profile/{stock}/{country}')
def get_profile(stock:str,country:str):
    stock = stock.strip().upper()
    country = country.strip().lower()
    
    available_stocks = stocks.get_stocks_list()
    available_countries = stocks.get_stock_countries()
    
    if stock not in available_stocks:
        return JSONResponse(content=f'Stock:{stock.lower()} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    if country not in available_countries:
        return JSONResponse(content=f'Country:{country} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    return gen_profile(stock,country)

def gen_summary(stock,country):
    try:
        df =  stocks.get_stock_financial_summary(stock=stock,country=country)
        df = df.reset_index()
        mylist = []
        for i in range(len(df)):
            dict = df.iloc[i].to_dict()
            date = dict['Date'].to_pydatetime()
            dict['Date'] = calendar.timegm(date.utctimetuple())
            mylist.append(dict)
        return mylist
    except:
        return JSONResponse(content=f'Sorry, Data Not Found',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get('/summary/{stock}/{country}')
def get_summary(stock:str,country:str):
    stock = stock.strip().upper()
    country = country.strip().lower()
    
    available_stocks = stocks.get_stocks_list()
    available_countries = stocks.get_stock_countries()
    
    if stock not in available_stocks:
        return JSONResponse(content=f'Stock:{stock.lower()} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    if country not in available_countries:
        return JSONResponse(content=f'Country:{country} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    return gen_summary(stock,country)


def gen_info(stock,country):
    try:
        return stocks.get_stock_information(stock=stock, country=country, as_json=True)
    except:
        return JSONResponse(content=f'Sorry, Data Not Found',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get('/info/{stock}/{country}')
def get_info(stock:str,country:str):
    stock = stock.strip().upper()
    country = country.strip().lower()
    
    available_stocks = stocks.get_stocks_list()
    available_countries = stocks.get_stock_countries()
    
    if stock not in available_stocks:
        return JSONResponse(content=f'Stock:{stock.lower()} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    if country not in available_countries:
        return JSONResponse(content=f'Country:{country} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    return gen_info(stock,country)

def gen_ohlcv(stock,country):
    try:
        return stocks.get_stock_recent_data(stock=stock, country=country, as_json=True)
    except:
        return JSONResponse(content=f'Sorry, data is not available at this moment.',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get('/ohlcv/{stock}/{country}')
def get_ohlcv(stock:str,country:str):
    stock = stock.strip().upper()
    country = country.strip().lower()
    
    available_stocks = stocks.get_stocks_list()
    available_countries = stocks.get_stock_countries()
    
    if stock not in available_stocks:
        return JSONResponse(content=f'Stock:{stock.lower()} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    if country not in available_countries:
        return JSONResponse(content=f'Country:{country} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    return gen_ohlcv(stock,country)

def gen_overview(country):
    try:
        return stocks.get_stocks_overview(country=country, as_json=True)
    except:
        return JSONResponse(content=f'Sorry, Data Not Found',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get('/overview/{country}')
def get_overview(country:str):
    country = country.strip().lower()
    available_countries = stocks.get_stock_countries()
    
    if country not in available_countries:
        return JSONResponse(content=f'Country:{country} Not Found',status_code=status.HTTP_404_NOT_FOUND)
    
    return gen_overview(country)


