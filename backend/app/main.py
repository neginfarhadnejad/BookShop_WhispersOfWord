from fastapi import FastAPI
from app.db.database import engine
from app.api import user as user_route   
from app.models import user as user_model


app = FastAPI()

user_model.Base.metadata.create_all(bind=engine)
app.include_router(user_route.router)


@app.get("/")
def root():
    return {"message": "Welcome to BookShop IAM Service"}
