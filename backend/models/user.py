from datetime import datetime, timedelta
from models.database import db
import pytz
import jwt
from flask import current_app
import secrets
import bcrypt
import logging
import os

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.Index('ix_user_register_time', 'register_time'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)  # 社群登入可能沒有密碼
    avatar = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default='Enabled')
    register_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)  # Firebase 用戶 ID
    provider = db.Column(db.String(20), nullable=True)  # 登入提供者 (google, facebook, github)
    
    # 新增重設密碼相關欄位
    reset_password_token = db.Column(db.String(100), unique=True)
    reset_password_expires = db.Column(db.DateTime)
    
    # 新增密碼歷史記錄欄位
    password_history = db.Column(db.JSON, default=list)  # 儲存最近5次的密碼hash

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'status': self.status,
            'register_time': self.register_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.register_time else None,
            'update_time': self.update_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def generate_reset_token(self):
        """生成重設密碼 token"""
        # 生成 32 位元的隨機 token
        token = secrets.token_urlsafe(32)
        
        # 根據配置設定過期時間
        expire_type = current_app.config['RESET_TOKEN_EXPIRE_TYPE']
        expire_value = current_app.config['RESET_TOKEN_EXPIRE_VALUE']
        
        # 檢查配置值
        logger.info("配置檢查:")
        logger.info(f"RESET_TOKEN_EXPIRE_TYPE 環境變數值: {os.getenv('RESET_TOKEN_EXPIRE_TYPE')}")
        logger.info(f"RESET_TOKEN_EXPIRE_VALUE 環境變數值: {os.getenv('RESET_TOKEN_EXPIRE_VALUE')}")
        logger.info(f"current_app.config['RESET_TOKEN_EXPIRE_TYPE']: {expire_type}")
        logger.info(f"current_app.config['RESET_TOKEN_EXPIRE_VALUE']: {expire_value}")
        
        now = datetime.utcnow()
        logger.info(f"Token 建立時間(UTC): {now}")
        
        # 計算過期時間
        logger.info(f"過期時間類型: {expire_type}, 值: {expire_value}")
        # 確保類型轉換正確
        expire_value = int(expire_value)
        if expire_type == 'seconds':
            expire_time = timedelta(seconds=expire_value)
            logger.info(f"過期時間設定為 {expire_value} 秒")
        elif expire_type == 'minutes':
            expire_time = timedelta(minutes=expire_value)
            logger.info(f"過期時間設定為 {expire_value} 分鐘")
        else:  # 預設使用小時
            expire_time = timedelta(hours=expire_value)
            logger.info(f"過期時間設定為 {expire_value} 小時")
        
        # 計算過期時間點 = 現在時間 + 過期時間
        expires = now + expire_time
        logger.info(f"Token 過期時間(UTC): {expires}")
        
        # 轉換為台灣時間以便記錄
        tw_expires = expires.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        logger.info(f"Token 過期時間(台灣): {tw_expires}")
        
        self.reset_password_token = token
        self.reset_password_expires = expires  # 存入 UTC 時間
        db.session.commit()
        
        return token
    
    def verify_reset_token(self, token):
        """驗證重設密碼 token"""
        if (self.reset_password_token != token or 
            not self.reset_password_expires or 
            datetime.utcnow() > self.reset_password_expires):
            return False
        return True
        
    def check_password_history(self, new_password: str) -> bool:
        """檢查新密碼是否與歷史密碼重複
        
        Returns:
            bool: True 如果密碼可以使用，False 如果密碼重複
        """
        # 檢查當前密碼
        if bcrypt.checkpw(new_password.encode('utf-8'), self.password.encode('utf-8')):
            return False
            
        # 檢查密碼歷史
        if self.password_history:
            for old_password in self.password_history:
                if bcrypt.checkpw(new_password.encode('utf-8'), old_password.encode('utf-8')):
                    return False
        return True
        
    def update_password_history(self, old_password: str):
        """更新密碼歷史
        
        Args:
            old_password: 舊密碼的hash值
        """
        history = self.password_history or []
        history.append(old_password)
        # 只保留最近5次的密碼
        self.password_history = history[-5:] if len(history) > 5 else history 