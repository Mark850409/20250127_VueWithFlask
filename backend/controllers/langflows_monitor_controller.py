from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import MonitorQuery, DeleteMessagesRequest, DeleteMessagesResponse, ErrorResponse
from services.langflow_monitor_service import LangflowMonitorService
import logging

logger = logging.getLogger(__name__)
monitor_tag = Tag(name='Langflow_monitor', description='Langflow 監控相關操作')
monitor_bp = APIBlueprint('monitor', __name__, url_prefix='/api/v1/monitor')

service = LangflowMonitorService()

@monitor_bp.get('/messages', tags=[monitor_tag])
def get_monitor_messages(query: MonitorQuery):
    """獲取監控訊息"""
    try:
        messages = service.get_monitor_messages(
            flow_id=query.flow_id,
            session_id=query.session_id,
            sender=query.sender,
            sender_name=query.sender_name,
            order_by=query.order_by
        )
        return {'messages': messages}
    except Exception as e:
        logger.error(f"獲取監控訊息失敗: {str(e)}")
        return {'message': str(e)}, 400

@monitor_bp.delete(
    '/messages/session/<string:session_id>',
    tags=[monitor_tag],
    responses={
        "200": DeleteMessagesResponse,
        "404": ErrorResponse,
        "500": ErrorResponse
    }
)
def delete_messages(path: DeleteMessagesRequest):
    """刪除指定 session 的對話記錄
    
    Args:
        path (DeleteMessagesRequest): 路徑參數
            session_id (str): 對話 Session ID
            
    Returns:
        200: 刪除成功
            success (bool): 是否成功
            message (str): 結果訊息
        404: 對話不存在
            message (str): 錯誤訊息
        500: 服務器錯誤
            message (str): 錯誤訊息
    """
    try:
        logger.info(f"接收到刪除請求，session_id: {path.session_id}")
        result = service.delete_messages_by_session(path.session_id)
        logger.info(f"刪除對話記錄結果: {result}")
        
        if result['success']:
            return DeleteMessagesResponse(
                success=True,
                message=result['message']
            ).dict()
        else:
            return ErrorResponse(
                message=result['message']
            ).dict(), 404
            
    except Exception as e:
        logger.error(f"刪除對話記錄時發生錯誤: {str(e)}")
        return ErrorResponse(
            message=f"刪除對話記錄失敗: {str(e)}"
        ).dict(), 500 