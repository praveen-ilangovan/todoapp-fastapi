"""
Jinja Templating
"""
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#-----------------------------------------------------------------------------#
# Templates
#-----------------------------------------------------------------------------#
TEMPLATES = Jinja2Templates(directory="fastapi_udemy_course/proj03_todo/templates")

def mount_static_files(app):
    app.mount("/static", StaticFiles(directory="fastapi_udemy_course/proj03_todo/static"), name="static")
