from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from services.redis_service import RedisService
from settings.database import setup_redis

app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


@app.on_event("startup")
def startup_event():
    app.state.redis = setup_redis()
    app.state.redis_service = RedisService(app.state.redis)


@app.on_event("shutdown")
def shutdown_event():
    app.state.redis.close()