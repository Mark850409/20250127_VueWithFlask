from flask_openapi3 import APIBlueprint, Tag
from services.menu_service import MenuService
from schemas.menu_schema import *
from pydantic import BaseModel, Field
from typing import List, Optional

menu_bp = APIBlueprint('menus', __name__, url_prefix='/api/menus')
menu_tag = Tag(name='menus', description='選單管理')

# 新增一個用於路徑參數的 Schema
class MenuPath(BaseModel):
    """選單路徑參數"""
    menu_id: int = Field(..., description='選單ID')

class MenuOrderItem(BaseModel):
    id: int
    sort_order: int
    section_order: int
    parent_id: Optional[int]
    category: Optional[str]

class MenuOrderUpdate(BaseModel):
    menus: List[MenuOrderItem]

@menu_bp.get('/', tags=[menu_tag])
def get_menus():
    """獲取所有選單
    
    Returns:
        200 (MenuResponseSchema): 選單列表
    """
    service = MenuService()
    menus = service.get_all_menus()
    return {'menus': [menu.to_dict() for menu in menus]}

@menu_bp.post('/', tags=[menu_tag])
def create_menu(body: MenuCreateSchema):
    """創建選單
    
    Args:
        body (MenuCreateSchema): 選單數據
        
    Returns:
        201 (MenuResponseSchema): 創建成功
        400: 父選單不存在
    """
    service = MenuService()
    
    # 檢查是否有任何選單存在
    existing_menus = service.get_all_menus()
    
    menu_data = body.dict()
    
    # 處理狀態值轉換
    if menu_data.get('status') == 'Enabled':
        menu_data['status'] = 'active'
    elif menu_data.get('status') == 'Disabled':
        menu_data['status'] = 'disabled'
    
    # 如果沒有任何選單，強制設置為頂層選單
    if not existing_menus:
        menu_data['parent_id'] = None
    # 如果有選單且指定了父選單，則檢查父選單是否存在
    elif menu_data.get('parent_id') is not None and menu_data.get('parent_id') != 0:
        parent_menu = service.get_menu(menu_data['parent_id'])
        if not parent_menu:
            return {'message': '父選單不存在'}, 400
    
    # 如果 parent_id 為 0 或 None，設為 None（表示頂層選單）
    if menu_data.get('parent_id') == 0 or menu_data.get('parent_id') is None:
        menu_data['parent_id'] = None
        
    menu = service.create_menu(menu_data)
    return menu.to_dict(), 201

@menu_bp.put('/<int:menu_id>', tags=[menu_tag])
def update_menu(path: MenuPath, body: MenuUpdateSchema):
    """更新選單
    
    Args:
        path (MenuPath): 路徑參數
            menu_id (int): 要更新的選單ID
        body (MenuUpdateSchema): 更新數據
            
    Example:
        PUT /api/menus/1
        {
            "name": "新選單名稱",
            "path": "/new-path"
        }
        
    Returns:
        200 (MenuResponseSchema): 更新成功
        400: 父選單不存在/不能設為自己的子選單
        404: 選單不存在
    """
    service = MenuService()
    menu_id = path.menu_id
    
    # 檢查選單是否存在
    existing_menu = service.get_menu(menu_id)
    if not existing_menu:
        return {'message': '選單不存在'}, 404
    
    menu_data = body.dict(exclude_unset=True)
    
    # 如果要更新 parent_id
    if 'parent_id' in menu_data:
        # 如果 parent_id 為 0 或 None，設為 None（表示頂層選單）
        if menu_data['parent_id'] == 0 or menu_data['parent_id'] is None:
            menu_data['parent_id'] = None
        else:
            # 檢查新的父選單是否存在
            parent_menu = service.get_menu(menu_data['parent_id'])
            if not parent_menu:
                return {'message': '父選單不存在'}, 400
            # 檢查是否將選單設為自己的子選單
            if menu_data['parent_id'] == menu_id:
                return {'message': '不能將選單設為自己的子選單'}, 400
    
    menu = service.update_menu(menu_id, menu_data)
    return menu.to_dict()

@menu_bp.delete('/<int:menu_id>', tags=[menu_tag])
def delete_menu(path: MenuPath):
    """刪除選單
    
    Args:
        path (MenuPath): 路徑參數
            menu_id (int): 要刪除的選單ID
            
    Example:
        DELETE /api/menus/1
        
    Returns:
        204: 刪除成功
        400: 請先刪除所有子選單
        404: 選單不存在
        500: 刪除失敗
    """
    service = MenuService()
    menu_id = path.menu_id
    
    # 檢查選單是否存在
    existing_menu = service.get_menu(menu_id)
    if not existing_menu:
        return {'message': '選單不存在'}, 404
    
    # 檢查是否有子選單
    child_menus = service.get_menus_by_parent_id(menu_id)
    if child_menus:
        return {'message': '請先刪除所有子選單'}, 400
    
    if service.delete_menu(menu_id):
        return '', 204
    return {'message': '刪除失敗'}, 500

@menu_bp.put('/order', tags=[menu_tag])
def update_menu_order(body: MenuOrderUpdate):
    """更新選單排序
    
    Args:
        body (MenuOrderUpdate): 選單排序數據
        
    Returns:
        200: 更新成功
        500: 更新失敗
    """
    service = MenuService()
    try:
        # 將 Pydantic 模型轉換為字典列表
        menu_list = [menu.dict() for menu in body.menus]
        print(f"Received menu list for update: {menu_list}")
        service.update_menu_order(menu_list)
        return {'message': '更新成功'}
    except Exception as e:
        return {'message': str(e)}, 500

@menu_bp.get('/sections', tags=[menu_tag])
def get_menu_sections():
    """獲取主功能區塊列表
    
    Returns:
        200: 主功能區塊列表
    """
    service = MenuService()
    sections = service.get_menu_sections()
    return {'sections': sections} 