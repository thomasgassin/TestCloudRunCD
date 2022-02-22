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
def keywords(city):
    if city == "London":
        data= pd.read_csv("gs://airbnbadvice/data/description_london.csv")
        # answer_keywords = data["keywords"].to_string()
        json_london = { 'city' : 'London',
                        'keywords': 'answer_keywords'}
        return json_london
    else : 
        return {'city':['no city'],
                'keywords':[""]}
    
