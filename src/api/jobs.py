import sqlalchemy
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    dependencies=[Depends(auth.get_api_key)],
)

class Job(BaseModel):
    Job_ID: str
    Experience_Level: str
    Employment_Type: str
    Industry: str
    Title: str
    Description: str
    Company: str
    Image: str
    Day_Posted: str
    Job_Location: str
    Job_Link: str
    
@router.get("/fetch", response_model=list[Job])
def fetch_Jobs():
    with db.engine.begin() as connection:
        job_list = connection.execute(sqlalchemy.select(db.Jobs).limit(10)).fetchall()
        
    # Convert each row to a dictionary by using _mapping to access keys and values
    result = [dict(row._mapping) for row in job_list]
    
    return result