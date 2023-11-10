from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, model_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    is_registered: bool = False
    password: str
    confirm_password: str


class UserLogin(UserBase):
    password: str


class UserInfo(UserBase):
    id: int
    fullname: str


class ResetPassword(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> "ResetPassword":
        password = self.password
        confirm_password = self.confirm_password
        if password is not None and password != confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")
        return self