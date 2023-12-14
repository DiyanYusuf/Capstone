from fastapi import FastAPI, UploadFile, File, Depends
from fastapi import HTTPException, Path
from fastapi.responses import JSONResponse
import os
#from dotenv import load_dotenv
import json
from typing import Annotated, Optional
from fastapi import Query

# Database Stuff
from database import SessionLocal, engine
import models
#from schemas import FileCreate
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from starlette.responses import StreamingResponse
import io

# Authorization Stuff
import auth
from auth import get_current_user
from starlette import status

models.Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

app = FastAPI()

app.include_router(auth.router)

db_dependency = Annotated[Session, Depends(get_db)] 
user_dependency = Annotated[dict, Depends(get_current_user)]

# Fetch sensitive information from environment variables
#key_json_content = os.getenv('KEY_CONFIG')
#bucket_name = os.getenv('BUCKET_NAME')

#client = storage.Client.from_service_account_json("")
#bucket_name = ''

# Convert the environment variable containing JSON to a Python dictionary
#key_info = json.loads(key_json_content)

# Use the fetched values
#KEY = {}
#client = storage.Client.from_service_account_info(KEY)

@app.get("/", status_code=status.HTTP_200_OK)
async def verify_status(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Forbidden. You Need to Login First')
    return {"User": user}