from fastapi import FastAPI

from apps.user import routes as user_routes
from apps.auth import routes as auth_routes
from apps.items import routes as item_routes
from apps.orders import routes as order_routes
from kafka_layer.consumer import run_consumer
import concurrent.futures as pool

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(item_routes.router)
app.include_router(order_routes.router)

executor = pool.ThreadPoolExecutor(max_workers=1)


@app.on_event("startup")
async def startup_event():
    executor.submit(run_consumer)
