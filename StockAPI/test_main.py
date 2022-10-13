import investpy
from main import app
from fastapi import status
from fastapi.testclient import TestClient


client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == "Hello World"