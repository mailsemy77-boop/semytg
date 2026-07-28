# main.py
import json
import time
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

BACKGROUND_API = "https://tg2num.noob73613.workers.dev/"
TIMEOUT_SECONDS = 10

@app.get("/semy")
async def semy_api(id: str = Query(None, description="Enter phone number with country code")):

    # Agar ID nahi diya
    if not id:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Please provide 'id' parameter. Example: /semy?id=+919876543210",
                "developer": "semy"
            }
        )

    try:
        # Background API call with timeout
        response = requests.get(
            BACKGROUND_API,
            params={"term": id},
            timeout=TIMEOUT_SECONDS
        )

        # Agar API ne error status code diya
        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "api error",
                    "developer": "semy"
                }
            )

        data = response.json()

        # Check response
        if data.get("success") and data.get("msg") == "Details fetched":
            return {
                "status": "success",
                "number": data.get("number"),
                "country": data.get("country"),
                "country_code": data.get("country_code"),
                "developer": "semy"
            }
        else:
            # Not found ya koi aur fail
            return {
                "status": "false",
                "developer": "semy"
            }

    except requests.Timeout:
        # Timeout case
        return {
            "status": "false",
            "developer": "semy"
        }

    except Exception as e:
        # Koi bhi unexpected error
        return JSONResponse(
            status_code=500,
            content={
                "status": "api error",
                "developer": "semy"
            }
        )