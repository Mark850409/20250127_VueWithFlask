from datetime import datetime
import pytz

def convert_to_taiwan_time(timestamp: int) -> str:
    """將 Unix timestamp 轉換為台灣時間"""
    utc_time = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
    taiwan_timezone = pytz.timezone('Asia/Taipei')
    taiwan_time = utc_time.astimezone(taiwan_timezone)
    return taiwan_time.strftime('%Y-%m-%d %H:%M:%S') 