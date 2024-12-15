from backend.utils.http_client import HTTPClient
from backend.models.opendrive.auth_models import (
    LoginResponse,
    LoginRequest,
    UserInfoResponse,
)
from backend.core.config import OPENDRIVE_BASE_URL
from backend.core.opendrive_interface import IAuthService


class AuthService(IAuthService):
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.http = HTTPClient(base_url=self.base_url)

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        if login_request.session_id:
            # Check if the provided session ID is valid
            session_check_response = await self.check_session(login_request.session_id)
            if session_check_response.get("result") == True:
                # Session is valid, fetch user info
                user_info = await self.get_user_info(login_request.session_id)

                return LoginResponse(
                    SessionID=login_request.session_id,
                    UserName=user_info.UserName,
                    UserFirstName=user_info.UserFirstName,
                    UserLastName=user_info.UserLastName,
                    AccType=user_info.AccType,
                    UserLang=user_info.UserLang,
                    Enable2FA=user_info.Enable2FA,
                    Active2FA=user_info.Enable2FA,  # Use the same value as Enable2FA for now
                    UserID=str(user_info.UserID),
                    IsAccountUser=user_info.IsAccountUser,
                    DriveName="",  # this information is not included in the get user info endpoint, so im leaving it blank
                    UserLevel=user_info.Level,
                    UserPlan=user_info.UserPlan,
                    FVersioning=user_info.FVersioning,
                    UserDomain="",  # this information is not included in the get user info endpoint, so im leaving it blank
                    PartnerUsersDomain=user_info.PartnerUsersDomain,
                    UploadSpeedLimit=0,  # this information is not included in the get user info endpoint, so im leaving it blank
                    DownloadSpeedLimit=0,  # this information is not included in the get user info endpoint, so im leaving it blank
                    UploadsPerSecond=0,  # this information is not included in the get user info endpoint, so im leaving it blank
                    DownloadsPerSecond=0,  # this information is not included in the get user info endpoint, so im leaving it blank
                )

            else:
                raise Exception("Invalid Session ID")
        else:
            if not login_request.username or not login_request.password:
                raise Exception(
                    "Username and password are required when no session_id provided"
                )
            data = {
                "username": login_request.username,
                "passwd": login_request.password,
            }
            response = await self.http.post("/session/login.json", json=data)
            response.raise_for_status()
            login_data = LoginResponse(**response.json())
            return login_data

    async def check_session(self, session_id: str) -> dict:
        data = {"session_id": session_id}
        response = await self.http.post("/session/exists.json", json=data)
        return response.json()

    async def get_user_info(self, session_id: str) -> UserInfoResponse:
        response = await self.http.get(f"/users/info.json/{session_id}")
        response.raise_for_status()

        # Parse the response with the correct model
        return UserInfoResponse(**response.json())
