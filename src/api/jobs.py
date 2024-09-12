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
    Description_HTML: str

@router.get("/fetch", response_model=list[Job])

def fetch_Jobs(    
    job_name: str = "",
    job_experience: str = "",
    job_degree: str = ""
    ):

    stmt = (
        sqlalchemy.select(
            db.Jobs.c.Experience_Level,
            db.Jobs.c.Employment_Type,
            db.Jobs.c.Industry,
            db.Jobs.c.Title,
            db.Jobs.c.Description,
            db.Jobs.c.Company,
            db.Jobs.c.Image,
            db.Jobs.c.Day_Posted,
            db.Jobs.c.Job_Location,
            db.Jobs.c.Job_Link,
            db.Jobs.c.Description_HTML,
            db.Jobs.c.Job_Experience,
            db.Jobs.c.Job_Degree,
        )
    )

    # filter only if name parameter is passed
    if job_name != "":
        stmt = stmt.where(db.search_orders_view.c.customer_name.ilike(f"%{job_name}%"))
        stmt_total_rows = stmt_total_rows.where(db.search_orders_view.c.customer_name.ilike(f"%{job_name}%"))
    
    if job_experience != "":
        stmt = stmt.where(db.search_orders_view.c.item_sku.ilike(f"%{job_experience}%"))
        stmt_total_rows = stmt_total_rows.where(db.search_orders_view.c.item_sku.ilike(f"%{job_experience}%"))

    if job_degree != "":
        stmt = stmt.where(db.search_orders_view.c.item_sku.ilike(f"%{job_degree}%"))
        stmt_total_rows = stmt_total_rows.where(db.search_orders_view.c.item_sku.ilike(f"%{job_degree}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        filtered_job_list = []
        for row in result:
            filtered_job_list.append(
            {
                "Experience_Level": row.Experience_Level,
                "Employment_Type": row.Employment_Type,
                "Industry": row.Industry,
                "Title": row.Title,
                "Description": row.Description,
                "Company": row.Company,
                "Image": row.Image,
                "Day_Posted": row.Day_Posted,
                "Job_Location": row.Job_Location,
                "Job_Link": row.Job_Link,
                "Description_HTML": row.Description_HTML,
                "Job_Experience": row.Job_Experience,
                "Job_Degree": row.Job_Degree,
            }
            )
    
    return filtered_job_list
