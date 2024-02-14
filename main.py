from fastapi import FastAPI

from apps.user import routes as user_routes
from apps.auth import routes as auth_routes
from kafka_layer.consumer import run_consumer

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)


@app.on_event("startup")
async def startup_event():
    run_consumer()
