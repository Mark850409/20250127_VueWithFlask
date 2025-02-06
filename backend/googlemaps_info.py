import pandas as pd
from utils.sqlfunctions import execute_query
from models.database import db
import os
from dao.googlemaps_dao import GoogleMapsDAO
from sqlalchemy import text
from config.config import Config
from models.googlemaps_info import GoogleMapsInfo


# 你的Google Places API金鑰
gmaps_dao = GoogleMapsDAO(Config.GOOGLE_MAPS_API_KEY)


# 建立空的DataFrame
df = pd.DataFrame(columns=['餐廳名稱', '使用者', '評論', '評分', '時間'])

# ----------------------------------------------------------------------------------------
# 資料表建立函數
# ----------------------------------------------------------------------------------------
# 創建資料表，如果不存在的話
def create_table_if_not_exists():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS restaurant.googlemaps_info
    (
        id              BIGINT AUTO_INCREMENT PRIMARY KEY,
        place_id        VARCHAR(255) UNIQUE,
        place_names     TEXT NULL,
        latitude        DOUBLE NULL,
        longitude       DOUBLE NULL,
        address         TEXT NULL,
        city            TEXT NULL,
        city_CN         TEXT NULL,
        redirection_url TEXT NULL,
        navigation_url  TEXT NULL
    );
    '''
    db.session.execute(text(create_table_query))
    db.session.commit()

def get_place_review(place_name):
    mydata = []
    count = 0
    for data in place_name:
        count = count + 1
        print(f"已經執行了:{count}筆")
        id = data[0]
        my_place_names = data[1]
        latitude = data[2]
        longitude = data[3]
        address = data[4]
        city = data[5]
        city_CN = data[6]
        redirection_url = data[7]

        # 取得ID
        place_id = gmaps_dao.find_place(my_place_names)

        # 範例起點和終點地址
        start_address = '東吳大學城中校區'
        navigation_url = gmaps_dao.get_navigation_url(start_address, my_place_names)
        mydata.append(
            {'id': id, 'place_id': place_id, 'place_names': my_place_names, 'latitude': latitude,
             'longitude': longitude, 'address': address, 'city': city, 'city_CN': city_CN,
             'redirection_url': redirection_url,
             'navigation_url': navigation_url})
        df = pd.DataFrame(mydata)
        print(data)
    try:
        create_table_if_not_exists()

        # 讀取現有place_id
        existing_place_ids = db.session.query(GoogleMapsInfo.place_id).all()
        existing_place_ids = [pid[0] for pid in existing_place_ids]

        # 找出需要插入的新資料
        new_data_df = df[~df['place_id'].isin(existing_place_ids)]

        # 將結果寫入新的 CSV
        new_data_df.to_csv('csv/googlemaps_info.csv', encoding='utf-8-sig', mode='a+',
                  header=True)

        # 將新資料寫入資料庫
        for _, row in new_data_df.iterrows():
            info = GoogleMapsInfo(
                place_id=row['place_id'],
                place_names=row['place_names'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                address=row['address'],
                city=row['city'],
                city_CN=row['city_CN'],
                redirection_url=row['redirection_url'],
                navigation_url=row['navigation_url']
            )
            db.session.add(info)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()

if __name__ == "__main__":
    # 獲取應用實例
    from flask import current_app
    app = current_app._get_current_object()  # 獲取實際的應用實例
    
    # 使用應用上下文查詢餐廳
    with app.app_context():
        # 移除CSV避免重複建立
        if os.path.exists('csv/googlemaps_info.csv'):
            os.remove('csv/googlemaps_info.csv')

        # 使用 SQL 語法查詢所有用戶
        sql_query = "SELECT id,name,latitude,longitude,address,city,city_CN,redirection_url FROM stores;"
        get_restaurants_list = execute_query(db.session, sql_query)

        my_restaurants_data = []

        for row in get_restaurants_list:
            my_restaurants_data.append(row)

        get_place_review(my_restaurants_data)
