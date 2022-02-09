# import joblib
import os
import random
import pandas as pd

MODEL_PATH = os.getenv('MODEL_PATH')

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
