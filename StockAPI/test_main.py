from investpy import stocks
from main import app
from fastapi import status
from fastapi.testclient import TestClient


client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == "Hello World"

def test_get_countries():
    # 1
    countries = stocks.get_stock_countries()
    res = client.get("/countries")
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert countries == res_body
    # 2
    res = client.get("/countries?sortby=desc")
    assert res.status_code == status.HTTP_200_OK
    countries.reverse()
    res_body = res.json()
    assert countries == res_body
    # 3
    res = client.get("/countries?sortby=xyz")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    res_body = res.json()
    assert res_body['detail'] == "query:sortby must be 'asce' or 'desc'"