from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

from config.cors_config import CorsConfig
from feature_engineering.controller.feature_engineering_controller import featureEngineeringRouter

load_dotenv()

app = FastAPI()

CorsConfig.middlewareConfig(app)

app.include_router(featureEngineeringRouter)

@app.get("/")
def first_test():
    return {"message": "Data Analysis Test"}
# Host는
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))