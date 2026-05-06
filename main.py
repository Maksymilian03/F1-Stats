from fastapi import FastAPI
from schemas import Driver
import httpx


app = FastAPI()


@app.get("/")
def root():
    return {"message": "F1 Stats"}


@app.get('/drivers/', response_model=list[Driver])
async def get_drivers():
    url = 'https://api.openf1.org/v1/drivers'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()
    