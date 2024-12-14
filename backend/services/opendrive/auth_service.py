# backend\services\opendrive\auth_service.py
from backend.utils.http_client import HTTPClient
from backend.models.opendrive.auth_models import LoginResponse
from backend.core.config import OPENDRIVE_BASE_URL, OPENDRIVE_USERNAME, OPENDRIVE_PASSWORD
from backend.core.opendrive_interface import IAuthService

class AuthService(IAuthService):
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.username = OPENDRIVE_USERNAME
        self.password = OPENDRIVE_PASSWORD
        self.http = HTTPClient(base_url=self.base_url)
        self.session_id = None

    async def login(self) -> LoginResponse:
        data = {
            "username": self.username,
            "passwd": self.password
        }
        response = await self.http.post("/session/login.json", json=data)
        response.raise_for_status()
        login_data = LoginResponse(**response.json())
        self.session_id = login_data.SessionID
        print(f"Loging in using authkey: {self.session_id}")
        return login_data

    async def ensure_session(self):
        if not self.session_id:
            await self.login()
        else:
            # Check if session_id is valid
            data = {
                "session_id": self.session_id
            }
            try:
                response = await self.http.post("/session/check.json", json=data)
                response.raise_for_status()
                if response.json().get('Error') == 1:
                    self.session_id = None
                    await self.login()
            except:
                self.session_id = None
                await self.login()

    async def check_session(self, session_id: str) -> dict:
        data = {
            "session_id": session_id
        }
        response = await self.http.post("/session/exists.json", json=data)
        return response.json()
