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
        # 處理狀態值轉換
        status_map = {
            'Enabled': 'active',
            'Disabled': 'disabled'
        }
        if menu_data.get('status') in status_map:
            menu_data['status'] = status_map[menu_data['status']]
        
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
        # 處理狀態值轉換
        if menu_data.get('status') == 'Enabled':
            menu_data['status'] = 'active'
        elif menu_data.get('status') == 'Disabled':
            menu_data['status'] = 'disabled'
        
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
    
    def get_menu_sections(self) -> List[dict]:
        """獲取主功能區塊列表"""
        # 獲取每個類別的選單，按照 section_order 排序
        sections = db.session.query(
            Menu.category,
            db.func.coalesce(Menu.section_order, 0).label('section_order')  # 使用 coalesce 處理 null 值
        ).filter(
            Menu.parent_id.is_(None)  # 只獲取頂層選單
        ).group_by(
            Menu.category,
            db.func.coalesce(Menu.section_order, 0)
        ).order_by(
            db.func.coalesce(Menu.section_order, 0).asc()  # 使用 coalesce 處理排序
        ).all()
        
        print("Database query result:", sections)  # 添加日誌
        result = []
        seen_categories = set()
        for section in sections:
            # 確保每個類別只出現一次，並保留最小的 section_order
            if section.category and section.category not in seen_categories:
                result.append({
                    'category': section.category,
                    'section_order': section.section_order or 0  # 確保返回 0 而不是 None
                })
                seen_categories.add(section.category)
        
        print("Processed result:", result)  # 添加日誌
        return result
    
    def update_menu_order(self, menus: List[dict]) -> None:
        """更新選單排序"""
        try:
            print("Received menus data for update:", menus)
            with db.session.begin():
                for menu_data in menus:
                    menu = self.get_menu(menu_data['id'])
                    print(f"Processing menu update - ID: {menu_data['id']}")
                    print(f"Menu data: {menu_data}")
                    if menu:
                        print(f"Current menu state - ID: {menu.id}, Category: {menu.category}")
                        print(f"Current section_order: {menu.section_order}, New section_order: {menu_data.get('section_order')}")
                        # 如果是更新主功能區塊排序
                        if menu_data.get('section_order') is not None:
                            new_section_order = int(menu_data['section_order'])
                            print(f"Updating section_order for category {menu_data['category']} to {new_section_order}")
                            # 找出同類別的所有選單並更新
                            same_category_menus = db.session.query(Menu).filter(
                                Menu.category == menu_data['category']
                            ).all()
                            print(f"Found {len(same_category_menus)} menus in category {menu_data['category']}")
                            for same_cat_menu in same_category_menus:
                                same_cat_menu.section_order = new_section_order
                                db.session.add(same_cat_menu)
                                print(f"Updated menu - ID: {same_cat_menu.id}, Category: {same_cat_menu.category}, New section_order: {new_section_order}")
                        
                        # 如果是更新一般選單排序
                        if menu_data.get('sort_order') is not None:
                            print(f"Updating sort_order for menu {menu.id} to {menu_data['sort_order']}")
                            menu.sort_order = int(menu_data.get('sort_order', menu.sort_order))
                        
                        if menu_data.get('parent_id') is not None:
                            print("更新父選單ID")
                            menu.parent_id = menu_data['parent_id']
                        if menu_data.get('category') is not None:
                            print("更新選單類別")
                            menu.category = menu_data['category']
                        
                        db.session.add(menu)
            
            db.session.commit()
            print("Menu order update completed - Verifying changes...")
            # 驗證更新
            for menu_data in menus:
                updated_menu = self.get_menu(menu_data['id'])
                print(f"Verified menu - ID: {updated_menu.id}, Category: {updated_menu.category}")
                print(f"New section_order: {updated_menu.section_order}, New sort_order: {updated_menu.sort_order}")
        except Exception as e:
            db.session.rollback()
            print(f"Error in update_menu_order: {str(e)}")
            raise ValueError(f'更新排序失敗: {str(e)}') 