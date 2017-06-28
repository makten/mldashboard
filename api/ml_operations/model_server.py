# Only testing
import pandas as pd
import numpy as np
from keras.models import load_model, model_from_json
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import json
from . import settings

try:
    import cPickle as pickle
except:
    import pickle

predictor = None  

def getModel(model_path):
        
    return load_model(model_path)



def load_scalar(scaler_path):
    try:
        f = open(scaler_path, 'rb')
        scalar = pickle.load(f)
        f.close()            
        return scalar
        
    except:
        raise Exception('Failed to load normalizer')



def normalize_input(X_input, scalar_path):
            
            scalar_x = load_scalar(scalar_path)
            X_input = scalar_x.fit_transform(X_input)
            
            return X_input


def denormalize_prediction(y_pred, scalar_path):
        
        scalar_y = load_scalar(scalar_path)
        value0 = scalar_y.inverse_transform(y_pred[:, -1])
        value1 = scalar_y.inverse_transform(y_pred[:, 0])
        return value0, value1

def faultPredictor():

    
    try:
        from random import randint

        dataframe = pd.read_csv("./api/ml_operations/pickles/random_cutout_test.csv")
        dataset = dataframe.values

        rand = randint(1, 32)
        X = dataset[:rand, 0:200].astype(float)
        y = dataset[:rand, -1].astype(int)
        

        model = getModel(settings.model_path)
        x_normed = normalize_input(X, settings.path_x_normalizer)

        y_pred = model.predict_classes(x_normed)        

        y_pred_actual = np.stack((y_pred, y), axis=1)             
        
        predictions, actuals = denormalize_prediction(y_pred_actual, settings.path_y_normalizer)

        combine_outputs = np.stack((predictions, actuals), axis =1)
        output_vals = json.dumps(combine_outputs.tolist())        

    except:
                
        return Exception("Something Went Wrong")

    
    from keras.backend.tensorflow_backend import clear_session
    clear_session()     

    return output_vals
