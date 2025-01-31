from typing import List, Optional
from models.menu import Menu, db

class MenuDAO:
    @staticmethod
    def get_all_menus() -> List[Menu]:
        """獲取所有選單"""
        return Menu.query.order_by(Menu.sort_order.asc()).all()
    
    @staticmethod
    def get_menu_by_id(menu_id: int) -> Optional[Menu]:
        """獲取指定選單"""
        return Menu.query.get(menu_id)
    
    @staticmethod
    def create_menu(menu_data: dict) -> Menu:
        """創建選單"""
        menu = Menu(**menu_data)
        db.session.add(menu)
        db.session.commit()
        return menu
    
    @staticmethod
    def update_menu(menu_id: int, menu_data: dict) -> Optional[Menu]:
        """更新選單"""
        menu = Menu.query.get(menu_id)
        if menu:
            for key, value in menu_data.items():
                setattr(menu, key, value)
            db.session.commit()
        return menu
    
    @staticmethod
    def delete_menu(menu_id: int) -> bool:
        """刪除選單"""
        menu = Menu.query.get(menu_id)
        if menu:
            db.session.delete(menu)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_menus_by_parent_id(parent_id: Optional[int] = None) -> List[Menu]:
        """獲取指定父級ID的所有選單"""
        return Menu.query.filter_by(parent_id=parent_id).order_by(Menu.sort_order.asc()).all() 