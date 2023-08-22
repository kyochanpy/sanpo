from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import sanpo

app = FastAPI(debug=True)

app.include_router(sanpo.router)

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)