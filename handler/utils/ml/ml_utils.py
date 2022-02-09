import os
import random
import pandas as pd
from constants import CATEGORICAL_FEATURES, NUMERICAL_FEATURES

MODEL_PATH = os.getenv('MODEL_PATH')

def get_pred_df(data):
    df = pd.DataFrame([eval(x.json()) for x in data])
    for col in CATEGORICAL_FEATURES:
        df = pd.concat([pd.get_dummies(df[col],prefix=col),df],axis=1).drop([col],axis=1)
    for col in NUMERICAL_FEATURES:
        # Add scaling/normalization
        pass
    # Other processing
    return df.to_dict()


class ScoreReportsDummyModel():
    """[summary]
    """
    def __init__(self):
        # Here, model can be loaded from memory e.g.
        # self.model = joblib.load(MODEL_PATH)
        self.model = None
        self.model_params = None
    
    def train(self, model_param):
        # Import necessary libraries here
        pass

    def predict(self, pred_data):
        df = pd.DataFrame(pred_data)
        preds = []
        for i in range(len(df)):
            preds.append(random.random())
        return preds

    # Other functions can be added as required
