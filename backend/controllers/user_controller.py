from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from services.user_service import UserService
from datetime import datetime, timedelta
import pytz
from schemas.user_schema import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from flask import request, send_from_directory, send_file, jsonify
import os
from pathlib import Path
from PIL import Image
import io
from flask_cors import cross_origin

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

# API 藍圖和標籤
user_bp = APIBlueprint('users', __name__, url_prefix='/api/users')
user_tag = Tag(name='users', description='用戶管理')

# 請求和響應模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str]
    status: str = 'Enabled'

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    avatar: Optional[str]
    status: Optional[str]

class UserResponse(UserBase):
    id: int
    register_time: datetime
    update_time: datetime

    @classmethod
    def from_orm(cls, obj):
        # 將時間轉換為台灣時區
        if obj.register_time:
            obj.register_time = obj.register_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        if obj.update_time:
            obj.update_time = obj.update_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        return super().from_orm(obj)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserList(BaseModel):
    users: List[UserResponse]

class ErrorResponse(BaseModel):
    message: str

# 添加請求參數模型
class UserPath(BaseModel):
    """用戶路徑參數"""
    user_id: int = Field(..., description='用戶ID')

class UserQuery(BaseModel):
    user_id: Optional[int] = None

# 獲取當前文件的目錄
CURRENT_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = 'uploads/avatars'
UPLOAD_PATH = CURRENT_DIR / UPLOAD_FOLDER

# 設定頭像的最大尺寸
MAX_SIZE = (200, 200)  # 寬度和高度的最大值

# 添加允許的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """檢查文件擴展名是否允許"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path):
    """調整圖片大小"""
    try:
        with Image.open(image_path) as img:
            # 保持原始比例
            img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            
            # 保存到內存
            img_io = io.BytesIO()
            
            # 根據原始格式保存
            if img.format == 'PNG':
                # PNG 保持 RGBA 模式
                img.save(img_io, format='PNG', optimize=True)
            elif img.format == 'GIF':
                # GIF 保持原始格式
                img.save(img_io, format='GIF')
            else:
                # 其他格式轉換為 RGB 並保存為 JPEG
                img = img.convert('RGB')
                img.save(img_io, format='JPEG', quality=85, optimize=True)
            
            img_io.seek(0)
            return img_io, img.format or 'JPEG'
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        return None, None

@user_bp.get('/avatar/<path:filename>', tags=[user_tag])
def get_avatar(path: UserAvatarParamsSchema):
    """獲取用戶頭像
    
    Args:
        path (UserAvatarParamsSchema): 頭像文件名
            
    Returns:
        200: 頭像文件
        404: 文件不存在
    """
    try:
        file_path = UPLOAD_PATH / path.filename
        if not file_path.exists():
            return {'message': '文件不存在'}, 404

        # 調整圖片大小
        img_io, img_format = resize_image(file_path)
        if img_io is None:
            return {'message': '圖片處理失敗'}, 500

        # 設置正確的 MIME 類型
        mime_types = {
            'JPEG': 'image/jpeg',
            'PNG': 'image/png',
            'GIF': 'image/gif'
        }
        mimetype = mime_types.get(img_format, 'image/jpeg')

        return send_file(
            img_io,
            mimetype=mimetype,
            as_attachment=False,
            download_name=path.filename
        )
    except Exception as e:
        print(f"Error accessing file: {path.filename}")
        print(f"Error details: {str(e)}")
        return {'message': f'文件不存在: {str(e)}'}, 404

@user_bp.get('/', tags=[user_tag])
@jwt_required()
def get_users():
    """獲取所有用戶
    
    Returns:
        200 (UserResponseSchema): 用戶列表
        500: 服務器錯誤
    """
    try:
        service = UserService()
        users = service.get_all_users()
        return {'users': [user.to_dict() for user in users]}
    except Exception as e:
        print(f"獲取用戶列表失敗: {str(e)}")
        return {'message': f'獲取用戶列表失敗: {str(e)}'}, 500

@user_bp.post('/register', tags=[user_tag])
def register():
    """用戶註冊
    
    Returns:
        201 (UserResponseSchema): 註冊成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        # 從表單數據中獲取值
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 驗證必填字段
        if not all([username, email, password]):
            return {'message': '請填寫所有必填欄位'}, 400

        data = {
            'username': username,
            'email': email,
            'password': password
        }
        
        # 處理頭像上傳
        avatar_file = request.files.get('avatar')
        if avatar_file and allowed_file(avatar_file.filename):
            # 確保上傳目錄存在
            os.makedirs(UPLOAD_PATH, exist_ok=True)
            # 生成安全的文件名（添加時間戳避免重名）
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{username}_{timestamp}_{avatar_file.filename}")
            filepath = UPLOAD_PATH / filename
            
            # 保存原始文件
            avatar_file.save(filepath)
            
            # 調整大小並保存
            with Image.open(filepath) as img:
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                # 根據原始格式保存
                if img.format == 'PNG':
                    img.save(filepath, format='PNG', optimize=True)
                elif img.format == 'GIF':
                    img.save(filepath, format='GIF')
                else:
                    img = img.convert('RGB')
                    img.save(filepath, format='JPEG', quality=85, optimize=True)
            
            data['avatar'] = f'{UPLOAD_FOLDER}/{filename}'
        else:
            data['avatar'] = f'{UPLOAD_FOLDER}/default.png'
        
        service = UserService()
        user = service.register(data)
        return user.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        return {'message': f'註冊失敗: {str(e)}'}, 500

@user_bp.post('/login', tags=[user_tag])
def login(body: UserLoginSchema):
    """用戶登入
    
    Args:
        body (UserLoginSchema): 登入數據
            
    Returns:
        200: 登入成功
            token (str): JWT token
            user (UserResponseSchema): 用戶信息
        400: 參數錯誤
        401: 登入失敗
    """
    try:
        service = UserService()
        user = service.login(body.dict())
        if not user:
            return {'message': '帳號或密碼錯誤'}, 401
            
        user_id = str(user.id)
        access_token = create_access_token(
            identity=user_id,
            additional_claims={'type': 'access'}
        )
            
        # 確保返回完整的用戶信息，包括頭像URL
        return {
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar,  # 確保這個字段存在
                'status': user.status
            }
        }
    except Exception as e:
        return {'message': f'登入失敗: {str(e)}'}, 500

@user_bp.get('/<int:user_id>', tags=[user_tag])
def get_user(path: UserPath):
    """獲取指定用戶
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 用戶ID
            
    Returns:
        200 (UserResponseSchema): 用戶信息
        404: 用戶不存在
        500: 服務器錯誤
    """
    try:
        service = UserService()
        user = service.get_user(path.user_id)
        if not user:
            return {'message': '用戶不存在'}, 404
        return user.to_dict()
    except Exception as e:
        return {'message': f'獲取用戶失敗: {str(e)}'}, 500

@user_bp.put('/<int:user_id>', tags=[user_tag])
def update_user(path: UserPath, body: UserUpdateSchema):
    """更新用戶
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 要更新的用戶ID
        body (UserUpdateSchema): 更新數據
            
    Example:
        PUT /api/users/1
        {
            "username": "mark_new",
            "email": "mark_new@example.com"
        }
        
    Returns:
        200 (UserResponseSchema): 更新成功
        400: 用戶名或郵箱已存在
        404: 用戶不存在
        500: 服務器錯誤
    """
    service = UserService()
    user_id = path.user_id
    
    # 檢查用戶是否存在
    existing_user = service.get_user(user_id)
    if not existing_user:
        return {'message': '用戶不存在'}, 404
    
    update_data = body.dict(exclude_unset=True)
    
    # 如果要更新用戶名，檢查是否已存在
    if 'username' in update_data:
        user = service.get_user_by_username(update_data['username'])
        if user and user.id != user_id:
            return {'message': '用戶名已存在'}, 400
    
    # 如果要更新郵箱，檢查是否已存在
    if 'email' in update_data:
        user = service.get_user_by_email(update_data['email'])
        if user and user.id != user_id:
            return {'message': '郵箱已存在'}, 400
    
    user = service.update_user(user_id, update_data)
    return user.to_dict()

@user_bp.delete('/<int:user_id>', tags=[user_tag])
def delete_user(path: UserPath):
    """刪除用戶
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 要刪除的用戶ID
            
    Example:
        DELETE /api/users/1
        
    Returns:
        204: 刪除成功
        404: 用戶不存在
        500: 刪除失敗
    """
    service = UserService()
    user_id = path.user_id
    
    # 檢查用戶是否存在
    existing_user = service.get_user(user_id)
    if not existing_user:
        return {'message': '用戶不存在'}, 404
    
    if service.delete_user(user_id):
        return '', 204
    return {'message': '刪除失敗'}, 500

@user_bp.post('/logout', tags=[user_tag])
@jwt_required()
def logout():
    """用戶登出
    
    Returns:
        200: 登出成功
            message (str): 成功信息
        401: 未登入
        500: 服務器錯誤
        
    Security:
        Bearer: []
        
    Example:
        POST /api/users/logout
        
    Response:
        {
            "message": "登出成功"
        }
    """
    try:
        # 獲取當前用戶信息
        current_user_id = get_jwt_identity()
        print(f"用戶 {current_user_id} 登出")
        
        return {'message': '登出成功'}, 200
    except Exception as e:
        print(f"登出錯誤: {str(e)}")
        return {'message': f'登出失敗: {str(e)}'}, 500

@user_bp.get('/verify', tags=[user_tag])
@jwt_required()
def verify_token():
    """驗證 token 是否有效
    
    Returns:
        200: token 有效
            message (str): 成功信息
            user_id (int): 用戶ID
        401: token 無效或過期
        
    Security:
        Bearer: []
        
    Example:
        GET /api/users/verify
        
    Response:
        {
            "message": "Token is valid",
            "user_id": 1
        }
    """
    try:
        current_user = get_jwt_identity()
        return jsonify({
            'message': 'Token is valid',
            'user_id': current_user
        }), 200
    except Exception as e:
        print(f"Token 驗證錯誤: {str(e)}")
        return {'message': f'Token 驗證失敗: {str(e)}'}, 401 

