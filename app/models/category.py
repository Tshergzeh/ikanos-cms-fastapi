from sqlmodel import Field, SQLModel

class Category(SQLModel, table=True):
    category_id: int | None = Field(default=None, primary_key=True)
    category_name: str = Field(index=True)
    