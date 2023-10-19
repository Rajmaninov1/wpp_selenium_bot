from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    password: str
    created_at: str
    updated_at: str
    deleted_at: str
    is_deleted: int
    is_active: int
    is_admin: int
    is_super_admin: int
    is_email_verified: int
    is_phone_verified: int
    is_email_subscribed: int
    is_phone_subscribed: int

    class Config:
        orm_mode = True


class Lead(BaseModel):
    id: int
    name: str
    score: float
    number_of_opinions: int
    phone_number: str
    website: str
    email: str
    country_scraped: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class UserLeads(BaseModel):
    id: int
    user_id: int
    lead_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class WhatsappMessagesHistory(BaseModel):
    id: int
    message: str
    user_id: int
    lead_id: int
    sent_at: str

    class Config:
        orm_mode = True


class WhatsappLists(BaseModel):
    id: int
    user_id: int
    lead_id: int
    list_name: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
