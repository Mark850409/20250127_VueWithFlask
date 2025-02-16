from pydantic import BaseModel, Field
from typing import Optional, List
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
    folder_id: str = Field(..., description='資料夾 ID', example='79f64748-03ac-454b-aaa4-19491195b026')

class FolderCreate(BaseModel):
    """Langflow 建立資料夾請求參數"""
    name: str = Field(..., description='資料夾名稱', example='string')
    description: str = Field(..., description='資料夾描述', example='string')
    components_list: List[str] = Field(..., description='組件列表', example=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])
    flows_list: List[str] = Field(..., description='流程列表', example=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])

class FolderUpdate(BaseModel):
    """更新資料夾請求"""
    name: str = Field(..., description='資料夾名稱', example='string')
    description: str = Field(..., description='資料夾描述', example='string')
    parent_id: str = Field(..., description='父資料夾 ID', example='3fa85f64-5717-4562-b3fc-2c963f66afa6')
    components: List[str] = Field(..., description='組件列表', example=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])
    flows: List[str] = Field(..., description='流程列表', example=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])

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

class DeleteMessagesRequest(BaseModel):
    """刪除對話請求參數"""
    session_id: str = Field(..., description='對話 Session ID')

class DeleteMessagesResponse(BaseModel):
    """刪除對話響應"""
    success: bool = Field(..., description='是否成功')
    message: str = Field(..., description='結果訊息')

class ErrorResponse(BaseModel):
    """錯誤響應"""
    message: str = Field(..., description='錯誤訊息')