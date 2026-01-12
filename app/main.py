from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import notes, versions, auth

app = FastAPI(title="Notes API with Version History")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(versions.router)
