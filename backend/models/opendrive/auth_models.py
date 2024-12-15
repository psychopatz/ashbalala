from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    session_id: Optional[str] = None


class LoginResponse(BaseModel):
    SessionID: str
    UserName: str
    UserFirstName: str
    UserLastName: str
    AccType: str
    UserLang: str
    Enable2FA: str
    Active2FA: str
    UserID: str
    IsAccountUser: int
    DriveName: str
    UserLevel: str
    UserPlan: str
    FVersioning: str
    UserDomain: str
    PartnerUsersDomain: str
    UploadSpeedLimit: int
    DownloadSpeedLimit: int
    UploadsPerSecond: int
    DownloadsPerSecond: int


class SessionCheckRequest(BaseModel):
    session_id: str


class SessionCheckResponse(BaseModel):
    result: bool


class UserInfoResponse(BaseModel):
    UserID: Optional[int] = None
    AccessUserID: Optional[int] = None
    UserName: Optional[str] = None
    UserFirstName: Optional[str] = None
    UserLastName: Optional[str] = None
    PrivateKey: Optional[str] = None
    Trial: Optional[str] = None
    UserSince: Optional[str] = None
    BwResetLast: Optional[str] = None
    AccType: Optional[str] = None
    MaxStorage: Optional[str] = None
    StorageUsed: Optional[str] = None
    BwMax: Optional[str] = None
    BwUsed: Optional[str] = None
    FVersioning: Optional[str] = None
    FVersions: Optional[str] = None
    DailyStat: Optional[int] = None
    UserLang: Optional[str] = None
    MaxFileSize: Optional[str] = None
    Level: Optional[str] = None
    Enable2FA: Optional[str] = None
    UserPlan: Optional[str] = None
    TimeZone: Optional[str] = None
    MaxAccountUsers: Optional[str] = None
    IsAccountUser: Optional[int] = None
    CompanyName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Avatar: Optional[str] = None
    AvatarColor: Optional[str] = None
    AdminMode: Optional[int] = None
    DueDate: Optional[str] = None
    WebLink: Optional[str] = None
    PublicProfiles: Optional[int] = None
    RootFolderPermission: Optional[int] = None
    CanChangePwd: Optional[int] = None
    IsPartner: Optional[int] = None
    Partner: Optional[str] = None
    SupportUrl: Optional[str] = None
    PartnerUsersDomain: Optional[str] = None
    Suspended: Optional[bool] = None
    Affiliation: Optional[str] = None
    UserUID: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    PopUp: Optional[str] = None
    InvoiceAddress: Optional[str] = None
    UserAddress: Optional[str] = None
    CardAddress: Optional[str] = None
    Verified: Optional[str] = None
    SignupVerified: Optional[str] = None
    SubscriptionEndDate: Optional[str] = None
    TotalSpace: Optional[int] = None
    UsedSpace: Optional[int] = None
    UserEmail: Optional[str] = None
    Active2FA: Optional[str] = None
