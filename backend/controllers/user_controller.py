from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from services.user_service import UserService
from datetime import datetime
import pytz
from schemas.user_schema import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

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

@user_bp.get('/', tags=[user_tag])
def get_users():
    """獲取所有用戶
    
    Returns:
        200 (UserResponseSchema): 用戶列表
        500: 服務器錯誤
    """
    service = UserService()
    users = service.get_all_users()
    return {'users': [user.to_dict() for user in users]}

@user_bp.post('/register', tags=[user_tag])
def register(body: UserRegisterSchema):
    """用戶註冊
    
    Args:
        body (UserRegisterSchema): 註冊數據
            
    Returns:
        201 (UserResponseSchema): 註冊成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = UserService()
        user = service.register(body.dict())
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
            
        # 確保使用正確的用戶ID
        user_id = str(user.id)
        print(f"登入用戶ID: {user_id}")  # 添加調試日誌
        
        access_token = create_access_token(
            identity=user_id,
            additional_claims={'type': 'access'}
        )
            
        return {
            'token': access_token,
            'user': user.to_dict()
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