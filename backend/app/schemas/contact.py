from pydantic import BaseModel, EmailStr, field_validator


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if len(v.strip()) < 10:
            raise ValueError("Message must be at least 10 characters")
        return v.strip()


class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool

    model_config = {"from_attributes": True}