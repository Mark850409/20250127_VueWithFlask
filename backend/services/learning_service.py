import os
from dao.learning_dao import LearningDAO
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image
import io

class LearningService:
    UPLOAD_FOLDER = 'uploads/learning'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_IMAGE_SIZE = (1200, 1200)
    
    def __init__(self):
        self.dao = LearningDAO()
        # 確保上傳目錄存在
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
    
    def get_all_sections(self):
        """獲取所有學習區塊，按排序順序返回"""
        sections = self.dao.get_all_sections()
        return [section.to_dict() for section in sections]
    
    def create_section(self, data):
        """創建主標題區塊"""
        # 如果沒有指定排序順序，則設置為當前最大值+1
        if 'sort_order' not in data or data['sort_order'] is None:
            max_order = self.dao.get_max_sort_order_section()
            data['sort_order'] = max_order + 1
            
        section = self.dao.create_section(data)
        return section.to_dict()
    
    def create_subsection(self, data):
        """創建次標題區塊"""
        # 檢查主區塊是否存在
        section = self.dao.get_section_by_id(data['section_id'])
        if not section:
            raise ValueError('主區塊不存在')
            
        # 如果沒有指定排序順序，則設置為當前最大值+1
        if 'sort_order' not in data or data['sort_order'] is None:
            max_order = self.dao.get_max_sort_order_subsection(data['section_id'])
            data['sort_order'] = max_order + 1
            
        subsection = self.dao.create_subsection(data)
        return subsection.to_dict()
    
    def update_section(self, section_id, data):
        """更新主標題區塊"""
        section = self.dao.get_section_by_id(section_id)
        if not section:
            raise ValueError('區塊不存在')
            
        section = self.dao.update_section(section, data)
        return section.to_dict()
    
    def update_subsection(self, subsection_id, data):
        """更新次標題區塊"""
        subsection = self.dao.get_subsection_by_id(subsection_id)
        if not subsection:
            raise ValueError('子區塊不存在')
            
        subsection = self.dao.update_subsection(subsection, data)
        return subsection.to_dict()
    
    def delete_section(self, section_id):
        """刪除主標題區塊"""
        section = self.dao.get_section_by_id(section_id)
        if not section:
            raise ValueError('區塊不存在')
            
        self.dao.delete_section(section)
    
    def delete_subsection(self, subsection_id):
        """刪除次標題區塊"""
        subsection = self.dao.get_subsection_by_id(subsection_id)
        if not subsection:
            raise ValueError('子區塊不存在')
            
        self.dao.delete_subsection(subsection)
    
    def upload_image(self, file):
        """上傳圖片
        
        Args:
            file (FileStorage): 圖片文件
            
        Returns:
            str: 圖片URL
            
        Raises:
            ValueError: 文件格式錯誤或大小超過限制
        """
        if not file:
            raise ValueError('未上傳文件')
            
        if not self._allowed_file(file.filename):
            raise ValueError('不支援的文件格式，僅支援 jpg、png、gif、webp 格式')
            
        # 檢查文件大小（5MB）
        file.seek(0, 2)  # 移到文件末尾
        size = file.tell()  # 獲取大小
        file.seek(0)  # 回到開頭
        
        if size > 5 * 1024 * 1024:  # 5MB
            raise ValueError('文件大小超過限制(5MB)')
        
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # 保存並處理圖片
        filepath = os.path.join(self.UPLOAD_FOLDER, filename)
        
        # 調整圖片大小並保存
        image = Image.open(file)
        image.thumbnail(self.MAX_IMAGE_SIZE)
        
        # 根據原始格式保存
        if image.format == 'PNG':
            image.save(filepath, format='PNG', optimize=True)
        elif image.format == 'GIF':
            image.save(filepath, format='GIF')
        else:
            image = image.convert('RGB')
            image.save(filepath, format='JPEG', quality=85, optimize=True)
        
        # 返回可訪問的URL
        return f"/uploads/learning/{filename}"
    
    def _allowed_file(self, filename):
        """檢查文件是否允許上傳"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS 