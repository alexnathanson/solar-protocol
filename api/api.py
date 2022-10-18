from fastapi import FastAPI
from typing import Union

app = FastAPI(title="solar-protocol", docs_url="/docs")

@app.get("/")
def root():
    return {"message": "Hello World 👋"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
