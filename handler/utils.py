from pydantic import BaseModel
from typing import Literal
import random

def get_predictions(pred_df):
    return random.random()


class RequestModel(BaseModel):
    abuse_type: Literal['MSG', 'PRF']           # Source of report
    report_text_len: int                        # chars length of report
    profile_rating: float                       # rating of the user sending the report
    popularity: Literal[0,1,2,3,4,5]            # popularity of user sending the report
    lifetime_matches_created: int               # number of matches for user sending the report
    
