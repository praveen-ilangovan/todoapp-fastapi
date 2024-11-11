"""

"""

# Project specific imports
from fastapi import FastAPI

# Local imports
from .database.database import ENGINE
from .database import model
from .routers import auth, todos

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#
model.BASE.metadata.create_all(bind=ENGINE)

#-----------------------------------------------------------------------------#
# App
#-----------------------------------------------------------------------------#
app = FastAPI()
app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(todos.router, tags=["Todos"], prefix="/todos")

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index() -> dict[str, str]:
    return {'message': 'Welcome ToDos App powered by sqlite'}
