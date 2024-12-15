from fastapi import APIRouter, HTTPException, Depends
from backend.services.opendrive.auth_service import AuthService
from backend.models.opendrive.auth_models import (
    LoginRequest,
    SessionCheckRequest,
    SessionCheckResponse,
    UserInfoResponse,
)
from backend.core.opendrive_interface import IAuthService

router = APIRouter()


def get_auth_service() -> IAuthService:
    return AuthService()


@router.post("/login")
async def login(
    login_request: LoginRequest = Depends(),
    service: IAuthService = Depends(get_auth_service),
):
    try:
        login_details = await service.login(login_request)
        return login_details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/session/check", response_model=SessionCheckResponse)
async def check_session(
    session_check: SessionCheckRequest = Depends(),
    service: IAuthService = Depends(get_auth_service),
) -> SessionCheckResponse:
    try:
        response = await service.check_session(session_check.session_id)
        return SessionCheckResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/info", response_model=UserInfoResponse)
async def get_user_info(
    session_id: str, service: IAuthService = Depends(get_auth_service)
) -> UserInfoResponse:
    try:
        user_info = await service.get_user_info(session_id)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
