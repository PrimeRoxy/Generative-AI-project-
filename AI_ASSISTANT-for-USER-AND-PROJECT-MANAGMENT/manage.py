import logging
from fastapi import APIRouter, Body, HTTPException, Request, FastAPI
from assistant import process_assistant_task
from helper import verify_authentication

router = APIRouter()
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.post("/manage/")
async def manage(request: Request, user_query: str = Body(..., embed=True)):
    try:
        user_info, authorization_header = await verify_authentication(request)
        if not user_info:
            logging.error("Unauthorized access attempt.")
            raise HTTPException(status_code=401, detail="Unauthorized")

        result = await process_assistant_task(user_query, authorization_header)
        logging.debug(f"Process assistant task result: {result}")
        return result
    except HTTPException as e:
        logging.error(f"HTTP exception occurred: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
