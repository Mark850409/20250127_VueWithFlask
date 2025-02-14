from pydantic import BaseModel, Field
from typing import Optional
from flask_openapi3 import FileStorage

class LangflowPath(BaseModel):
    """Langflow 路徑參數"""
    flow_id: str = Field(..., description='Flow ID', example='ae94aa3d-ca48-4d32-afca-3913d1f1669c')
    file_name: str = Field(..., description='檔案名稱', example='測試流程.json')

class LangflowUploadPath(BaseModel):
    """Langflow 上傳路徑參數"""
    flow_id: str = Field(..., description='Flow ID', example='ae94aa3d-ca48-4d32-afca-3913d1f1669c')

class LangflowQuery(BaseModel):
    """Langflow 查詢參數"""
    flow_id: str = Field(..., description='Flow ID', example='ae94aa3d-ca48-4d32-afca-3913d1f1669c')

class LangflowUpload(BaseModel):
    """Langflow 上傳請求參數"""
    file: FileStorage = Field(..., description='上傳檔案')

class LangflowResponse(BaseModel):
    """Langflow 響應數據"""
    id: int = Field(..., description='ID')
    flow_id: str = Field(..., description='Flow ID')
    file_name: str = Field(..., description='檔案名稱')
    file_path: str = Field(..., description='檔案路徑')
    status: str = Field(..., description='狀態')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間')

class LangflowDownloadPath(BaseModel):
    """Langflow 下載路徑參數"""
    flow_id: str = Field(..., description='Flow ID', example='ae94aa3d-ca48-4d32-afca-3913d1f1669c')
    file_id: str = Field(..., description='檔案 ID', example='20240213085700')

class MonitorQuery(BaseModel):
    """監控查詢參數"""
    flow_id: str = Field(..., description='Flow ID')
    session_id: Optional[str] = Field(None, description='Session ID')
    sender: Optional[str] = Field(None, description='發送者')
    sender_name: Optional[str] = Field(None, description='發送者名稱')
    order_by: Optional[str] = Field('timestamp', description='排序欄位')

class FolderPath(BaseModel):
    """資料夾路徑參數"""
    folder_id: str = Field(..., description='資料夾 ID', example='folder123')

class FolderCreate(BaseModel):
    """建立資料夾請求"""
    name: str = Field(..., description='資料夾名稱')
    description: Optional[str] = Field(None, description='資料夾描述')
    parent_id: Optional[str] = Field(None, description='父資料夾 ID')

class FolderUpdate(BaseModel):
    """更新資料夾請求"""
    name: Optional[str] = Field(None, description='資料夾名稱')
    description: Optional[str] = Field(None, description='資料夾描述')
    parent_id: Optional[str] = Field(None, description='父資料夾 ID')

class FolderDownloadResponse(BaseModel):
    """資料夾下載回應"""
    description: str = Field("ZIP file containing the folder", description="回應描述")
    content: dict = Field(
        default={
            "application/zip": {
                "schema": {
                    "type": "string",
                    "format": "binary"
                }
            }
        },
        description="回應內容"
    )