from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return "Hello from Cloud Run CD"

@app.get("/keywords")
def city_keywords(city):
    if city == "London":
        data= pd.read_csv("gs://airbnbadvice/data/description_london.csv")
        answer_keyword = data["keywords"].tolist()
        json_london = { 'city' : ['London'],
                        'keywords': answer_keyword }
        return json_london
    else : 
        return {'city':['no city'],
                'keywords':[""]}
    
