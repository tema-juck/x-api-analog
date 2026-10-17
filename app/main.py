from fastapi import FastAPI
from posts.routes import router as post_router

app = FastAPI(
    title="X-Analog API",
    description="API for pet-project",
    version="0.1.0",
    openapi_tags=[{"name": "Posts", "description": "Control your Projects"}],
)


app.include_router(post_router)
