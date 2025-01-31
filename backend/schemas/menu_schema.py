from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MenuBaseSchema(BaseModel):
    parent_id: Optional[int] = Field(None, description='父選單ID，不指定或為0時表示頂層選單')
    name: str = Field(..., description='選單名稱')
    path: Optional[str] = Field(None, description='路由路徑')
    component: Optional[str] = Field(None, description='組件路徑')
    icon: Optional[str] = Field(None, description='圖標名稱')
    sort_order: Optional[int] = Field(0, description='排序順序，數字越小越靠前')
    is_hidden: Optional[bool] = Field(False, description='是否隱藏')
    status: Optional[str] = Field('active', description='狀態：active-啟用，disabled-禁用')

class MenuCreateSchema(MenuBaseSchema):
    """創建選單請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'name': '系統管理',
                'path': '/system',
                'component': 'Layout',
                'icon': 'setting',
                'parent_id': 0,
                'sort_order': 0,
                'is_hidden': False,
                'status': 'active'
            }
        }

class MenuUpdateSchema(BaseModel):
    """更新選單請求參數"""
    parent_id: Optional[int] = Field(None, description='父選單ID，不指定或為0時表示頂層選單')
    name: Optional[str] = Field(None, description='選單名稱')
    path: Optional[str] = Field(None, description='路由路徑')
    component: Optional[str] = Field(None, description='組件路徑')
    icon: Optional[str] = Field(None, description='圖標名稱')
    sort_order: Optional[int] = Field(None, description='排序順序，數字越小越靠前')
    is_hidden: Optional[bool] = Field(None, description='是否隱藏')
    status: Optional[str] = Field(None, description='狀態：active-啟用，disabled-禁用')

    class Config:
        schema_extra = {
            'example': {
                'name': '系統管理',
                'path': '/system',
                'component': 'Layout',
                'icon': 'setting',
                'parent_id': 1,
                'sort_order': 1,
                'is_hidden': False,
                'status': 'active'
            }
        }

class MenuResponseSchema(MenuBaseSchema):
    """選單響應數據"""
    id: int = Field(..., description='選單ID')
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'parent_id': None,
                'name': '系統管理',
                'path': '/system',
                'component': 'Layout',
                'icon': 'setting',
                'sort_order': 0,
                'is_hidden': False,
                'status': 'active',
                'created_at': '2024-01-31 13:18:29',
                'updated_at': '2024-01-31 13:18:29'
            }
        } 