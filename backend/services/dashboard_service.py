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
    def get_basic_stats(self):
        """獲取基本統計數據"""
        try:
            # 分別查詢各個表的總數
            total_users = db.session.query(User).count()
            total_stores = db.session.query(Store).count()
            total_ratings = db.session.query(Rating).count()
            total_favorites = db.session.query(Favorite).count()

            # 計算增長趨勢（與上月比較）
            last_month = datetime.now() - timedelta(days=30)
            
            new_users = db.session.query(User)\
                .filter(User.register_time >= last_month).count()
            new_stores = db.session.query(Store)\
                .filter(Store.created_at >= last_month).count()
            new_ratings = db.session.query(Rating)\
                .filter(Rating.time >= last_month).count()
            new_favorites = db.session.query(Favorite)\
                .filter(Favorite.created_at >= last_month).count()

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
                ]
            }
        except Exception as e:
            logger.error(f"獲取基本統計數據失敗: {str(e)}")
            raise

    def get_top_shops(self):
        """獲取熱門店家"""
        try:
            # 使用窗口函數來確保每個店家只出現一次
            rank_query = """
                WITH RankedStores AS (
                    SELECT 
                        s.id,
                        s.name,
                        s.address,
                        s.city,
                        s.city_CN,
                        COUNT(r.id) as rating_count,
                        ROUND(AVG(r.rating), 2) as avg_rating,
                        ROW_NUMBER() OVER (
                            PARTITION BY s.name 
                            ORDER BY COUNT(r.id) DESC, AVG(r.rating) DESC
                        ) as rn
                    FROM stores s
                    LEFT JOIN ratings r ON s.name = r.restaurant_name
                    GROUP BY s.id, s.name, s.address, s.city, s.city_CN
                )
                SELECT *
                FROM RankedStores
                WHERE rn = 1
                ORDER BY rating_count DESC, avg_rating DESC
                LIMIT 5
            """

            # 執行查詢
            top_shops = db.session.execute(text(rank_query)).fetchall()

            # 計算增長率（最近30天）
            last_month = datetime.now() - timedelta(days=30)
            
            result = []
            for shop in top_shops:
                # 計算該店家最近30天的評論數
                recent_reviews = db.session.query(func.count(Rating.id))\
                    .filter(
                        Rating.restaurant_name == shop.name,
                        Rating.time >= last_month
                    ).scalar()
                
                # 計算增長率
                total_reviews = shop.rating_count
                increase = round((recent_reviews / total_reviews * 100) if total_reviews > 0 else 0, 1)

                result.append({
                    "id": shop.id,
                    "name": shop.name,
                    "address": shop.address,
                    "city": shop.city,
                    "city_CN": shop.city_CN,
                    "rating": float(shop.avg_rating) if shop.avg_rating else 0,
                    "review_number": shop.rating_count,
                    "increase": increase
                })

            return {"topShops": result}
            
        except Exception as e:
            logger.error(f"獲取熱門店家失敗: {str(e)}")
            raise

    def get_latest_reviews(self):
        """獲取最新評論"""
        try:
            # 使用窗口函數來獲取每個用戶最新的評論
            latest_reviews_query = """
                WITH RankedReviews AS (
                    SELECT 
                        r.id,
                        r.user,
                        r.place_id,
                        r.restaurant_name,
                        r.rating,
                        r.text,
                        r.english_texts,
                        r.time,
                        ROW_NUMBER() OVER (
                            PARTITION BY r.user 
                            ORDER BY r.time DESC
                        ) as rn
                    FROM ratings r
                )
                SELECT *
                FROM RankedReviews
                WHERE rn = 1
                ORDER BY time DESC
                LIMIT 5
            """

            # 執行查詢
            latest_reviews = db.session.execute(text(latest_reviews_query)).fetchall()

            return {
                "latestReviews": [
                    {
                        "id": review.id,
                        "user": review.user,
                        "place_id": review.place_id,
                        "restaurant_name": review.restaurant_name,
                        "rating": float(review.rating),
                        "text": review.text,
                        "english_texts": review.english_texts,
                        "createdAt": review.time
                    } for review in latest_reviews
                ]
            }
        except Exception as e:
            logger.error(f"獲取最新評論失敗: {str(e)}")
            raise

    def get_system_logs(self):
        """獲取系統日誌"""
        try:
            system_logs = db.session.query(Log)\
              .order_by(desc(Log.created_at))\
              .limit(5).all()

            return {
                "systemLogs": [
                    {
                        "id": log.id,
                        "type": log.status.lower() if log.status else 'info',
                        "message": log.description,
                        "timestamp": log.created_at.strftime("%Y-%m-%d %H:%M")
                    } for log in system_logs
                ]
            }
        except Exception as e:
            logger.error(f"獲取系統日誌失敗: {str(e)}")
            raise

    def get_activity_data(self):
        """獲取活動數據"""
        try:
            return {
                "activityData": self._get_activity_data()
            }
        except Exception as e:
            logger.error(f"獲取活動數據失敗: {str(e)}")
            raise

    def get_stats(self):
        """獲取完整的儀表板統計數據"""
        try:
            return {
                **self.get_basic_stats(),
                **self.get_top_shops(),
                **self.get_latest_reviews(),
                **self.get_system_logs(),
                **self.get_activity_data()
            }
        except Exception as e:
            logger.error(f"獲取儀表板數據失敗: {str(e)}")
            raise

    def _get_activity_data(self):
        """獲取用戶活躍度數據"""
        try:
            # 使用 GMT+8 時間
            now = datetime.now() + timedelta(hours=8)
            hourly_start = now - timedelta(hours=48)
            daily_start = now - timedelta(days=30)

            # 使用原生 SQL 查詢來獲取小時數據
            hourly_sql = """
                SELECT 
                    DATE_FORMAT(
                        CASE 
                            WHEN activity_time IS NOT NULL THEN DATE_ADD(activity_time, INTERVAL 8 HOUR)
                            ELSE NOW()
                        END, 
                        '%Y-%m-%d %H:00'
                    ) as hour,
                    COUNT(DISTINCT user_id) as count
                FROM (
                    SELECT id as user_id, register_time as activity_time FROM users WHERE register_time >= :hourly_start
                    UNION ALL
                    SELECT user as user_id, time as activity_time FROM ratings WHERE time >= :hourly_start
                    UNION ALL
                    SELECT user_id, created_at as activity_time FROM favorites WHERE created_at >= :hourly_start
                ) as activities
                WHERE activity_time IS NOT NULL
                GROUP BY hour
                ORDER BY hour
            """

            # 使用原生 SQL 查詢來獲取日數據
            daily_sql = """
                SELECT 
                    DATE_FORMAT(
                        CASE 
                            WHEN activity_time IS NOT NULL THEN DATE_ADD(activity_time, INTERVAL 8 HOUR)
                            ELSE NOW()
                        END, 
                        '%Y-%m-%d'
                    ) as date,
                    COUNT(DISTINCT user_id) as count
                FROM (
                    SELECT id as user_id, register_time as activity_time FROM users WHERE register_time >= :daily_start
                    UNION ALL
                    SELECT user as user_id, time as activity_time FROM ratings WHERE time >= :daily_start
                    UNION ALL
                    SELECT user_id, created_at as activity_time FROM favorites WHERE created_at >= :daily_start
                ) as activities
                WHERE activity_time IS NOT NULL
                GROUP BY date
                ORDER BY date
            """

            # 執行查詢
            hourly_result = db.session.execute(
                text(hourly_sql),
                {"hourly_start": hourly_start}
            ).fetchall()

            daily_result = db.session.execute(
                text(daily_sql),
                {"daily_start": daily_start}
            ).fetchall()

            # 處理結果
            hourly_dates = []
            hourly_values = []
            for row in hourly_result:
                if row[0] is not None:  # 確保日期不為 None
                    hourly_dates.append(row[0])
                    hourly_values.append(row[1])

            daily_dates = []
            daily_values = []
            for row in daily_result:
                if row[0] is not None:  # 確保日期不為 None
                    daily_dates.append(row[0])
                    daily_values.append(row[1])

            return {
                "dates": daily_dates,
                "values": daily_values,
                "hourly": {
                    "dates": hourly_dates,
                    "values": hourly_values
                }
            }

        except Exception as e:
            logger.error(f"獲取活躍度數據失敗: {str(e)}")
            raise 