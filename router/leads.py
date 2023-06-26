from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List
from util.config import Tags

from services.scrape import get_outscraper_info
import util.logger as logger


leadroute = APIRouter()
my_logger = logger.get_logger("leads.py")

# Scrape Leads
@leadroute.get("/", response_model=list[List], 
        tags=[Tags.leads], 
        summary="Generate leads",
        description="Generate leads from a Google maps search, email all users who do not have a website, and create a CSV file with the results.",
        response_description="Successfully generated and email leads list.",
        )
async def get_leads(query: List[str] = Query(
    example=[
        "restaurants dallas usa",
        "bars dallas usa",
    ])):
    try:
        results = get_outscraper_info(query)
        my_logger.info("Retrieved dataz from scraper")
        return results
    except Exception as e:
        my_logger.error("Error getting email info" + str(e))
        raise HTTPException(
            status_code=400, 
            detail="Unprocessabile entity" + str(e),
            headers={"X-Error": "LG400"})



@leadroute.get("/attachment",
        tags=[Tags.leads], 
        )
async def get_csv():
    """
    Download csv file generated from leads endpoint:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    file_like = open("./filename.csv", mode="rb")
    response = StreamingResponse(file_like, media_type="text/csv")
    # response.headers["Content-Disposition"] = f"inline; filename=export.csv"
    response.headers["Content-Disposition"] = f"attachment; filename=export.csv"
    my_logger.info("Retrieved data from existing csv file")
    return response
