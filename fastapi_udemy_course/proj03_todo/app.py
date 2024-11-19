"""

"""

# Project specific imports
from fastapi import FastAPI

# Local imports
from .database.database import ENGINE
from .database import model
from .routers import admin, auth, todos, user

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
app.include_router(admin.router, tags=["Admin"], prefix="/admin")
app.include_router(user.router, tags=["Me"], prefix="/me1")



#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
# @app.get("/", tags=['Root'])
# async def index() -> dict[str, str]:
#     return {'message': 'Welcome ToDos App powered by sqlite'}

@app.get("/health", tags=['Root'])
async def health_check() -> dict[str, str]:
    return {'health': 'ok'}
