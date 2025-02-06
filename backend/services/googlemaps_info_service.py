from typing import List, Dict
from dao.googlemaps_info_dao import GoogleMapsInfoDAO
from dao.googlemaps_dao import GoogleMapsDAO
import pandas as pd
import os
from config.config import Config
from models.database import db

class GoogleMapsInfoService:
    def __init__(self):
        self.dao = GoogleMapsInfoDAO()
        self.gmaps_dao = GoogleMapsDAO(Config.GOOGLE_MAPS_API_KEY)
        
        # 確保CSV目錄存在
        if not os.path.exists('csv'):
            os.makedirs('csv')
        
        # 初始化CSV文件
        self.csv_path = 'csv/googlemaps_info.csv'
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        
        # 寫入CSV標頭
        pd.DataFrame(columns=[
            'place_id', 'place_names', 'latitude', 'longitude',
            'address', 'city', 'city_CN', 'redirection_url', 'navigation_url'
        ]).to_csv(self.csv_path, encoding='utf-8-sig', index=False)

    def process_store_data(self, store_data: List[tuple]) -> Dict:
        """處理店家資料"""
        try:
            if not store_data:
                return {
                    'success': False,
                    'message': '沒有店家資料需要處理',
                    'error': '輸入的資料為空'
                }

            total_processed = 0
            new_records = 0
            batch_size = 10  # 每10筆資料處理一次
            current_batch = []
            error_records = []
            
            # 獲取已存在的place_ids
            existing_place_ids = set(self.dao.get_existing_place_ids())
            # 記錄當前批次中的place_ids
            current_batch_place_ids = set()
            
            for data in store_data:
                total_processed += 1
                print(f"處理第 {total_processed} 筆資料")
                
                try:
                    # 解構資料並檢查
                    if len(data) != 8:
                        raise ValueError(f"資料欄位數量不正確: {len(data)}")
                    
                    id, name, lat, lon, addr, city, city_cn, redirect_url = data
                    
                    # 檢查必要欄位
                    if not name or not isinstance(name, str):
                        raise ValueError(f"店家名稱無效: {name}")
                    
                    # 檢查座標
                    if lat is not None and not isinstance(lat, (int, float)):
                        lat = float(lat) if lat else None
                    if lon is not None and not isinstance(lon, (int, float)):
                        lon = float(lon) if lon else None
                    
                    # 獲取 Google Place ID
                    place_id = self.gmaps_dao.find_place(name)
                    if not place_id:
                        raise ValueError(f"找不到對應的地點: {name}")
                    
                    # 檢查place_id是否已存在於資料庫或當前批次中
                    if place_id in existing_place_ids or place_id in current_batch_place_ids:
                        continue
                    
                    # 獲取導航URL
                    start_address = '東吳大學城中校區'
                    navigation_url = self.gmaps_dao.get_navigation_url(start_address, name)
                    if not navigation_url:
                        navigation_url = "No navigation found"
                    
                    # 準備資料
                    store_info = {
                        'place_id': place_id,
                        'place_names': name,
                        'latitude': lat,
                        'longitude': lon,
                        'address': addr or '',
                        'city': city or '',
                        'city_CN': city_cn or '',
                        'redirection_url': redirect_url or '',
                        'navigation_url': navigation_url
                    }
                    
                    # 加入批次處理
                    current_batch.append(store_info)
                    current_batch_place_ids.add(place_id)  # 記錄此place_id
                    new_records += 1
                    
                    # 當達到批次大小時，進行處理
                    if len(current_batch) >= batch_size:
                        self._process_batch(current_batch)
                        # 更新已存在的place_ids集合
                        existing_place_ids.update(current_batch_place_ids)
                        # 清空當前批次
                        current_batch = []
                        current_batch_place_ids = set()
                
                except Exception as e:
                    error_msg = f"處理第 {total_processed} 筆資料時發生錯誤: {str(e)}"
                    print(error_msg)
                    error_records.append({
                        'index': total_processed,
                        'data': data,
                        'error': str(e)
                    })
                    continue
            
            # 處理剩餘的資料
            if current_batch:
                try:
                    self._process_batch(current_batch)
                    existing_place_ids.update(current_batch_place_ids)
                except Exception as e:
                    print(f"處理最後一批資料時發生錯誤: {str(e)}")
                    error_records.extend([{
                        'index': total_processed - len(current_batch) + i + 1,
                        'data': item,
                        'error': str(e)
                    } for i, item in enumerate(current_batch)])
            
            # 準備回傳結果
            result = {
                'success': True,
                'message': f'成功處理 {total_processed} 筆資料，新增 {new_records} 筆記錄',
                'total_processed': total_processed,
                'new_records': new_records
            }
            
            # 如果有錯誤記錄，加入到結果中
            if error_records:
                result['success'] = False
                result['error_records'] = error_records
                result['message'] = f'處理完成，但有 {len(error_records)} 筆資料發生錯誤'
            
            return result
            
        except Exception as e:
            db.session.rollback()  # 發生錯誤時回滾事務
            return {
                'success': False,
                'message': f'處理資料時發生錯誤: {str(e)}',
                'error': str(e)
            }

    def _process_batch(self, batch: List[Dict]):
        """處理一批資料"""
        if not batch:
            return
            
        try:
            # 寫入資料庫
            self.dao.bulk_create(batch)
            
            # 寫入CSV
            df = pd.DataFrame(batch)
            df.to_csv(
                self.csv_path,
                mode='a',
                header=False,
                index=False,
                encoding='utf-8-sig'
            )
            
        except Exception as e:
            db.session.rollback()  # 發生錯誤時回滾事務
            print(f"批次處理失敗: {str(e)}")
            raise e 