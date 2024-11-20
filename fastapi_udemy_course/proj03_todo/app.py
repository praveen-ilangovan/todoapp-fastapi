"""

"""

# Project specific imports
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse

# Local imports
from .database.database import ENGINE
from .database import model
from .routers import admin, auth, todos, user
from .templating import TEMPLATES, mount_static_files

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
app.include_router(user.router, tags=["Me"], prefix="/me")
mount_static_files(app)


#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)

@app.get("/health", tags=['Root'])
async def health_check() -> dict[str, str]:
    return {'health': 'ok'}
