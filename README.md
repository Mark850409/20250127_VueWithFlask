# Git 小助手

一個簡單易用的Git圖形化操作介面，使用Vue 3和Python Flask開發。

## 專案簡介

Git小助手是一個輕量級的Git圖形化工具，提供基本的Git操作功能，適合Git初學者使用。它具有直觀的用戶界面，可以幫助用戶更容易地理解和使用Git的基本功能。

### 主要功能

- 倉庫初始化
- 檔案暫存
- 提交更改
- 分支管理
- 遠程倉庫配置
- 推送代碼
- Git配置設置

### 技術棧

前端：
- Vue 3
- Tailwind CSS
- Vite
- Fetch API

後端：
- Python 3.8+
- Flask
- GitPython
- Flask-CORS

## 安裝步驟

### 前置需求

- Node.js 14+
- Python 3.8+
- Git

### 後端設置

1. 創建並啟動Python虛擬環境：
```bash
cd backend
python -m venv venv
```
2. 激活虛擬環境：
```bash
source venv/bin/activate
```
3. 安裝依賴：
```bash
pip install -r requirements.txt
```
4. 運行Flask應用：
```bash
python app.py
```

### 前端設置

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```
3. 運行Vite開發環境：
```bash
npm run dev
```

4. 訪問前端應用：
```bash
http://localhost:3000
```

## 使用說明

1. **初始化倉庫**
   - 輸入倉庫路徑
   - 點擊「初始化倉庫」按鈕

2. **配置Git信息**
   - 點擊右上角「配置Git」按鈕
   - 輸入用戶名和郵箱
   - 點擊保存

3. **添加和提交文件**
   - 點擊「添加文件」將更改加入暫存區
   - 點擊「提交更改」並輸入提交信息

4. **分支操作**
   - 點擊「分支操作」
   - 可以創建新分支或切換到現有分支

5. **遠程倉庫操作**
   - 點擊「配置遠程倉庫」
   - 輸入遠程倉庫URL
   - 使用「推送到遠程」將代碼推送到遠程倉庫


## 開發指南

### 項目結構
```
git-helper/
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── App.vue
│ │ └── main.js
│ ├── index.html
│ └── package.json
└── backend/
├── app.py
├── git_operations.py
└── requirements.txt
```


### 開發模式

1. 後端開發
   - 修改 `app.py` 添加新的路由
   - 在 `git_operations.py` 中實現新的Git操作

2. 前端開發
   - 在 `App.vue` 中添加新的UI元素
   - 實現對應的方法處理用戶操作

## 版本記錄

### v1.0.1 (2025-01-27)
- 增加git提交歷史
- 增加版本回退

### v1.0.0 (2025-01-27)
- 初始版本發布
- 實現基本的Git操作功能
- 添加遠程倉庫支持

## 注意事項

1. 使用前確保已安裝Git
2. 需要正確配置Git用戶信息
3. 推送到遠程倉庫時需要適當的權限
4. 使用HTTPS推送時需要配置個人訪問令牌（Personal Access Token）
5. 使用SSH推送時需要配置SSH密鑰

### 配置遠程倉庫認證

#### 使用HTTPS（推薦新手使用）：
1. 在GitHub設置中生成個人訪問令牌（Personal Access Token）
2. 使用令牌作為密碼進行認證
3. 可以使用Git憑證管理器保存認證信息

#### 使用SSH：
1. 生成SSH密鑰對：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. 將公鑰添加到GitHub賬戶
3. 確保使用SSH URL作為遠程倉庫地址

## 貢獻指南

1. Fork 本專案
2. 創建新的功能分支
3. 提交更改
4. 發起 Pull Request

## 授權協議

本專案採用 MIT 授權協議。

## 作者

markhsu

## 致謝

- Vue.js 團隊
- Flask 開發團隊
- GitPython 專案