# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from collections import Counter


data = pd.read_csv('datasets/zero_imputed_dataset.csv', delimiter=',', low_memory=False)


def splitXy(data):
    X = data.iloc[:, 0:200]
    y = data.iloc[:, -1]
    return X, y

X, y = splitXy(data)

X = X.astype(float)
y = y.astype(int)

sm = SMOTE(random_state = 99)
print('Original dataset shape {}'. format(Counter(y)))

X_res, y_res = sm.fit_sample(X, y)
print('Resampled dataset shape {}'. format(Counter(y_res)))

#newset = pd.DataFrame(X_res, columns = X.columns)
#newset = pd.DataFrame(X_res)
#newset.to_csv('datasets/_X.csv', sep=',', encoding='utf-8')
