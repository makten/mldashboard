# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
# from keras.callbacks import ModelCheckpoint
# from keras.models import load_model
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import norm
from keras.utils import np_utils
from keras import backend as K
from keras.models import Sequential, load_model, model_from_json
from keras.layers import Dense
from keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasClassifier
K.set_image_dim_ordering('th')
from sklearn.model_selection import train_test_split, KFold, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
import seaborn as sns
#sns.set(color_codes=True)
try:
    import cPickle as pickle
except:
    import pickle
    


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)


# load dataset
dataframe = pd.read_csv("./api/ml_operations/pickles/final_oversampled_zero_impute.csv")
#dataframe = pd.read_csv("./api/ml_operations/pickles/never_seen_test.csv")

#from sklearn.externals import joblib
#joblib.dump(sc_X, 'save_models/x_scaler.pkl')

#sns.distplot(X[:3100, 98:99])

dataset = dataframe.values
X = dataset[:,0:200].astype(float)
Y = dataset[:,-1]


# encode class values as integers
sc_X = StandardScaler()
X = sc_X.fit_transform(X)


encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
dummy_y = np_utils.to_categorical(encoded_Y)


print('Persisting StandardScalar To Disk ...')
pickle.dump(encoder, 
            open('./api/ml_operations/pickles/y_scalar.pickle', 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

pickle.dump(sc_X, 
            open('./api/ml_operations/pickles/x_scalar.pickle', 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)




kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
cvscores = []

print('Compiling and Training Model.....')

for train, test in kfold.split(X, dummy_y):
    model = Sequential()
    model.add(Dense(120, input_shape=(200,), kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(150, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(10, kernel_initializer='normal', activation='relu'))
    model.add(Dense(4, kernel_initializer='normal', activation='sigmoid'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    hist = model.fit(X[train], dummy_y[train], epochs = 1000, batch_size = 300, verbose=1)
    
    scores = model.evaluate(X[test], dummy_y[test], verbose= 1)
    print('%s: %.2f%%' % (model.metrics_names[1], scores[1]* 100))
    cvscores.append(scores[1]* 100)
    
print('%s: %.2f%%' % (np.mean(cvscores), np.std(cvscores)))


print('Persisting Model To Disk .........')
open('./api/ml_operations/pickles/fault_classifier.json', 'w').write(model.to_json())
model.save_weights('./api/ml_operations/pickles/fault_classifier_weights.h5')

#model.save('./api/ml_operations/pickles/fault_classifier.h5')

y_pred = model.predict_classes(X)
#prob = model.predict_proba(X_test)


loadedModel = load_model('save_models/98_perc_multiclass.h5')

tttt = loadedModel.predict_classes(X)


print("Baseline Error: %.2f%%" % (100-scores[1]*100))


train_loss = hist.history['loss']
val_loss = hist.history['val_loss']
train_acc = hist.history['acc']
val_acc = hist.history['val_acc']
xc = range(230)


plt.figure(1, figsize=(7,5))
plt.plot(xc, train_loss)
plt.plot(xc, val_loss)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.title('train vs val loss')
plt.grid(True)
plt.legend('train', 'val')
#print(plt.style.available)
plt.style.use(['fivethirtyeight'])

from sklearn.metrics import classification_report, confusion_matrix


labels = ['0 (No Fault)', '1 (F0184)', '2 (F0185)', '3 (F0844)']

print(classification_report(np.argmax(dummy_y, axis=1), y_pred, target_names=labels))
print(confusion_matrix(np.argmax(dummy_y, axis=1), y_pred))