# -*- coding: utf-8 -*-

from keras.models import load_model, model_from_json
from sklearn.preprocessing import StandardScaler
import pandas as pd
import tensorflow as tf

tf.reset_default_graph()
try:
    import cPickle as pickle
except:
    import pickle
    



class ModelOperations(object):
    """
    """

    def __init__(self):
        pass

    def load_models(self, model_path):
        
        try:           

            model = load_model('./api/ml_operations/pickles/fault_classifier.h5')
#                        
            return model
        
        except:
            
            raise Exception('Failed to load model/weights')
            


    def load_normalizer(self, sk_normalized):
        """
        This function loads the sklearn.preprocessing.StandardScaler object
        which had been used to normalize the original dataset
        """
        try:
             f = open(sk_normalized, 'rb')
             scalar = pickle.load(f)
             f.close()            
             return scalar
        
        except:
            raise Exception('Failed to load normalizer')
            
    
    def revers_labels(path_sk_normalizer, y_pred):
        try:
             f = open(path_sk_normalizer, 'rb')
             scalar = pickle.load(f)
             f.close()            
             return scalar
        
        except:
            raise Exception('Failed to load normalizer')
        

            
            
           
            

class Predictor(object):
    """
    """

    def __init__(self, model_path, normalized_x, normalized_y, **kwargs):
    
            modoperations = ModelOperations()
            self.model = modoperations.load_models(model_path)
            self.scalar_x = modoperations.load_normalizer(normalized_x)
            self.scalar_y = modoperations.load_normalizer(normalized_y)
            
    
    def _normalize_input(self, X_input):
            """
            Normalizes the input object to be predicted according to the scalar
            used during the training process
            :param X_input:
                Input data to transform( normalize)
            """
    
            X_input = self.scalar_x.fit_transform(X_input)
            
            return X_input



    def _denormalize_prediction(self, x_pred):
        """
        De-normalizes the x_pred to actual value as per dataset
        :param x_pred
        """
        value = self.scalar_y.inverse_transform(x_pred)
        return value
    
    
    

    def predicts(self, X_input):
        """
        Make predictions, given some input data
        This normalizes the predictions based on the real normalization
        parameters and then generates a prediction

        :param X_input
            input vector to for prediction
        """
        
        print(X_input)
        x_normed = self._normalize_input(X_input)    
        print(self.model.summary())
        print(x_normed)
        
        x_pred = self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])    
#        prediction = self._denormalize_prediction(x_pred)
#        return prediction

