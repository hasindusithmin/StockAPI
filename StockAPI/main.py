from investpy import stocks
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
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
    return JSONResponse(status_code=status.HTTP_200_OK,content="Hello World")

@app.get("/countries")
def get_countries(sortby:str="asce"):
    if sortby not in ['asce','desc']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="query:sortby must be 'asce' or 'desc'")
    countries = stocks.get_stock_countries()
    if sortby == "desc":
        countries.reverse()
    return countries