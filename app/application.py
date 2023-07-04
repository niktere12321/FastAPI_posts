import uvicorn
from fastapi import FastAPI

from app.api.routers import users_router, posts_router, likes_router, dislikes_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users_router)
    app.include_router(posts_router, prefix="/posts", tags=["Posts"])
    app.include_router(likes_router, prefix="/likes", tags=["Likes"])
    app.include_router(dislikes_router, prefix="/dislikes", tags=["Dislikes"])
    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8080)
