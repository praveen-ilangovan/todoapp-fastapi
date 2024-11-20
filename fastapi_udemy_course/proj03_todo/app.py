"""

"""

# Project specific imports
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Local imports
from .database.database import ENGINE
from .database import model
from .routers import admin, auth, todos, user

#-----------------------------------------------------------------------------#
# Templates
#-----------------------------------------------------------------------------#
TEMPLATES = Jinja2Templates(directory="fastapi_udemy_course/proj03_todo/templates")

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

app.mount("/static", StaticFiles(directory="fastapi_udemy_course/proj03_todo/static"), name="static")


#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index(request: Request):
    return TEMPLATES.TemplateResponse("home.html", {'request': request})

@app.get("/health", tags=['Root'])
async def health_check() -> dict[str, str]:
    return {'health': 'ok'}
