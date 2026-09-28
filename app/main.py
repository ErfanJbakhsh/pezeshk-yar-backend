from fastapi import FastAPI
from app.routes import doctors


app = FastAPI()

app.include_router(doctors.router)
