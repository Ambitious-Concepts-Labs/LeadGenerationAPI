import csv
import json
import motor.motor_asyncio
import os

from fastapi.encoders import jsonable_encoder
from outscraper import ApiClient

import util.config as config
import util.logger as logger

my_logger = logger.get_logger("scrape.py")
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017" or os.environ["MONGODB_URL"])
db = client.leadGeneration

async def get_outscraper_info(queries=[], business_type=None, location_name=None, limit=1):
    try:
        api_client = ApiClient(api_key=config.keys["outscraper_api_key"])
        res = "" 
        results = ""
        getMarketingInfo = False

        # Search with many queries (batching)
        if queries is not []:
            if config.redis_cache.exists("outscraper_maps"):
                my_logger.info("Retrieved data from redis")
                res = config.redis_cache.get("outscraper_maps")
                res = json.loads(res)

                # Find info about owner possibly improve site or marekting
                if (res[0][0]["site"] != "null" and getMarketingInfo is True):
                    results = config.redis_cache.get("outscraper_emails")
                else:
                    results = res
                return results
            else:
                # Return business info as list
                res = api_client.google_maps_search(queries, language="en", limit=limit)
                my_logger.info("Pulling data from Google Maps Search")

                # Save dat to redis as str
                config.redis_cache.setex("outscraper_maps", 1000, json.dumps(res))
                my_logger.info("Saving data to redis")

                # convert data to dict to be processed
                business_mappings = {}

                # Only interates through the first Query
                for index, element in enumerate(res[0]):
                    business_mappings[index] = element

                # Map data to save to db
                for x in business_mappings:
                    # Needs to have a model
                    data = {
                        "query": business_mappings[x]["query"],
                        "name": business_mappings[x]["name"],
                        "full_address": business_mappings[x]["full_address"],
                        "borough": business_mappings[x]["borough"],
                        "popular_times": business_mappings[x]["popular_times"] or "null",
                        "site": business_mappings[x]["site"] or "null",
                        "phone": business_mappings[x]["phone"] or "null",
                        "type": business_mappings[x]["type"] or "null",
                        "logo": business_mappings[x]["logo"] or "null",
                        "description": business_mappings[x]["description"] or "null",
                        "category": business_mappings[x]["category"] or "null",
                        "subtypes": business_mappings[x]["subtypes"] or "null",
                        "rating": business_mappings[x]["rating"] or "null",
                        "reviews": business_mappings[x]["reviews"] or "null",
                        "reviews_per_score": str(business_mappings[x]["reviews_per_score"]),
                        "rating": business_mappings[x]["rating"] or "null",
                        "working_hours": business_mappings[x]["working_hours"] or "null",
                        "business_status": business_mappings[x]["business_status"] or "null",
                        "other": str(business_mappings[x]["about"]["Other"]) or "null",
                        "amenities": str(business_mappings[x]["about"]["Amenities"]) or "null",
                        "atmosphere": str(business_mappings[x]["about"]["Atmosphere"]) or "null",
                        "crowd": str(business_mappings[x]["about"]["Crowd"]) or "null",
                        "owner_title": business_mappings[x]["owner_title"] or "null",
                        "owner_link": business_mappings[x]["owner_link"] or "null"
                        }
                   
                    existing_business_mappings = await db["business_mapping"].find_one({"name": data["name"]})
                    if (existing_business_mappings):
                        my_logger.info("Existing data found in db: " + str(existing_business_mappings["_id"]))
                        continue
                    
                    # Save business info to db 
                    await db["business_mapping"].insert_one(jsonable_encoder(data))
                    my_logger.info("Saving maps data to db")

                    # Find info about owner possibly improve site or marekting
                    if (data["site"] != "null" and getMarketingInfo is True):
                        
                        # Return business contact info as list
                        data_emails = api_client.emails_and_contacts([data["site"]])
                        my_logger.info("Pulling data from email and contacts")

                        # Save dat to redis as str
                        config.redis_cache.setex("outscraper_emails", 1000, json.dumps(res))
                        my_logger.info("Saving data to redis")

                        # Map data to save to db
                        processed_email_data = {
                            "query": data_emails[0]["query"],
                            "external_emails": str(data_emails[0]["external_emails"]),
                            "emails": str(data_emails[0]["emails"]),
                            "socials": str(data_emails[0]["socials"]),
                            "phones": str(data_emails[0]["phones"])
                        }

                        # Save business contact info to db 
                        await db["business_emails"].insert_one(jsonable_encoder(processed_email_data))
                        my_logger.info("Saving email data to db")
                        return data_emails
                    else:
                        results = data
                        print("How will we contact them")

                
                # Write to csv file
                with open("business_leads.csv", "w") as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow(res)
                    my_logger.info("Writing data to csv")

        # Search for businesses in specific locations:
        if business_type is not None:
            res = api_client.google_maps_search(
                business_type + " dallas usa", limit=limit, language="en"
            )
            return res

        if location_name is not None:
            res = api_client.google_maps_search(location_name, limit=limit)
            return res

        if location_name is not None and business_type is not None:
            res = api_client.google_maps_search(
                business_type + " " + location_name, limit=limit
            )
            return res

        # Get data of the specific place by id
        # result = api_client.google_maps_search('ChIJrc9T9fpYwokRdvjYRHT8nI4', language='en')
        return results
    except Exception as e:
        my_logger.error("Error processing data: " + str(e))
        return None