import os

import uvicorn as uvicorn
from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/')
async def get_items():
    return {"Status": os.getenv("STATUS")}


if __name__ == "__main__":
    print("http://127.0.0.1:5000/api/")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
