from fastapi import FastAPI
from a2wsgi import ASGIMiddleware
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 👋"}

@app.post("/items/")
async def update_device(device: Device):
    return device


# mod_wsgi expects the name 'application' by default
application = ASGIMiddleware(app)
