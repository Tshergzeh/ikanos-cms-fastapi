from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password: str = Field()
    is_admin: bool | None = Field(default=False)