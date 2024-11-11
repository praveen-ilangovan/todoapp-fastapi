"""

"""

from fastapi import APIRouter

router = APIRouter()

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.get("/")
async def auth_page() -> dict[str, str]:
    return {"message": "Auth page"}
