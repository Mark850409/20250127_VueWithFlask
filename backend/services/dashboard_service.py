from models.database import db
from models.user import User
from models.store import Store
from models.rating import Rating
from models.log import Log
from models.favorite import Favorite
from sqlalchemy import func, desc, distinct, case, text
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DashboardService:
    def get_stats(self):
        """獲取儀表板統計數據"""
        try:
            # 分別查詢各個表的總數
            total_users = db.session.query(User).count()
            total_stores = db.session.query(Store).count()
            total_ratings = db.session.query(Rating).count()
            total_favorites = db.session.query(Favorite).count()

            # 計算增長趨勢（與上月比較）
            last_month = datetime.now() - timedelta(days=30)
            
            # 分別查詢新增數據
            new_users = db.session.query(User)\
                .filter(User.register_time >= last_month).count()
            
            new_stores = db.session.query(Store)\
                .filter(Store.created_at >= last_month).count()
            
            new_ratings = db.session.query(Rating)\
                .filter(Rating.time >= last_month).count()
            
            new_favorites = db.session.query(Favorite)\
                .filter(Favorite.created_at >= last_month).count()

            # 獲取熱門店家
            top_shops = db.session.query(
                Store,
                func.count(Rating.id).label('rating_count'),
                func.avg(Rating.rating).label('avg_rating')
            ).join(Rating, Rating.restaurant_name == Store.name)\
             .group_by(Store.id)\
             .order_by(desc('rating_count'))\
             .limit(5).all()

            # 獲取最新評論
            latest_reviews = db.session.query(Rating)\
              .order_by(desc(Rating.time))\
              .limit(5).all()

            # 獲取系統日誌
            system_logs = db.session.query(Log)\
              .order_by(desc(Log.created_at))\
              .limit(5).all()

            # 獲取用戶活躍度數據
            activity_data = self._get_activity_data()
            #print(activity_data)

            return {
                "stats": [
                    {
                        "title": "店家管理",
                        "value": str(total_stores),
                        "trend": round((new_stores / total_stores * 100) if total_stores > 0 else 0.0, 1),
                        "unit": "家",
                        "icon": "fas fa-store",
                        "iconColor": "text-purple-500",
                        "path": "/admin/shops"
                    },
                    {
                        "title": "用戶管理",
                        "value": str(total_users),
                        "trend": round((new_users / total_users * 100) if total_users > 0 else 0, 1),
                        "unit": "人",
                        "icon": "fas fa-users",
                        "iconColor": "text-blue-500",
                        "path": "/admin/accounts"
                    },
                    {
                        "title": "評論管理",

                        "value": str(total_ratings),
                        "trend": round((new_ratings / total_ratings * 100) if total_ratings > 0 else 0, 1),
                        "unit": "則",
                        "icon": "fas fa-comments",
                        "iconColor": "text-yellow-500",
                        "path": "/admin/ratings"
                    },
                    {
                        "title": "最愛管理",
                        "value": str(total_favorites),
                        "trend": round((new_favorites / total_favorites * 100) if total_favorites > 0 else 0, 1),
                        "unit": "個",
                        "icon": "fas fa-heart",
                        "iconColor": "text-red-500",
                        "path": "/admin/favorites"
                    }
                ],
                "topShops": [
                    {
                        "id": shop.Store.id,
                        "name": shop.Store.name,
                        "address": shop.Store.address,
                        "city": shop.Store.city,
                        "city_CN": shop.Store.city_CN,
                        "rating": float(shop.avg_rating) if shop.avg_rating else 0,
                        "review_number": shop.rating_count,
                        "increase": 15  # 這裡可以計算實際增長率
                    } for shop in top_shops
                ],
                "latestReviews": [
                    {
                        "id": review.id,
                        "user": review.user,  # 使用者名稱
                        "place_id": review.place_id,  # 店家ID
                        "restaurant_name": review.restaurant_name,  # 店家名稱
                        "rating": float(review.rating),
                        "text": review.text,  # 評論內容
                        "english_texts": review.english_texts,  # 英文評論
                        "createdAt": review.time  # 直接使用字符串時間
                    } for review in latest_reviews
                ],
                "systemLogs": [
                    {
                        "id": log.id,
                        "type": log.status.lower() if log.status else 'info',
                        "message": log.description,
                        "timestamp": log.created_at.strftime("%Y-%m-%d %H:%M")
                    } for log in system_logs
                ],
                "activityData": activity_data
            }
        except Exception as e:
            logger.error(f"獲取儀表板數據失敗: {str(e)}")
            raise

    def _get_activity_data(self):
        """獲取用戶活躍度數據"""
        try:
            # 使用 GMT+8 時間
            now = datetime.now() + timedelta(hours=8)
            hourly_dates = []
            hourly_values = []
            daily_dates = []
            daily_values = []

            # 獲取最近48小時的數據（用於日視圖）
            for i in range(48):
                hour = now - timedelta(hours=i)
                hour_str = hour.strftime("%Y-%m-%d %H:00")
                
                hourly_users = db.session.query(func.count(func.distinct(
                    func.coalesce(User.id, Rating.user, Favorite.user_id)
                ))).select_from(User)\
                .outerjoin(Rating, func.date_format(func.date_add(Rating.time, text('INTERVAL 8 HOUR')), '%Y-%m-%d %H:00') == hour_str)\
                .outerjoin(Favorite, func.date_format(func.date_add(Favorite.created_at, text('INTERVAL 8 HOUR')), '%Y-%m-%d %H:00') == hour_str)\
                .filter(
                    db.or_(
                        func.date_format(func.date_add(User.register_time, text('INTERVAL 8 HOUR')), '%Y-%m-%d %H:00') == hour_str,
                        func.date_format(func.date_add(Rating.time, text('INTERVAL 8 HOUR')), '%Y-%m-%d %H:00') == hour_str,
                        func.date_format(func.date_add(Favorite.created_at, text('INTERVAL 8 HOUR')), '%Y-%m-%d %H:00') == hour_str
                    )
                ).scalar()
                
                hourly_dates.insert(0, hour.strftime("%Y-%m-%d %H:00"))
                hourly_values.insert(0, hourly_users or 0)

            # 獲取最近30天的數據（用於週視圖和月視圖）
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            for i in range(30):
                day = today - timedelta(days=i)  # 從今天開始算，包括今天
                day_str = day.strftime("%Y-%m-%d")
                
                daily_users = db.session.query(func.count(func.distinct(
                    func.coalesce(User.id, Rating.user, Favorite.user_id)
                ))).select_from(User)\
                .outerjoin(Rating, func.date_format(func.date_add(Rating.time, text('INTERVAL 8 HOUR')), '%Y-%m-%d') == day_str)\
                .outerjoin(Favorite, func.date_format(func.date_add(Favorite.created_at, text('INTERVAL 8 HOUR')), '%Y-%m-%d') == day_str)\
                .filter(
                    db.or_(
                        func.date_format(func.date_add(User.register_time, text('INTERVAL 8 HOUR')), '%Y-%m-%d') == day_str,
                        func.date_format(func.date_add(Rating.time, text('INTERVAL 8 HOUR')), '%Y-%m-%d') == day_str,
                        func.date_format(func.date_add(Favorite.created_at, text('INTERVAL 8 HOUR')), '%Y-%m-%d') == day_str
                    )
                ).scalar()
                
                daily_dates.insert(0, day.strftime("%Y-%m-%d"))
                daily_values.insert(0, daily_users or 0)

            return {
                "dates": daily_dates,  # 使用日期視圖作為基礎
                "values": daily_values,
                "hourly": {  # 添加小時視圖的數據
                    "dates": hourly_dates,
                    "values": hourly_values
                }
            }
        except Exception as e:
            logger.error(f"獲取活躍度數據失敗: {str(e)}")
            raise 