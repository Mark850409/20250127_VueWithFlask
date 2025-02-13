from flask_openapi3 import APIBlueprint, Tag
from services.bot_service import BotService
from schemas.bot_schema import *
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger(__name__)

bot_bp = APIBlueprint('bots', __name__, url_prefix='/api/bots')
bot_tag = Tag(name='bots', description='機器人問答管理')

@bot_bp.get('/', tags=[bot_tag])
def get_bots(query: BotQuerySchema):
    """獲取所有問答
    
    Returns:
        200: 問答列表
        500: 服務器錯誤
    """
    try:
        service = BotService()
        bots = service.get_all_bots(
            is_active=query.is_active
        )
        return {'bots': [bot.to_dict() for bot in bots]}
    except Exception as e:
        logger.error(f"獲取問答列表失敗: {str(e)}")
        return {'message': f'獲取問答列表失敗: {str(e)}'}, 500

@bot_bp.post('/', tags=[bot_tag])
@jwt_required()
def create_bot(body: BotCreateSchema):
    """創建問答
    
    Args:
        body: 問答數據
    
    Returns:
        201: 創建成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = BotService()
        bot = service.create_bot(body.dict())
        return bot.to_dict(), 201
    except Exception as e:
        logger.error(f"創建問答失敗: {str(e)}")
        return {'message': f'創建問答失敗: {str(e)}'}, 500

@bot_bp.put('/<int:bot_id>', tags=[bot_tag])
@jwt_required()
def update_bot(path: BotPath, body: BotUpdateSchema):
    """更新問答
    
    Args:
        path: 路徑參數
        body: 更新數據
    
    Returns:
        200: 更新成功
        404: 問答不存在
        500: 服務器錯誤
    """
    try:
        service = BotService()
        bot = service.update_bot(path.bot_id, body.dict(exclude_unset=True))
        if not bot:
            return {'message': '問答不存在'}, 404
        return bot.to_dict()
    except Exception as e:
        logger.error(f"更新問答失敗: {str(e)}")
        return {'message': f'更新問答失敗: {str(e)}'}, 500

@bot_bp.delete('/<int:bot_id>', tags=[bot_tag])
@jwt_required()
def delete_bot(path: BotPath):
    """刪除問答
    
    Args:
        path: 路徑參數
    
    Returns:
        204: 刪除成功
        404: 問答不存在
        500: 服務器錯誤
    """
    try:
        service = BotService()
        if service.delete_bot(path.bot_id):
            return '', 204
        return {'message': '問答不存在'}, 404
    except Exception as e:
        logger.error(f"刪除問答失敗: {str(e)}")
        return {'message': f'刪除問答失敗: {str(e)}'}, 500 