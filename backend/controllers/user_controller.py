from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from services.user_service import UserService
from datetime import datetime, timedelta
import pytz
from schemas.user_schema import (
    UserRegisterSchema, UserLoginSchema, UserUpdateSchema, UserResponseSchema,
    UserPath, UserRegisterFileSchema, UserRegisterFormSchema, UserAvatarParamsSchema,
    UserAvatarSchema, FileUploadResponse, UserRegisterResponse,
    UserRegisterMultipartSchema, UploadFileForm, ForgotPasswordSchema,
    ResetPasswordSchema, VerifyResetTokenResponse, VerifyResetTokenParams,
    FirebaseLoginSchema
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from flask import request, send_from_directory, send_file, jsonify, current_app
import os
from pathlib import Path
from PIL import Image
import io
from flask_cors import cross_origin
import logging
from services.mail_service import MailService
from models.user import User, db

logger = logging.getLogger(__name__)

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

# API 藍圖和標籤
user_bp = APIBlueprint('users', __name__, url_prefix='/api/users')
user_tag = Tag(name='users', description='用戶管理')

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
        # 從表單數據中獲取值
        username = body.username
        email = body.email
        password = body.password
        status = body.status or 'Enabled'

        # 驗證必填字段
        if not all([username, email, password, status]):
            return {'message': '請填寫所有必填欄位'}, 400

        data = {
            'username': username,
            'email': email,
            'password': password,
            'status': status
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
            data['avatar'] = ''

        #print('data', data)
        
        service = UserService()
        user = service.register(data)
        
        # 生成 token
        user_id = str(user.id)
        access_token = create_access_token(
            identity=user_id,
            additional_claims={'type': 'access'}
        )
        
        # 返回用戶信息和 token
        user_data = user.to_dict()
        return {
            'token': access_token,
            'user': user_data
        }, 201
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
@jwt_required()
def update_user(path: UserPath, body: UserUpdateSchema):
    """更新用戶
    
    Args:
        path (UserPath): 路徑參數
        body (UserUpdateSchema): 更新數據
            
    Returns:
        200 (UserResponseSchema): 更新成功
        404: 用戶不存在
        500: 服務器錯誤
    """
    try:
        service = UserService()
        # 將請求數據轉換為字典，並過濾掉 None 值
        update_data = {k: v for k, v in body.dict().items() if v is not None}
        user = service.update_user(path.user_id, update_data)
        
        if not user:
            return {'message': '用戶不存在'}, 404
            
        return user.to_dict()
    except Exception as e:
        return {'message': f'更新用戶失敗: {str(e)}'}, 500

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
        logger.info(f"用戶 {current_user_id} 登出")
        
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

@user_bp.post(
    '/avatar',
    tags=[user_tag],
    responses={
        "200": FileUploadResponse,
        "400": {"description": "參數錯誤"},
        "401": {"description": "未登入"},
        "500": {"description": "服務器錯誤"}
    }
)
@jwt_required()
def update_avatar(form: UploadFileForm):
    """更新用戶頭像
    
    Returns:
        200: 
            message (str): 成功訊息
            avatar_url (str): 頭像URL
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return {'message': '未上傳文件'}, 400
            
        avatar_file = request.files['file']
        if not avatar_file.filename:
            return {'message': '未選擇文件'}, 400
            
        service = UserService()
        avatar_url = service.update_avatar(user_id, avatar_file)
        
        return {
            'message': '頭像上傳成功',
            'avatar_url': avatar_url
        }
        
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"更新頭像錯誤: {str(e)}", exc_info=True)
        return {'message': '更新頭像失敗'}, 500 

@user_bp.post(
    '/forgot-password',
    tags=[user_tag],
    responses={
        "200": {
            "description": "重設密碼郵件已發送",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"}
                        }
                    }
                }
            }
        },
        "404": {
            "description": "用戶不存在",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
)
def forgot_password(body: ForgotPasswordSchema):
    """處理忘記密碼請求
    
    Args:
        body (ForgotPasswordSchema): 包含用戶 email
            
    Returns:
        200: 重設密碼郵件已發送
        400: 參數錯誤
        404: 用戶不存在
        500: 服務器錯誤
    """
    try:
        service = UserService()
        service.request_password_reset(body.email)
        
        return jsonify({
            'success': True,
            'message': '重設密碼郵件已發送'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
        
    except Exception as e:
        logger.error(f"忘記密碼錯誤: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': '發送重設密碼郵件失敗'
        }), 500

@user_bp.post(
    '/reset-password',
    tags=[user_tag],
    responses={
        "200": {
            "description": "密碼重設成功",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"}
                        }
                    }
                }
            }
        },
        "400": {
            "description": "參數錯誤或密碼不符合規則",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"}
                        },
                        "example": {
                            "success": False,
                            "message": "新密碼不能與最近5次使用過的密碼相同"
                        }
                    }
                }
            }
        }
    }
)
def reset_password(body: ResetPasswordSchema):
    """重設密碼
    
    Args:
        body (ResetPasswordSchema): 包含重設密碼 token 和新密碼
            
    Returns:
        200: 密碼重設成功
        400: 參數錯誤或密碼不符合規則
        500: 服務器錯誤
    """
    try:
        service = UserService()
        service.reset_password(body.token, body.password)
        
        return jsonify({
            'success': True,
            'message': '密碼重設成功'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e) if '新密碼不能與最近' in str(e) else '無效的重設密碼連結或已過期'
        }), 400
        
    except Exception as e:
        logger.error(f"重設密碼錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': '重設密碼失敗'
        }), 500

@user_bp.get(
    '/verify-reset-token/<token>',
    tags=[user_tag],
    responses={
        "200": {
            "description": "Token 有效",
            "content": {
                "application/json": {
                    "schema": VerifyResetTokenResponse.schema()
                }
            }
        },
        "400": {
            "description": "Token 無效或已過期",
            "content": {
                "application/json": {
                    "schema": VerifyResetTokenResponse.schema()
                }
            }
        }
    }
)
def verify_reset_token(path: VerifyResetTokenParams):
    """驗證重設密碼 token
    
    Args:
        token (str): 重設密碼 token
        
    Returns:
        200: Token 有效
        400: Token 無效或已過期
    """
    try:
        service = UserService()
        if service.verify_reset_token(path.token):
            return jsonify({
                'success': True
            })
        else:
            return jsonify({
                'success': False,
                'message': '無效的重設密碼連結或已過期'
            }), 400
            
    except Exception as e:
        logger.error(f"驗證重設密碼 token 錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': '驗證 token 失敗'
        }), 500

@user_bp.post('/firebase', tags=[user_tag])
def firebase_login(body: FirebaseLoginSchema):
    """Firebase 社群登入
    
    Args:
        body (FirebaseLoginSchema): Firebase 登入數據
            
    Returns:
        200: 登入成功
            token (str): JWT token
            user (UserResponseSchema): 用戶信息
        400: 參數錯誤
        401: 登入失敗
    """
    try:
        service = UserService()
        user = service.firebase_login(body.token, body.provider)
        
        if not user:
            return {'message': '登入失敗'}, 401
            
        user_id = str(user.id)
        access_token = create_access_token(
            identity=user_id,
            additional_claims={'type': 'access'}
        )
            
        return {
            'token': access_token,
            'user': user.to_dict()
        }
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        return {'message': f'登入失敗: {str(e)}'}, 500

