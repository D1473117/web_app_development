# 路由與頁面設計文件（ROUTES）

本文件根據產品需求文件（PRD）、資料庫設計文件（DB_DESIGN）及架構文件產出，詳細規劃所有 Flask 路由及對應視圖。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 列表 | GET | `/` | `recipes/index.html` | 顯示最新/熱門且公開的食譜 |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收並驗證註冊資料，寫入資料庫 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳密並登入 session |
| 處理登出 | POST | `/auth/logout` | — | 清除登入 session |
| 建立食譜頁 | GET | `/recipes/create` | `recipes/create.html` | 顯示新增食譜表單 |
| 儲存新食譜 | POST | `/recipes/create` | — | 儲存食譜、圖片、食材對應關係 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `recipes/detail.html` | 顯示特定食譜內容與留言 |
| 編輯食譜頁 | GET | `/recipes/<int:id>/edit` | `recipes/edit.html` | 顯示該筆食譜編輯表單 |
| 更新食譜 | POST | `/recipes/<int:id>/update` | — | 接收修改後的資料 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | — | 刪除食譜 |
| 關鍵字搜尋 | GET | `/search` | `search/results.html` | 基於標題/描述模糊搜尋 |
| 食材搜尋 | GET | `/search/ingredients` | `search/results.html` | 基於食材清單進行倒排與匹配度排序 |
| 切換收藏 | POST | `/favorites/toggle/<int:recipe_id>`| — | (JSON API) 將食譜加入/移除收藏 |
| 我的收藏 | GET | `/user/favorites` | `user/favorites.html`| 顯示使用者收藏的所有食譜 |
| 個人主頁 | GET | `/user/profile` | `user/profile.html`| 顯示「我的食譜」與「統計資訊」 |
| 新增留言 | POST | `/recipes/<int:id>/comments` | — | 送出針對該食譜的留言與評分 |
| 管理員總覽 | GET | `/admin/` | `admin/dashboard.html` | 顯示平台總覽（食譜數/用戶數） |
| 食譜管理 | GET | `/admin/recipes` | `admin/recipes.html` | 管理員檢視所有食譜 |
| 停用/刪除用戶 | POST | `/admin/users/<int:user_id>/delete`| — | 管理使用者狀態 |
| 刪除留言 | POST | `/admin/comments/<int:id>/delete` | — | 管理員刪除違規留言 |

---

## 2. 每個路由的詳細說明

### 首頁 (`/`)
- **輸入**: 無參數 (可支援 ?page= 分頁)
- **邏輯**: 呼叫 `Recipe.get_all(public_only=True)` 並排序
- **輸出**: 渲染 `recipes/index.html`

### 註冊/登入 (`/auth/register`, `/auth/login`)
- **輸入**: 表單的 `email` 及 `password`
- **邏輯**: 使用 `User.create()` 或 `check_password_hash`，成功則調用 `login_user()`
- **輸出**: 渲染模板，或 POST 成功時 `redirect(url_for('recipes.index'))`
- **錯誤處理**: 如果帳號重複或密碼錯誤，透過 `flash()` 回傳到原頁面。

### 新增/編輯食譜 (`/recipes/create`, `/recipes/<id>/edit`)
- **輸入**: 表單欄位有 `title`, `steps`, `prep_time` 及自定義的食材標籤、上傳圖片
- **邏輯**: `flask_login.login_required`。驗證後呼叫 `Recipe.create()`，並處理 `static/uploads/` 圖片存檔與食材寫入。
- **輸出**: 成功後 `redirect(url_for('recipes.detail', id=recipe.id))`
- **錯誤處理**: 驗證非作者或未登入則 403 / redirect 到登入，表單驗證失敗則渲染原來頁面重新填寫。

### 搜尋 (`/search`, `/search/ingredients`)
- **輸入**: `request.args.get('q')`
- **邏輯**: 前者使用 `LIKE` 條件，後者解析 `q` 並反查 `RecipeIngredient` 計算匹配數量。
- **輸出**: `search/results.html` 並傳入結果陣列與原先的 query 變數。

### 收藏 (`/favorites/toggle/<id>`)
- **輸入**: 無，依賴 URL 參數及目前的 `current_user`
- **邏輯**: `Favorite.query` 檢查是否已有紀錄，若有則刪除，若無則建立。
- **輸出**: 回傳 JSON `{ "status": "success", "action": "added|removed" }` 供前端 JS 使用。

### 使用者頁面 (`/user/profile`, `/user/favorites`)
- **邏輯**: 查詢 `current_user.recipes` 及 `current_user.favorites` 以呈現內容。
- **輸出**: 渲染 `user/profile.html` 與 `user/favorites.html`。

### 管理員路由 (`/admin/*`)
- **邏輯**: 所有路由須加上自定義的 `@admin_required` (檢查 `current_user.is_admin`)，可列表所有 user 和 models 並執行刪除。

---

## 3. Jinja2 模板清單

全站模板皆會繼承 **`base.html`**，其中包含頂部 Navbar 與底部 Footer。

- `templates/base.html`：公用版型，帶有 CSS/JS 引入及主推的 Navbar。
- `templates/auth/`
  - `login.html`：登入頁。
  - `register.html`：註冊頁。
- `templates/recipes/`
  - `index.html`：首頁。
  - `detail.html`：食譜詳情頁（包含步驟、圖片與下方留言區塊）。
  - `create.html` / `edit.html`：填寫與發布表格。
- `templates/search/`
  - `results.html`：搜尋結果清單。
- `templates/user/`
  - `profile.html`：個人主頁（可看自己所有食譜與統計）。
  - `favorites.html`：收藏清單。
- `templates/admin/`
  - `dashboard.html` / `users.html` / `recipes.html`：後台管理。
