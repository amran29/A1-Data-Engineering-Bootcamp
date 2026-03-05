from pydantic import BaseModel, EmailStr
from typing import Optional, List

# النموذج الأساسي (المشترك)
class UserBase(BaseModel):
    username: str
    email: EmailStr

# البيانات المطلوبة عند إنشاء حساب جديد
class UserCreate(UserBase):
    password: str

# البيانات التي ستعود في الرد (Response)
class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True # يسمح لـ Pydantic بقراءة بيانات SQLAlchemy Models

# نموذج خاص ببيانات التوكن (Login)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None