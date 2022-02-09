import pandas as pd
import json
from lib2to3.pytree import Base
import string
from pydantic import BaseModel
from typing import Literal
from ml.constants import CATEGORICAL_FEATURES, NUMERICAL_FEATURES

def get_pred_df(data):
    df = pd.DataFrame([eval(x.json()) for x in data])
    for col in CATEGORICAL_FEATURES:
        df = pd.concat([pd.get_dummies(df[col],prefix=col),df],axis=1).drop([col],axis=1)
    for col in NUMERICAL_FEATURES:
        # Add scaling/normalization
        pass
    # Other processing
    return df.to_dict()

class RequestBody(BaseModel):
    abuse_type: Literal['MSG', 'PRF']           # Source of report
    report_text_len: int                        # chars length of report
    profile_rating: float                       # rating of the user sending the report
    popularity: Literal[0,1,2,3,4,5]            # popularity of user sending the report
    lifetime_matches_created: int               # number of matches for user sending the report
    
class SubmittedTask(BaseModel):
    task_id: str
    status: str


class FetchedScore(BaseModel):
    task_id: str
    status: str
    score: float