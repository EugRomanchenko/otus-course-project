from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from crud import delete_certificate_by_fingerprint
from db.engine import session_dependency


router = APIRouter(prefix="/delete", tags=["delete"])

templates = Jinja2Templates(directory="templates")


@router.post("/{fingerprint_id}", status_code=200)
async def delete_certificate(
        fingerprint_id: str,
        async_session: AsyncSession = Depends(session_dependency),
):
    await delete_certificate_by_fingerprint(session=async_session, fingerprint=fingerprint_id)
    return {"message": f"Certificate with fingerprint {fingerprint_id} was successfully deleted"}
