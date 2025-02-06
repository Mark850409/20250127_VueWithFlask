from typing import List, Optional
from models.googlemaps_info import GoogleMapsInfo
from models.database import db
from sqlalchemy import text

class GoogleMapsInfoDAO:
    def get_all(self) -> List[GoogleMapsInfo]:
        """獲取所有記錄"""
        return GoogleMapsInfo.query.all()

    def get_by_id(self, id: int) -> Optional[GoogleMapsInfo]:
        """根據ID獲取記錄"""
        return GoogleMapsInfo.query.get(id)

    def get_by_place_id(self, place_id: str) -> Optional[GoogleMapsInfo]:
        """根據place_id獲取記錄"""
        return GoogleMapsInfo.query.filter_by(place_id=place_id).first()

    def create(self, data: dict) -> GoogleMapsInfo:
        """創建新記錄"""
        info = GoogleMapsInfo(**data)
        db.session.add(info)
        db.session.commit()
        return info

    def bulk_create(self, data_list: List[dict]) -> List[GoogleMapsInfo]:
        """批量創建記錄"""
        infos = [GoogleMapsInfo(**data) for data in data_list]
        db.session.bulk_save_objects(infos)
        db.session.commit()
        return infos

    def get_existing_place_ids(self) -> List[str]:
        """獲取所有已存在的place_id"""
        results = db.session.query(GoogleMapsInfo.place_id).all()
        return [result[0] for result in results if result[0]] 