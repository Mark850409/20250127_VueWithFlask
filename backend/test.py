import os
import zipfile
from services.folder_service import FolderService
from factory import create_app
import io

# 建立 Flask 應用程式
app = create_app()

def test_download_folder():
    # 使用應用程式上下文
    with app.app_context():
        folder_id = "79f64748-03ac-454b-aaa4-19491195b026"
        service = FolderService()
        response = service.download_folder(folder_id)
        
        if response:
            print(f"下載成功: {response}")
            # 將回應內容轉換為 BytesIO 物件
            zip_data = io.BytesIO(response.content)
            
            # 使用 BytesIO 讀取 ZIP 內容
            with zipfile.ZipFile(zip_data) as zipf:
                print("壓縮內容:", zipf.namelist())
        else:
            print("下載資料夾失敗")

if __name__ == "__main__":
    test_download_folder()