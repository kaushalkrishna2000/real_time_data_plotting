from fastapi import FastAPI
from api_v1 import api
from fastapi.responses import HTMLResponse
from utilities.util_1 import get_all_plot,get_specific_plot
from utilities.util_2 import filtering

app=FastAPI()


app.include_router(api.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
