# 飲料店點餐推薦系統 API

這是一個基於 Flask 的飲料店點餐推薦系統後端 API，提供完整的用戶管理、店家管理、評分系統、收藏功能等服務。

## 功能特點

- 🔐 完整的用戶認證系統（註冊、登入、JWT）
- 🏪 店家管理（CRUD、圖片上傳）
- ⭐ 評分與評論系統
- ❤️ 收藏功能
- 📊 數據分析與推薦
- 🔍 搜尋功能
- 📝 日誌記錄
- 👮 管理員後台
- 🌐 跨域支援
- 📚 Swagger API 文檔

## 技術指標

- Python 3.11
- Flask + flask-openapi3
- MySQL 8.0
- SQLAlchemy
- JWT 認證
- OpenAPI/Swagger
- Docker

## 快速開始

1. 複製專案：
```bash
git clone https://github.com/your-username/restaurant-api.git
cd restaurant-api
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 配置環境變數：
   - 複製 `.env.example` 到 `.env.development`（開發環境）
   - 複製 `.env.example` 到 `.env.production`（生產環境）
   - 根據需求修改配置

4. 初始化數據庫：
```bash
mysql -u root -p < scripts/init.sql
```

5. 運行服務：
```bash
python backend/app.py
```

6. 訪問 API 文檔：
   - 開發環境：http://localhost:5000/openapi/swagger
   - 生產環境：https://your-domain.com/openapi/swagger

## 專案結構

```
backend/
├── app.py              # 應用入口
├── config/            # 配置文件
├── controllers/       # 控制器層
├── services/         # 服務層
├── dao/              # 數據訪問層
├── models/           # 數據模型
├── schemas/          # 請求/響應模式
└── utils/            # 工具函數
```

## API 文檔

詳細的 API 文檔可以在運行服務後通過 Swagger UI 查看：
- 開發環境：http://localhost:5000/openapi/swagger
- 生產環境：https://your-domain.com/openapi/swagger

## 環境變數配置

| 變數名 | 說明 | 預設值 |
|--------|------|--------|
| DB_HOST | 數據庫主機 | localhost |
| DB_PORT | 數據庫端口 | 3306 |
| DB_USER | 數據庫用戶名 | root |
| DB_NAME | 數據庫名稱 | restaurant |
| JWT_SECRET_KEY | JWT 密鑰 | your-secret-key |
| CORS_ORIGINS | 允許的跨域來源 | http://localhost:3000 |

## 貢獻指南

1. Fork 本專案
2. 創建新分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

## 聯繫方式

- 作者：Mark
- Email：mark@example.com
- GitHub：[your-github-profile](https://github.com/your-username)