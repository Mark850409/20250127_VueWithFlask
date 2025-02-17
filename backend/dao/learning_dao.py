from models.learning import Section, Subsection
from models.database import db
from sqlalchemy import desc

class LearningDAO:
    @staticmethod
    def get_all_sections():
        """獲取所有學習區塊"""
        return Section.query.order_by(Section.sort_order).all()
    
    @staticmethod
    def get_section_by_id(section_id):
        """根據ID獲取學習區塊"""
        return Section.query.get(section_id)
    
    @staticmethod
    def get_subsection_by_id(subsection_id):
        """根據ID獲取子區塊"""
        return Subsection.query.get(subsection_id)
    
    @staticmethod
    def create_section(section_data):
        """創建學習區塊"""
        section = Section(**section_data)
        db.session.add(section)
        db.session.commit()
        return section
    
    @staticmethod
    def create_subsection(subsection_data):
        """創建子區塊"""
        subsection = Subsection(**subsection_data)
        db.session.add(subsection)
        db.session.commit()
        return subsection
    
    @staticmethod
    def update_section(section, data):
        """更新學習區塊"""
        for key, value in data.items():
            if value is not None:
                setattr(section, key, value)
        db.session.commit()
        return section
    
    @staticmethod
    def update_subsection(subsection, data):
        """更新子區塊"""
        for key, value in data.items():
            if value is not None:
                setattr(subsection, key, value)
        db.session.commit()
        return subsection
    
    @staticmethod
    def delete_section(section):
        """刪除學習區塊"""
        db.session.delete(section)
        db.session.commit()
    
    @staticmethod
    def delete_subsection(subsection):
        """刪除子區塊"""
        db.session.delete(subsection)
        db.session.commit()
    
    @staticmethod
    def get_max_sort_order_section():
        """獲取最大排序值的區塊"""
        return db.session.query(db.func.max(Section.sort_order)).scalar() or 0
    
    @staticmethod
    def get_max_sort_order_subsection(section_id):
        """獲取指定區塊下最大排序值的子區塊"""
        return db.session.query(db.func.max(Subsection.sort_order))\
            .filter(Subsection.section_id == section_id).scalar() or 0 