from fastapi import FastAPI
from loguru import logger
from app.core.db.database import init_db  

from app.api.routes.user_route import router as user_router
from app.api.routes.admin_route import router as admin_router



def create_app() -> FastAPI:
    app = FastAPI(title="BookShop IAM Service")

    init_db()

    app.include_router(user_router,prefix="/users" )
    app.include_router(admin_router, prefix="/admins", tags=["admins"])


    @app.get("/")
    def root():
        return {"message": "Welcome to BookShop IAM Service"}

    logger.info("App initialized successfully.")
    return app


app = create_app()
