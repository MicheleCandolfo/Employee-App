from fastapi import FastAPI
import models

from database import engine
from typing import Annotated
from routers import auth, admin, users

# creates an instance of the FastAPI class
app = FastAPI()

# creates all of the tables in the database based on the models we created
models.Base.metadata.create_all(bind=engine)


# this lines add ther routers to the app, 
# so that the app can use the endpoints todos, auth, admin, users
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)

# In summary the main file creates an instance of the FastAPI class,
# creates all of the tables in the database based on the models we created,
# that meand we create an app with a database connection
# it also implements all the routers we created in the routers folder into the app