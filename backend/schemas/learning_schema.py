from pydantic import BaseModel, Field
from typing import List, Optional
from flask_openapi3 import FileStorage
from datetime import datetime

class SectionPath(BaseModel):
    """區塊路徑參數"""
    section_id: int = Field(..., description='區塊ID')

class SubsectionPath(BaseModel):
    """子區塊路徑參數"""
    subsection_id: int = Field(..., description='子區塊ID')

class SectionCreateSchema(BaseModel):
    """創建主標題區塊"""
    title: str = Field(..., description='標題')
    description: str = Field(..., description='描述')
    sort_order: int = Field(0, description='排序順序')

class SubsectionCreateSchema(BaseModel):
    """創建次標題區塊"""
    section_id: int = Field(..., description='主區塊ID')
    title: str = Field(..., description='標題')
    content: str = Field(..., description='內容')
    images: List[str] = Field(default=[], description='圖片URL列表')
    sort_order: int = Field(0, description='排序順序')

class SectionUpdateSchema(BaseModel):
    """更新主標題區塊"""
    title: Optional[str] = Field(None, description='標題')
    description: Optional[str] = Field(None, description='描述')
    sort_order: Optional[int] = Field(None, description='排序順序')

class SubsectionUpdateSchema(BaseModel):
    """更新次標題區塊"""
    title: Optional[str] = Field(None, description='標題')
    content: Optional[str] = Field(None, description='內容')
    images: Optional[List[str]] = Field(None, description='圖片URL列表')
    sort_order: Optional[int] = Field(None, description='排序順序')

class FileUploadResponse(BaseModel):
    """圖片上傳響應"""
    url: str = Field(..., description='圖片URL')
    message: Optional[str] = Field(None, description='響應信息')

class ErrorResponse(BaseModel):
    """錯誤響應"""
    message: str = Field(..., description='錯誤信息')

class UploadFileForm(BaseModel):
    """文件上傳請求"""
    file: FileStorage = Field(
        ...,
        description='圖片文件 (支援 jpg、png、gif、webp 格式，最大 5MB)',
    )

    class Config:
        arbitrary_types_allowed = True 