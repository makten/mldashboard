
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
# from keras.callbacks import ModelCheckpoint
# from keras.models import load_model
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

from keras import optimizers
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
plt.style.use(['fivethirtyeight'])


data = pd.read_csv('datasets/zero_imputed_binary_original.csv', delimiter=',', low_memory=False)

#faulty = data[data.code == 1]
#no_faulty = data[data.code != 1]
#
#xx = faulty.iloc[:600, [0]]

#plt.plot(faulty.iloc[:100, [0]])
#plt.plot(no_faulty.iloc[0:100, [0]])
#plt.legend(['faulty', 'non-fault'], loc='upper left')

def splitXy(data):
    X = data.iloc[:, 0:200]
    y = data.iloc[:, -1]
    return X, y

X, y = splitXy(data)


# for reproducibility
seed = 7
np.random.seed(seed)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state =42)


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
#sc_y = StandardScaler()
#y_train = sc_y.fit_transform(y_train)


# one hot encode outputs
#y_train = np_utils.to_categorical(y_train)
#y_test = np_utils.to_categorical(y_test)
#num_classes = y_test.shape[1]




def base_model():
    model = Sequential()
    model.add(Dense(350, input_shape=(200,), activation='relu'))
    model.add(Dropout(0.2))      
    model.add(Dense(110, activation='relu')) 
    model.add(Dropout(0.25))
#    model.add(Dense(110, activation='relu')) 
    model.add(Dense(5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
#    sgd = optimizers.SGD(lr=0.1, momentum=0.8, decay=1e-6, nesterov = 0.7)
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model


# build the model
model = base_model()


# Fit the model
hist = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=40, verbose=1)


scores = model.evaluate(X_test, y_test, verbose=0)

y_pred = model.predict_classes(X_test)
#prob = model.predict_proba(X_test)




print("Baseline Error: %.2f%%" % (100-scores[1]*100))


train_loss = hist.history['loss']
val_loss = hist.history['val_loss']
train_acc = hist.history['acc']
val_acc = hist.history['val_acc']
xc = range(100)


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


labels = ['True', 'False']

print(classification_report(y_test, y_pred, target_names=labels))
print(confusion_matrix(y_test, y_pred))
