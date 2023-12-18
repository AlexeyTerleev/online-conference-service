from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import all_routers
from config import settings

app = FastAPI(title=settings.PROJECT_NAME)

origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)
