from fastapi import FastAPI
from routes import doctors


app = FastAPI()

app.include_router(doctors.router)
