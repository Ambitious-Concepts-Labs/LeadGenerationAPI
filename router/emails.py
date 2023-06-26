from fastapi import APIRouter, Body, HTTPException
from util.config import Tags

import util.logger as logger
import services.sendEmail as sendEmail


emailroute = APIRouter()
my_logger = logger.get_logger("route_email.py")

# Send Emails
@emailroute.post("/cold", 
        tags=[Tags.emails], 
        summary="Send Emails",
        description="Send emails to leads who do not have a website.",
        response_description="Successfully email leads.",
        )
async def send_email(query: str = Body(
    example= {
        "email": "dhoseadesigns@gmail.com",
        "name": "Dominique Hosea",
        "template": 2,
        "params": {
            "BUSINESSNAME": "Test Business",
            "BUSINESSTYPE": "Gym",
            "BUSINESSLOGO": "https://unsplash.com/photos/iBLWICTNt0Y",
            "RATING": 4.5,
            "REVIEWS": 200,
            "REVIEWSPERSCORE": "{'1': 7, '2': 8, '3': 11, '4': 23, '5': 232}",
            "BUSINESSSTATUS": "OPERATIONAL",
            "OTHER": "{'LGBTQ+ friendly': True}",
            "AMENITIES": "{'Gender-neutral restroom': True, 'Restroom': True}",
            "ATMOSPHERE": "{'Cozy': True, 'Hip': True, 'Romantic': True, 'Trending': True}",
            "CROWD": "{'Family-friendly': True, 'LGBTQ+ friendly': True, 'Tourists': True, '…",
            "OWNERTITLE": "Petra and the Beast",
            "OWNERLINK":"https://www.google.com/maps/contrib/101648973239882470567"
        }
        })):           
    try:
        results = sendEmail.send_email(query["email"], query["template"])
        my_logger.info("Sent email to: " + query["email"])
        return results
    except Exception as e:
        my_logger.error("Error getting email info" + str(e))
        raise HTTPException(
            status_code=400, 
            detail="Unprocessabile entity" + str(e),
            headers={"X-Error": "LG400"})

