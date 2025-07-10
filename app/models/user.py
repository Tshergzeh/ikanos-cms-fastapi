from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    hashed_password: str = Field()
    is_admin: bool | None = Field(default=False)

class UserCreate(SQLModel):
    username: str
    password: str
    is_admin: bool = False