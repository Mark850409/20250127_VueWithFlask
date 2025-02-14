from typing import List, Optional
from models.folder import Folder, db

class FolderDAO:
    @staticmethod
    def get_all_folders() -> List[Folder]:
        """獲取所有資料夾"""
        return Folder.query.filter_by(status='active').all()
    
    @staticmethod
    def create_folder(data: dict) -> Folder:
        """建立資料夾"""
        folder = Folder(**data)
        db.session.add(folder)
        db.session.commit()
        return folder
    
    @staticmethod
    def get_by_folder_id(folder_id: str) -> Optional[Folder]:
        """根據 folder_id 獲取資料夾"""
        return Folder.query.filter_by(
            folder_id=folder_id,
            status='active'
        ).first()
    
    @staticmethod
    def update_folder(folder_id: str, data: dict) -> Optional[Folder]:
        """更新資料夾"""
        folder = Folder.query.filter_by(
            folder_id=folder_id,
            status='active'
        ).first()
        
        if folder:
            for key, value in data.items():
                setattr(folder, key, value)
            db.session.commit()
        
        return folder
    
    @staticmethod
    def delete_folder(folder_id: str) -> bool:
        """刪除資料夾（軟刪除）"""
        folder = Folder.query.filter_by(folder_id=folder_id).first()
        if folder:
            folder.status = 'deleted'
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_children(folder_id: str) -> List[Folder]:
        """獲取子資料夾"""
        return Folder.query.filter_by(
            parent_id=folder_id,
            status='active'
        ).all() 