from pydantic import BaseModel, Field
from typing import Optional

class BotCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    sort_order: int = Field(0, description='排序順序')
    icon: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    is_default: bool = False
    message: Optional[str] = None

class BotUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    sort_order: Optional[int] = None
    icon: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    message: Optional[str] = None

class BotPath(BaseModel):
    bot_id: int = Field(..., description='Bot ID')

class BotQuerySchema(BaseModel):
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None 