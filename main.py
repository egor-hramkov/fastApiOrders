from fastapi import FastAPI

from apps.user import routes as user_routes
from apps.auth import routes as auth_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
