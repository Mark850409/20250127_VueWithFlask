from typing import List, Optional
from models.menu import Menu, db
from dao.menu_dao import MenuDAO

class MenuService:
    def __init__(self):
        self.dao = MenuDAO()
    
    def get_all_menus(self) -> List[Menu]:
        """獲取所有選單"""
        return self.dao.get_all_menus()
    
    def get_menu(self, menu_id: int) -> Optional[Menu]:
        """獲取指定選單"""
        return self.dao.get_menu_by_id(menu_id)
    
    def create_menu(self, menu_data: dict) -> Menu:
        """創建選單"""
        # 檢查是否有任何選單存在
        existing_menus = self.get_all_menus()
        
        # 如果沒有任何選單，強制設置為頂層選單
        if not existing_menus:
            menu_data['parent_id'] = None
        # 如果有選單且指定了父選單，則檢查父選單是否存在
        elif menu_data.get('parent_id') is not None and menu_data.get('parent_id') != 0:
            parent = self.get_menu(menu_data['parent_id'])
            if not parent:
                raise ValueError('父選單不存在')
        
        # 如果 parent_id 為 0 或 None，設為 None（表示頂層選單）
        if menu_data.get('parent_id') == 0 or menu_data.get('parent_id') is None:
            menu_data['parent_id'] = None
            
        return self.dao.create_menu(menu_data)
    
    def update_menu(self, menu_id: int, menu_data: dict) -> Optional[Menu]:
        """更新選單"""
        return self.dao.update_menu(menu_id, menu_data)
    
    def delete_menu(self, menu_id: int) -> bool:
        """刪除選單"""
        return self.dao.delete_menu(menu_id)
    
    def get_menus_by_parent_id(self, parent_id: Optional[int] = None) -> List[Menu]:
        """獲取指定父級ID的所有選單"""
        return self.dao.get_menus_by_parent_id(parent_id)
    
    def get_menu_tree(self) -> List[dict]:
        """獲取選單樹結構"""
        def build_tree(parent_id=None):
            menus = self.dao.get_menus_by_parent_id(parent_id)
            tree = []
            for menu in menus:
                node = menu.to_dict()
                children = build_tree(menu.id)
                if children:
                    node['children'] = children
                tree.append(node)
            return tree
        
        return build_tree() 