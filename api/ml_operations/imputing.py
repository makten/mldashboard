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

try:
    import cPickle as pickle
except:
    import pickle
    

dataset = pd.read_csv('./api/ml_operations/pickles/24_hour_window.csv', delimiter=',', low_memory=False)


dataset.iloc[3:100, :6].plot(kind='density', layout=(2,2), subplots=True, sharex=False)
plt.show()


#rm_35_lower = dataset[dataset.procent > 35]
#
#day_hour_window = rm_35_lower.iloc[:, :204]
#
#df = day_hour_window.drop('created_epoch', axis=1)
#
#df['code'].fillna(0, inplace=True)

#dataset.ix[dataset.code != 0, 'code'] = 1 ## only group replace
dataset['code'] = np.where(dataset['code'] == 0, 0, 1)




#small = dataset.iloc[:500, :]
LE = LabelEncoder()
dataset['coded'] = LE.fit(dataset['code']).transform(dataset['code'])

print('Persisting StandardScalar To Disk ...')
pickle.dump(LE, 
            open('./api/ml_operations/pickles/y_labeler.pickle', 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

#f = open('./api/ml_operations/pickles/y_labeler.pickle', 'rb')
#scalar = pickle.load(f)
#f.close() 

#print(scalar.inverse_transform([[0]]))


dataset = dataset.drop(['dn'], axis=1)


dataset['ucs_coded'] = LE.fit(dataset['ucs']).transform(dataset['ucs'])

dataset = dataset.drop(['ucs'], axis=1)
dataset = dataset.drop(['code'], axis=1)





imp = Imputer(missing_values="NaN", strategy="mean", axis=1)
Imputer

small = imp.fit_transform(dataset)
small = dataset.astype(object).T.fillna(dataset.mean(axis=1)).T
small = dataset.astype(object).T.fillna(0).T

v = pd.DataFrame(small, columns = dataset.columns)


t = list(LE.inverse_transform(v['coded'].astype(int)))




dataset.to_csv('datasets/zero_imputed_binary_original.csv', sep=',', encoding='utf-8')


#np.savetxt('datasets/imputed_data-'+str(time.time())+'.csv', small, delimiter=',')



data = pd.read_csv('datasets/transform_dataset.csv', delimiter=',', low_memory=False)

#data.iloc[:100, :6].plot(kind='density', subplots=True, sharex=False)
#plt.show()


def splitXy(data):
    X = data.iloc[:, 2:202]
    y = data.iloc[:, -1]
    return X, y

X, y = splitXy(data)

import matplotlib
from scipy.stats import norm

#colors = ['red','green','blue','purple']
#fig = plt.figure(figsize=(8,8))
#plt.scatter(X, y, c=y, cmap=matplotlib.colors.ListedColormap(colors))
#plt.show()




from keras.utils import np_utils
from keras import backend as K


# for reproducibility
seed = 7
np.random.seed(seed)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state =42)


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
#sc_y = StandardScaler()
#y_train = sc_y.fit_transform(y_train)



# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend as K
K.set_image_dim_ordering('th')

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(160, input_shape=(200,),  activation='relu'))
	model.add(Dense(115, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model



# build the model
model = baseline_model()


# Fit the model
hist = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=1000, batch_size=200, verbose=1)


scores = model.evaluate(X_test, y_test, verbose=0)

y_pred = model.predict_classes(X_test)
#prob = model.predict_proba(X_test)




print("Baseline Error: %.2f%%" % (100-scores[1]*100))


train_loss = hist.history['loss']
val_loss = hist.history['val_loss']
train_acc = hist.history['acc']
val_acc = hist.history['val_acc']
xc = range(1000)


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

print(classification_report(np.argmax(y_test, axis=1), y_pred, target_names=labels))
print(confusion_matrix(np.argmax(y_test, axis=1), y_pred))


predicted = np.argmax(y_pred, axis=1)
print(predicted)


