from models.restaurant import RestaurantTypeList
from models.database import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text
from typing import Dict, Any

class RestaurantDAO:
    @staticmethod
    def create_restaurant(data: Dict[str, Any]) -> RestaurantTypeList:
        """創建餐廳記錄"""
        restaurant = RestaurantTypeList(**data)
        db.session.add(restaurant)
        db.session.commit()
        return restaurant

    @staticmethod
    def find_by_name(name: str) -> RestaurantTypeList:
        """根據名稱查找餐廳"""
        return RestaurantTypeList.query.filter_by(name=name).first()

    @staticmethod
    def reset_table():
        """重置資料表"""
        db.session.execute(text("ALTER TABLE restaurant_type_list AUTO_INCREMENT = 1"))
        db.session.commit() 