from keras.models import load_model, model_from_json
from sklearn.preprocessing import StandardScaler
import pandas as pd

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
            
            


class Predictor(object):
    """
    """

    def __init__(self, json_path, normalized_x, **kwargs):

        modoperations = ModelOperations()
        self.model = modoperations.load_models(json_path)
        self.scalar_x = modoperations.load_normalizer(normalized_x)
        

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

    def predictss(self):
        """
        Make predictions, given some input data
        This normalizes the predictions based on the real normalization
        parameters and then generates a prediction

        :param X_input
            input vector to for prediction
        """
        
        print('*************************************************************')
        
        dataframe = pd.read_csv("./api/ml_operations/pickles/random_cutout_test.csv")
        dataset = dataframe.values
        X = dataset[:,0:200].astype(float)
        x_normed = self._normalize_input(X)
        
        ss = self.model.predict(x_normed)
#        print(self.model.predict(x_normed))
#        x_pred = self.model.predict_classes(x_normed)
#        prediction = x_pred
#        # prediction = self._denormalize_prediction(x_pred)
#        return prediction
