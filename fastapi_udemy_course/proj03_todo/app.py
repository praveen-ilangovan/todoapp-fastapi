"""

"""

# Project specific imports
from fastapi import FastAPI

# Local imports
from .database import BASE, ENGINE

# Connect to the database
BASE.metadata.create_all(bind=ENGINE)

app = FastAPI()

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index() -> dict[str, str]:
    return {'message': 'Welcome ToDos App powered by sqlite'}
