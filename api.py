from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import pickle
from io import BytesIO


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
        data = pd.read_csv("https://storage.googleapis.com/airbnbadvice/data/description_london.csv" )
        json_london = { 'city' : 'London',
                        'keywords': data.keywords}
        return json_london
    else : 
        return {'city':'no city',
                'keywords':""}
    
# @app.get("/fare_prediction")
# def fare_prediction(json): #not sure which argument shoud be passed the idea is to ret
#     data_frame = pd.DataFrame.from_dict(pd.json_normalize(json), orient='columns')    
#     # gcs_path = 'gs://airbnbadvice/model/model_rf_price_log.pkl'
#     # loaded_model = joblib.load(tf.io.gfile.GFile(gcs_path, 'rb'))
#     return data_frame

@app.get("/fare_prediction")
def fare_prediction(latitude ="latitude",longitude="longitude",accomodates ="accomodates",bedrooms="bedrooms",beds="beds",minimum_nights = "minimum_nights",Entire_home_apt = "Entire_home_apt"): #not sure which argument shoud be passed the idea is to ret
    dictionnary = { 'latitude': float(latitude),
                    'longitude':float(longitude),
                    'accomodates' :int(accomodates),
                    'bedrooms' : int(bedrooms),
                    'beds': int(beds),
                    'minimum_nights': int(minimum_nights),
                    'Entire_home_apt':int(Entire_home_apt)
                    }
    dictionnary2= {  "latitude" : 51.50344025 ,
                        "longitude" : -0.12770820958562096 ,
                        "accomodates":2,
                        "bedrooms" : 2 , 
                        "beds" : 1,
                        "minimum_nights" : 1 , 
                        "Entire_home_apt" : 1
                    }
    X_to_predict = pd.DataFrame.from_dict(dictionnary,orient="index")
    gcs_path = 'gs://airbnbadvice/model/model_rf_price_log.pkl'
    loaded_model = joblib.load(tf.io.gfile.GFile(gcs_path, 'rb'))
    predicted_fare_log = loaded_model.predict(X_to_predict.T)
    predicted_fare = np.exp(predicted_fare_log)
    return predicted_fare[0]



# {  "latitude" : 51.50344025 ,
#     "longitude" : -0.12770820958562096 ,
#     "accomodates":2,
#     "bedrooms" : 2 , 
#     "beds" : 1,
#     "minimum_nights" : 1 , 
#     "Entire_home_apt" : 1
# }