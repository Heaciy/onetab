from pydantic import BaseModel
from pydantic import Field, EmailStr
from pydantic import model_validator


class UserBase(BaseModel):
    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(max_length=32)
    password_again: str = Field(max_length=32)
    # TODO: 增加字段校验

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        pw1 = self.password
        pw2 = self.password_again
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class UserAuth(BaseModel):
    username: str = Field(max_length=10)
    password: str = Field(max_length=32)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


if __name__ == "__main__":
    user = UserCreate(username="heaciy", email="heaciyyy@qq.com",
                      password="123456", password_again="1234567")
    print(user)
    print(user.model_dump(exclude=["password_again"]))
