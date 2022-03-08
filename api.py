from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

from pred import generate_text_seq

# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle
# from io import BytesIO

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
    return "Hello from the team "

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
    gcs_path = 'gs://airbnbadvice/model/model_rf_price_log.pkl'
    loaded_model = joblib.load(tf.io.gfile.GFile(gcs_path, 'rb'))
    X_to_predict = pd.DataFrame.from_dict(dictionnary,orient="index")
    predicted_fare_log = loaded_model.predict(X_to_predict.T)
    predicted_fare = np.exp(predicted_fare_log)
    json_predicted_fare={'predicted_fare' : predicted_fare[0]}
    return json_predicted_fare
    
# @app.get("/fare_prediction")
# def fare_prediction(json): #not sure which argument shoud be passed the idea is to ret
#     data_frame = pd.DataFrame.from_dict(pd.json_normalize(json), orient='columns')    
#     # gcs_path = 'gs://airbnbadvice/model/model_rf_price_log.pkl'
#     # loaded_model = joblib.load(tf.io.gfile.GFile(gcs_path, 'rb'))
#     return data_frame

@app.get("/announcement")
def announcement(keywords1="keywords1"):
    result = generate_text_seq(str(keywords1))
    json_announce_created={"announce":result}
    return json_announce_created