from flask_openapi3 import APIBlueprint, Tag
from services.message_service import MessageService
from schemas.message_schema import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel, Field

message_bp = APIBlueprint('messages', __name__, url_prefix='/api/messages')
message_tag = Tag(name='messages', description='留言板管理')

class MessagePath(BaseModel):
    """留言路徑參數"""
    message_id: int = Field(..., description='留言ID')

@message_bp.get('/', tags=[message_tag])
def get_messages():
    """獲取所有留言
    
    Returns:
        200: 
            messages (List[MessageResponseSchema]): 留言列表
        500: 服務器錯誤
    """
    try:
        service = MessageService()
        messages = service.get_all_messages()
        return {'messages': [message.to_dict() for message in messages]}
    except Exception as e:
        print(f"獲取留言列表錯誤: {str(e)}")
        return {'message': '獲取留言列表失敗'}, 500

@message_bp.post('/', tags=[message_tag])
@jwt_required()
def create_message(body: MessageCreateSchema):
    """創建留言
    
    Args:
        body (MessageCreateSchema): 留言數據
            content (str): 留言內容
            
    Returns:
        201 (MessageResponseSchema): 創建成功
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
        
    Security:
        Bearer: []
        
    Example:
        POST /api/messages/
        {
            "content": "這是一條測試留言"
        }
    """
    try:
        service = MessageService()
        user_id = int(get_jwt_identity())
        message = service.create_message(user_id, body.dict())
        return message.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"創建留言錯誤: {str(e)}")
        return {'message': '創建留言失敗'}, 500

@message_bp.put('/<int:message_id>', tags=[message_tag])
@jwt_required()
def update_message(path: MessagePath, body: MessageUpdateSchema):
    """更新留言
    
    Args:
        path (MessagePath): 路徑參數
            message_id (int): 留言ID
        body (MessageUpdateSchema): 更新數據
            content (str): 留言內容
            
    Returns:
        200 (MessageResponseSchema): 更新成功
        400: 
            - 參數錯誤
            - 只能修改自己的留言
        401: 未登入
        404: 留言不存在
        500: 服務器錯誤
        
    Security:
        Bearer: []
        
    Example:
        PUT /api/messages/1
        {
            "content": "這是更新後的留言內容"
        }
    """
    try:
        service = MessageService()
        user_id = int(get_jwt_identity())
        message = service.update_message(user_id, path.message_id, body.dict())
        if not message:
            return {'message': '留言不存在'}, 404
        return message.to_dict()
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"更新留言錯誤: {str(e)}")
        return {'message': '更新留言失敗'}, 500

@message_bp.delete('/<int:message_id>', tags=[message_tag])
@jwt_required()
def delete_message(path: MessagePath):
    """刪除留言
    
    Args:
        path (MessagePath): 路徑參數
            message_id (int): 留言ID
            
    Returns:
        204: 刪除成功
        400: 只能刪除自己的留言
        401: 未登入
        404: 留言不存在
        500: 刪除失敗
        
    Security:
        Bearer: []
        
    Example:
        DELETE /api/messages/1
    """
    try:
        service = MessageService()
        user_id = int(get_jwt_identity())
        if service.delete_message(user_id, path.message_id):
            return '', 204
        return {'message': '留言不存在'}, 404
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"刪除留言錯誤: {str(e)}")
        return {'message': '刪除留言失敗'}, 500 