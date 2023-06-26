import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from util.config import settings

import util.logger as logger
from fastapi.middleware.cors import CORSMiddleware
from router.leads import leadroute
from router.emails import emailroute

description = """
LeadGeneration API helps automate generate leads. 🚀

## Leads

You can **generate leads**.

## Emails

You can **send emails to cold leads**.
You can **create contacts for marketing campaigns**.

You will be able to:

* **Create users** (_not implemented_).
* **Send bulk emails** (_not implemented_).
* **Send marketing emails** (_not implemented_).
* **Send warm lead emails** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Leads",
        "description": "Lead generation is the process of identifying and nurturing potential customers to convert them into buyers.",
        "externalDocs": {
            "description": "Leads external docs",
            "url": "https://app.outscraper.com/api-docs#tag/Email-Related",
        },
    },
    {
        "name": "Emails",
        "description": "Automated cold emails - a way to reach out to potential customers and generate leads.",
        "externalDocs": {
            "description": "Email external docs",
            "url": "https://developers.brevo.com/reference/getting-started-1",
        },
    },
]

app = FastAPI(
    title = "LeadGenerationAPI",
    description = description,
    version = "0.0.1",
    terms_of_service = "http://example.com/terms/",
    contact={
        "name": "Ambitious Concepts Lab",
        "url": "https://www.ambitiousconceptslabs.com",
        "email": "info@ambitiousconept.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local environment"},
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    openapi_tags = tags_metadata
    )


my_logger = logger.get_logger("main.py")

app.include_router(leadroute, prefix="/leads")
app.include_router(emailroute, prefix="/emails")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = {}

class TimedRoute(APIRouter):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

router = APIRouter(route_class=TimedRoute)

# You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.
@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get('/healthcheck', status_code=200)
def perform_healthcheck():
    '''
    Simple route for the GitHub Actions to perform healthchecks on.

    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check

    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.

    Additionally, it also returns a JSON response in the form of:

    {
      'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }

