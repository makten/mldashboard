from os.path import dirname, join, abspath

__dir__ = dirname(abspath("__file__"))


model_path = './api/ml_operations/pickles/fault_classifier.h5'
#path_model_weight = './api/ml_operations/pickles/fault_classifier_weights.h5'
path_x_normalizer = './api/ml_operations/pickles/x_scalar.pickle'
path_y_normalizer = './api/ml_operations/pickles/y_labeler.pickle'
