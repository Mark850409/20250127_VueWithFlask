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
- 提交歷史查看
- 版本回退
- 遠程同步

### 技術棧

前端：
- Vue 3
- Tailwind CSS
- Vite
- Fetch API
- SweetAlert2

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

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行Flask應用：
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

3. 運行開發服務器：
```bash
npm run dev
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
   - 點擊「配置遠程倉庫」配置遠程倉庫
   - 使用「推送到遠程」推送代碼
   - 使用「拉取遠程更新」同步遠程更改

6. **歷史管理**
   - 點擊「查看提交歷史」查看所有提交
   - 可以回退到指定版本

## 版本記錄

## 更新日誌

### v1.1.4 (2025-01-30)

#### 功能更新
- 提交歷史功能增強
  - 添加搜尋功能，支援提交哈希、作者、日期搜尋
  - 添加表格排序功能，支援所有欄位排序
  - 添加分頁功能，可自定義每頁顯示筆數
  - 優化版本回退功能，添加確認提示視窗

#### 介面優化
- 提交歷史顯示改進
  - 優化表格布局和樣式
  - 添加排序指示圖標
  - 美化分頁控制器
  - 改進每頁筆數選擇器樣式

#### 使用者體驗
- 添加操作提示和確認機制
  - 版本回退前顯示警告提示
  - 添加操作成功反饋
  - 優化錯誤提示訊息
- 改進資料顯示
  - 添加資料載入狀態
  - 優化空資料提示
  - 顯示資料總數和當前範圍

#### 技術改進
- 程式碼優化
  - 重構狀態解析邏輯
  - 優化資料過濾和排序機制
  - 改進分頁計算方法
  - 統一錯誤處理機制

### v1.1.3 (2025-01-30)

#### 功能更新
- 整合 Git 版本控制功能
  - 添加倉庫狀態即時監控
  - 支援基本的 Git 操作（提交、分支、推送等）
  - 美化提交歷史顯示界面
  - 優化檔案狀態展示

#### 改進
- 倉庫狀態顯示
  - 分類顯示未追蹤、已修改、已刪除和已暫存的文件
  - 使用不同顏色和圖標區分文件狀態
  - 支援多列顯示提升可讀性
  - 添加文件路徑截斷處理

- 提交歷史
  - 優化提交記錄的展示方式
  - 添加提交詳情查看功能
  - 支援版本回退操作
  - 美化提交信息格式

#### 技術改進
- 前後端整合
  - 統一錯誤處理機制
  - 添加請求超時保護
  - 優化 CORS 配置
  - 改進 API 路由結構

#### 問題修復
- 修復提交歷史顯示換行問題
- 修復遠程倉庫配置驗證問題
- 改善操作反饋提示
- 修正文件路徑顯示格式

### v1.1.2 (2025-01-29)
#### 介面優化
- 優化 Git 小助手介面
  - 改進提交歷史顯示
    - 調整表格欄位寬度比例
    - 優化提交信息的換行處理
    - 將操作按鈕改為圖標式設計
  - 美化整體視覺效果
    - 統一表格樣式
    - 添加懸停效果
    - 改善文字排版

#### 功能改進
- 改進提交歷史功能
  - 優化提交信息格式化顯示
  - 自動處理 feat:、fix: 等前綴的換行
  - 提升提交歷史的可讀性
- 改進遠程倉庫操作
  - 添加遠程倉庫後自動更新提交歷史
  - 添加操作成功/失敗的視覺反饋

#### 問題修復
- 修復提交歷史顯示換行問題
- 修復表格寬度不合理的問題
- 改善操作按鈕的可用性

### v1.1.1 (2025-01-29)

#### 新增功能
- 新增 Git 操作小助手功能
  - 在左下角添加固定的圓形按鈕，方便快速訪問 Git 操作介面
  - 實現 Git 操作的模態框顯示
  - 支援基本的 Git 操作功能（提交、分支、推送等）

#### 介面優化
- 優化登入/註冊頁面
  - 調整頁面間距和元件大小
  - 改善與導航欄的視覺層級關係
- 統一 Banner 組件的高度和樣式
  - 確保首頁、平台特色、學習中心、定價方案頁面的一致性
  - 修正 Banner 與導航欄的重疊問題

#### 技術改進
- 重構頁面布局結構
- 優化組件間的間距和層級關係
- 改善響應式設計

#### 問題修復
- 修復導航欄遮擋內容的問題
- 修正登入頁面的間距問題
- 解決 Banner 組件高度不一致的問題

### v1.1.0 (2025-01-28)
#### 新增功能
- 統一返回首頁按鈕樣式
  - 改為圓形按鈕設計
  - 添加懸浮動畫效果
  - 統一由 App.vue 管理

- 優化飲料店管理功能
  - 新增店家城市欄位
  - 新增店家星級評分顯示
  - 新增店家瀏覽次數統計
  - 優化店家圖片上傳與預覽
  - 完善表單驗證機制

#### 介面優化
- 店家列表顯示改進
  - 圖片尺寸調整為 16x16
  - 添加圖片陰影效果
  - 星級使用星星圖標直觀顯示
  - 瀏覽次數添加眼睛圖標

#### 資料結構更新
- 店家資料模型擴充
  - 添加 city 欄位
  - 添加 rating 評分欄位
  - 添加 views 瀏覽次數欄位
  - 優化狀態顯示格式

### v1.0.10 (2025-01-27)
### 導航欄優化
- 更新系統名稱為「基於文字探勘與情感分析的點餐推薦系統」
- 使用 DiceBear API 生成臨時 Logo
- 將導航選單置中顯示
- 移除關於我們下拉選單，改為直接展示主要功能頁面
- 優化 Git 小助手按鈕樣式，改用漸層色彩設計

### 頁面按鈕優化
- 在平台特色、學習中心和定價方案區塊底部添加導向按鈕
- 統一按鈕樣式和交互效果
- 優化按鈕位置，提升用戶體驗

### Footer 區塊改版
- 更新品牌介紹文案
- 功能特色區塊改為主要頁面快速連結
- 添加頁面連結的 hover 效果
- 更新版權聲明文字
- 優化整體排版和間距

### 其他改進
- 統一使用 router-link 進行頁面導航
- 優化響應式布局
- 改善整體視覺一致性
- 提升用戶交互體驗

### v1.0.9 (2025-01-27)
- 新增點餐推薦系統前台
  - 一頁式響應設計
  - 美食推薦功能
  - 社群媒體連結
- 優化界面設計
  - 添加 Logo 設計
  - 改進導航欄樣式
  - 優化頁腳布局
- 系統整合
  - 實現 Git 小助手與點餐系統的切換功能
  - 保持兩個系統的獨立性
  - 優化用戶體驗
- 技術改進
  - 添加 Vite 路徑別名配置
  - 改進組件結構
  - 優化資源加載

### v1.0.8 (2025-01-27)
- 美化界面顯示
  - 優化輸出區域樣式

### v1.0.7 (2025-01-27)
- 移除刪除提交功能以確保倉庫安全性
- 簡化操作界面
- 美化界面顯示
  - 優化輸出區域樣式
  - 添加狀態信息顏色提示
  - 改進滾動條設計
- 改進用戶體驗
  - Git狀態輸出格式化
  - 不同類型文件狀態使用不同顏色標示
  - 添加視覺反饋效果

### v1.0.6 (2025-01-27)
- 改進提交歷史界面
  - 固定表頭
  - 優化滾動條樣式
  - 調整欄位寬度比例
  - 美化提交信息顯示格式
  - 添加表格行懸停效果
- 改進提交信息顯示
  - 標題和內容分開顯示
  - 保持換行格式
  - 優化字體大小和間距

### v1.0.5 (2025-01-27)
- 移除退出按鈕
- 改進界面布局

### v1.0.4 (2025-01-27)
- 增加拉取遠程更新功能
- 改進推送功能，自動處理版本不同步問題

### v1.0.3 (2025-01-27)
- 增加刪除指定版本歷史功能
- 添加危險操作的確認機制

### v1.0.2 (2025-01-27)
- 增加版本回退時會同步清空未被Git追蹤的新文件、空目錄

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

## 授權協議

本專案採用 MIT 授權協議。

## 作者

markhsu

## 致謝

- Vue.js 團隊
- Flask 開發團隊
- GitPython 專案
- SweetAlert2 團隊
