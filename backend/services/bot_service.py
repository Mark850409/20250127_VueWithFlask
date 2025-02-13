from models.bot import Bot, db
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class BotService:
    def create_bot(self, data: dict) -> Bot:
        """創建新的快速問答或預設訊息"""
        try:
            # 如果是預設訊息，檢查是否已存在其他預設訊息
            if data.get('is_default'):
                existing_default = Bot.query.filter_by(is_default=True).first()
                if existing_default:
                    raise ValueError('已存在預設訊息，請先停用現有預設訊息')
            
            bot = Bot(**data)
            db.session.add(bot)
            db.session.commit()
            return bot
        except Exception as e:
            db.session.rollback()
            logger.error(f"創建失敗: {str(e)}")
            raise

    def get_bot(self, bot_id: int) -> Optional[Bot]:
        """獲取指定問答或預設訊息"""
        return Bot.query.get(bot_id)

    def get_all_bots(self, is_active: bool = None, is_default: bool = None) -> List[Bot]:
        """獲取所有問答或預設訊息"""
        query = Bot.query
        
        if is_active is not None:
            query = query.filter(Bot.is_active == is_active)
        if is_default is not None:
            # 如果要查詢快速問答，則排除預設訊息
            if not is_default:
                query = query.filter(Bot.is_default == False)
            # 如果要查詢預設訊息，則只查詢預設訊息
            else:
                query = query.filter(Bot.is_default == True)
        
        return query.order_by(Bot.sort_order.asc()).all()

    def get_default_message(self) -> Optional[Bot]:
        """獲取當前啟用的預設訊息"""
        return Bot.query.filter_by(is_default=True, is_active=True).first()

    def update_bot(self, bot_id: int, data: dict) -> Optional[Bot]:
        """更新問答或預設訊息"""
        try:
            bot = self.get_bot(bot_id)
            if bot:
                # 如果要設為預設訊息，先檢查是否有其他預設訊息
                if data.get('is_default'):
                    existing_default = Bot.query.filter(
                        Bot.id != bot_id,
                        Bot.is_default == True
                    ).first()
                    if existing_default:
                        raise ValueError('已存在預設訊息，請先停用現有預設訊息')
                
                for key, value in data.items():
                    setattr(bot, key, value)
                db.session.commit()
            return bot
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新失敗: {str(e)}")
            raise

    def delete_bot(self, bot_id: int) -> bool:
        """刪除問答或預設訊息"""
        try:
            bot = self.get_bot(bot_id)
            if bot:
                db.session.delete(bot)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            logger.error(f"刪除失敗: {str(e)}")
            raise 