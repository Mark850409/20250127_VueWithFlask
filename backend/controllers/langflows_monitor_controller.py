from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import MonitorQuery
from services.langflow_service import LangflowService
import logging

logger = logging.getLogger(__name__)
monitor_tag = Tag(name='Langflow_monitor', description='Langflow 監控相關操作')
monitor_bp = APIBlueprint('monitor', __name__, url_prefix='/api/v1/monitor')

service = LangflowService()

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