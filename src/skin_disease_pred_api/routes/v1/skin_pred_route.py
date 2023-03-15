import os
import uuid
import logging
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Request
)
from starlette.responses import JSONResponse
from skin_disease_pred_api.utils.skin_disease_pred import disease_prediction
skin_pred_router = APIRouter(
    prefix="/v1",
    tags=["disease_pred"],
    responses={
        404: {"description": "Not found"}
    }
)
@skin_pred_router.post("/disease_pred")
async def callback_post_api(request: Request):
    request_json = await request.json()
    bucket_name="bucket_name"
    file_name="file_name"
    logging.info("Calling Diseases prediction model")
    resp = disease_prediction(bucket_name,file_name)
    return JSONResponse(resp, status_code=200)