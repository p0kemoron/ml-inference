from pydantic import BaseModel
from typing import Literal, List


class RequestBody(BaseModel):
    """Extends pydantic BaseModel to validate client incoming requests
    """    
    abuse_type: Literal["MSG", "PRF"]                   # Source of report
    report_text_len: int                                # chars length of report
    profile_rating: float                               # rating of the user sending the report
    popularity: Literal[0, 1, 2, 3, 4, 5]               # popularity of user sending the report
    lifetime_matches_created: int                       # number of matches for user sending the report

    # Check for constraints and raise errors if not met


class SubmittedTask(BaseModel):
    task_id: str
    status: str


class FetchedScore(BaseModel):
    task_id: str
    status: str
    score: List[float]
