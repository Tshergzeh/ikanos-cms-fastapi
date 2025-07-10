from sqlmodel import Field, SQLModel
from datetime import datetime

class Project(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True)
    project_image: str = Field()
    category_id: int = Field(index=True)
    created_by: str = Field()
    last_modified_by: str = Field()
    is_published: bool = Field(index=True, default=False)
    approved_by: str | None = Field()
    approved_at: datetime | None = Field()

class ProjectUpdate(SQLModel):
    project_image: str | None = None
    category_id: str | None = None
    last_modified_by: str | None = None
    is_published: bool | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None

