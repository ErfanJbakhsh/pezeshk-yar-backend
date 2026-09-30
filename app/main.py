from fastapi import FastAPI
from routes import doctors, auth


app = FastAPI()

app.include_router(doctors.router)
app.include_router(auth.router)