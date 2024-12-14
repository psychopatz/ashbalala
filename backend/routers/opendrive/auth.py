from fastapi import APIRouter, HTTPException, Depends
from backend.services.opendrive.auth_service import AuthService
from backend.models.opendrive.auth_models import LoginRequest, SessionCheckRequest, SessionCheckResponse
from backend.core.opendrive_interface import IAuthService

router = APIRouter()

def get_auth_service() -> IAuthService:
    return AuthService()

@router.post("/login")
async def login(
    login_request: LoginRequest = Depends(),
    service: IAuthService = Depends(get_auth_service)
):
    if login_request.session_id:
        service.session_id = login_request.session_id
        return {"message": "Session ID set", "session_id": service.session_id}
    else:
        login_details = await service.login()
        return login_details

@router.post("/session/check", response_model=SessionCheckResponse)
async def check_session(
    session_check: SessionCheckRequest = Depends(),
    service: IAuthService = Depends(get_auth_service)
) -> SessionCheckResponse:
    try:
        response = await service.check_session(session_check.session_id)
        return SessionCheckResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))