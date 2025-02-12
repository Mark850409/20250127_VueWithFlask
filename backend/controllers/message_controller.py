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

class ReplyPath(MessagePath):
    """回覆路徑參數"""
    reply_id: int = Field(..., description='回覆ID')

class ReplyCreateSchema(BaseModel):
    """回覆創建參數"""
    content: str = Field(..., description='回覆內容')
    user_name: str = Field(..., description='回覆者名稱')
    user_id: int = Field(0, description='回覆者ID')
    avatar: str = Field('shop.png', description='回覆者頭像')

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
        return {'messages': messages}
    except Exception as e:
        print(f"獲取留言列表錯誤: {str(e)}")
        return {'message': '獲取留言列表失敗'}, 500

@message_bp.post('/', tags=[message_tag])
@jwt_required()
def create_message(body: MessageCreateSchema):
    """創建評論
    
    Args:
        body (MessageCreateSchema): 評論數據
            content (str): 評論內容
            store_id (int): 店家ID
            rating (float): 評分
            
    Returns:
        201 (MessageResponseSchema): 創建成功
        400: 參數錯誤
        401: 未登入
        404: 店家不存在
        500: 服務器錯誤
    """
    try:
        service = MessageService()
        user_id = int(get_jwt_identity())
        message = service.create_message(user_id, body.dict())
        return message.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"創建評論錯誤: {str(e)}")
        return {'message': '創建評論失敗'}, 500

@message_bp.put('/<int:message_id>', tags=[message_tag])
@jwt_required()
def update_message(path: MessagePath, body: MessageUpdateSchema):
    """更新留言
    
    Args:
        path (MessagePath): 路徑參數
            message_id (int): 留言ID
        body (MessageUpdateSchema): 更新數據
            content (str, optional): 留言內容
            rating (float, optional): 評分
            status (str, optional): 留言狀態 (pending/approved/rejected)
            
    Returns:
        200 (MessageResponseSchema): 更新成功
        400: 
            - 參數錯誤
            - 只能修改自己的留言
            - 無效的狀態值
            - 評分必須在0-5之間
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
        
        # 驗證狀態值
        if body.status and body.status not in ['pending', 'approved', 'rejected']:
            return {'message': '無效的狀態值'}, 400
        
        # 驗證評分範圍
        if body.rating is not None and not (0 <= body.rating <= 5):
            return {'message': '評分必須在0-5之間'}, 400
        
        message = service.update_message(user_id, path.message_id, body.dict(exclude_unset=True))
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

@message_bp.post('/<int:message_id>/replies', tags=[message_tag])
@jwt_required()
def add_reply(path: MessagePath, body: ReplyCreateSchema):
    """添加回覆
    
    Args:
        path (MessagePath): 路徑參數
            message_id (int): 評論ID
        body (ReplyCreateSchema): 回覆數據
            content (str): 回覆內容
            user_name (str): 回覆者名稱
            user_id (int): 回覆者ID，預設為0(店家)
            avatar (str): 回覆者頭像，預設為shop.png
            
    Returns:
        200 (MessageResponseSchema): 添加成功
        400: 參數錯誤
        401: 未登入
        404: 評論不存在
        500: 服務器錯誤
    """
    try:
        service = MessageService()
        message = service.add_reply(path.message_id, body.dict())
        if not message:
            return {'message': '評論不存在'}, 404
        return message.to_dict()
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"添加回覆錯誤: {str(e)}")
        return {'message': '添加回覆失敗'}, 500

@message_bp.delete('/<int:message_id>/replies/<int:reply_id>', tags=[message_tag])
@jwt_required()
def delete_reply(path: ReplyPath):
    """刪除回覆
    
    Args:
        path (ReplyPath): 路徑參數
            message_id (int): 評論ID
            reply_id (int): 回覆ID
            
    Returns:
        200 (MessageResponseSchema): 刪除成功
        401: 未登入
        404: 評論或回覆不存在
        500: 服務器錯誤
    """
    try:
        service = MessageService()
        message = service.delete_reply(path.message_id, path.reply_id)
        if not message:
            return {'message': '評論或回覆不存在'}, 404
        return message.to_dict()
    except Exception as e:
        print(f"刪除回覆錯誤: {str(e)}")
        return {'message': '刪除回覆失敗'}, 500 