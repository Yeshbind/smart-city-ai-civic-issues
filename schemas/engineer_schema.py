from pydantic import BaseModel

class EngineerRegister(BaseModel):
    userId: str
    password: str
    ward: str

class EngineerLogin(BaseModel):
    userId: str
    password: str

class EngineerResetPassword(BaseModel):
    userId: str
    newPassword: str