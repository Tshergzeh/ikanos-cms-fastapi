from sqlmodel import Field, SQLModel
from datetime import datetime

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field()
    image: str = Field()
    created_by: str = Field()
    last_modified_by: str = Field()
    is_published: bool = Field(default=False)
    approved_by: str | None = Field()
    approved_at: datetime | None = Field()

class ServiceUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    image: str | None = None
    last_modified_by: str 
    is_published: bool = False

class ServiceApproveInput(SQLModel):
    approved_by: str 

class ServiceApproveFinal(ServiceUpdate):
    last_modified_by: str
    is_published: bool = True
    approved_by: str
    approved_at: datetime = datetime.now()
