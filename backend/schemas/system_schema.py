from pydantic import BaseModel, Field
from typing import Optional

class ClientIPResponse(BaseModel):
    """客戶端 IP 響應"""
    ip: str = Field(..., description='客戶端 IP 地址')
    
    class Config:
        schema_extra = {
            "example": {
                "ip": "127.0.0.1"
            }
        }

class ErrorResponse(BaseModel):
    """錯誤響應"""
    message: str = Field(..., description='錯誤信息') 