# 流程圖文件（FLOWCHART）

**專案名稱：** 食譜收藏夾  
**版本：** v1.0  
**建立日期：** 2026-04-09  
**依據文件：** docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁\n公開食譜列表]

    Home --> Browse[瀏覽食譜]
    Home --> SearchKW[關鍵字搜尋]
    Home --> SearchIng[食材搜尋]
    Home --> AuthCheck{是否已登入？}

    %% 搜尋流程
    SearchKW --> KWInput[輸入關鍵字\n選擇篩選條件]
    KWInput --> SearchResult[搜尋結果頁]
    SearchIng --> IngInput[輸入食材標籤]
    IngInput --> SearchResult
    SearchResult --> RecipeDetail[食譜詳情頁]
    Browse --> RecipeDetail

    %% 登入註冊
    AuthCheck -->|未登入| LoginPage[登入頁]
    AuthCheck -->|已登入| UserOptions{選擇操作}
    LoginPage --> HasAccount{有帳號？}
    HasAccount -->|是| DoLogin[輸入 Email + 密碼]
    HasAccount -->|否| RegisterPage[註冊頁]
    RegisterPage --> FillRegister[填寫 Email + 密碼]
    FillRegister --> DoLogin
    DoLogin --> LoginResult{登入成功？}
    LoginResult -->|失敗| LoginPage
    LoginResult -->|成功| UserOptions

    %% 已登入操作
    UserOptions --> AddRecipe[新增食譜]
    UserOptions --> MyPage[個人主頁]
    UserOptions --> AdminCheck{是管理員？}

    %% 新增食譜
    AddRecipe --> FillRecipe[填寫食譜表單\n名稱/食材/步驟/圖片]
    FillRecipe --> ValidateForm{表單驗證}
    ValidateForm -->|失敗| FillRecipe
    ValidateForm -->|成功| SaveRecipe[儲存食譜]
    SaveRecipe --> RecipeDetail

    %% 食譜詳情操作（已登入）
    RecipeDetail --> FavAction[收藏/取消收藏]
    RecipeDetail --> CommentAction[留言 + 評分]
    RecipeDetail --> IsOwner{是否為作者？}
    IsOwner -->|是| EditRecipe[編輯食譜]
    IsOwner -->|是| DeleteRecipe[刪除食譜]
    EditRecipe --> SaveRecipe
    DeleteRecipe --> Home

    %% 個人主頁
    MyPage --> MyRecipes[我的食譜清單]
    MyPage --> MyFavorites[我的收藏清單]
    MyFavorites --> RecipeDetail
    MyRecipes --> RecipeDetail

    %% 管理員後台
    AdminCheck -->|是| AdminPanel[管理員後台]
    AdminPanel --> ManageRecipes[審核/刪除食譜]
    AdminPanel --> ManageUsers[查看/停用用戶]
    AdminPanel --> ManageComments[刪除留言]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 使用者登入流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(auth.py)
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 填寫 Email + 密碼，點擊登入
    Browser->>Flask: POST /auth/login
    Flask->>Model: 查詢 User（by email）
    Model->>DB: SELECT * FROM users WHERE email=?
    DB-->>Model: 回傳 User 資料
    Model-->>Flask: User 物件

    alt 帳號存在且密碼正確
        Flask->>Flask: check_password_hash 驗證
        Flask->>Browser: 建立 Session，重導向到首頁
        Browser-->>User: 顯示首頁（已登入狀態）
    else 帳號不存在或密碼錯誤
        Flask-->>Browser: 回傳錯誤訊息
        Browser-->>User: 顯示「帳號或密碼錯誤」
    end
```

---

### 2.2 新增食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(recipes.py)
    participant RecipeModel as Recipe Model
    participant IngModel as Ingredient Model
    participant DB as SQLite

    User->>Browser: 填寫食譜表單（名稱/食材/步驟/圖片）
    Browser->>Flask: POST /recipes/create
    Flask->>Flask: 驗證 CSRF Token
    Flask->>Flask: 驗證表單欄位（Flask-WTF）

    alt 表單驗證失敗
        Flask-->>Browser: 回傳錯誤提示
        Browser-->>User: 顯示錯誤訊息，重新填寫
    else 表單驗證成功
        Flask->>Flask: 儲存上傳圖片到 static/uploads/
        Flask->>RecipeModel: 建立新 Recipe 物件
        RecipeModel->>DB: INSERT INTO recipes (...)
        DB-->>RecipeModel: 回傳新 Recipe ID

        loop 每個食材
            Flask->>IngModel: 查詢或建立 Ingredient
            IngModel->>DB: SELECT / INSERT INTO ingredients
            DB-->>IngModel: 食材 ID
            Flask->>DB: INSERT INTO recipe_ingredients（關聯）
        end

        Flask-->>Browser: 重導向到食譜詳情頁
        Browser-->>User: 顯示新增後的食譜
    end
```

---

### 2.3 食材搜尋食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(search.py)
    participant Model as Recipe + Ingredient Model
    participant DB as SQLite

    User->>Browser: 輸入食材標籤（如：雞蛋、番茄）
    Browser->>Flask: GET /search/ingredients?q=雞蛋,番茄
    Flask->>Model: 解析食材清單
    Model->>DB: SELECT recipes JOIN recipe_ingredients\nWHERE ingredient IN (雞蛋, 番茄)\nGROUP BY recipe_id\nORDER BY 匹配數量 DESC
    DB-->>Model: 符合的食譜清單（含匹配食材數）
    Model-->>Flask: Recipe 物件列表
    Flask-->>Browser: render_template('search/results.html')
    Browser-->>User: 顯示依匹配度排序的食譜結果
```

---

### 2.4 收藏食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(favorites.py)
    participant FavModel as Favorite Model
    participant DB as SQLite

    User->>Browser: 點擊食譜的「愛心」按鈕
    Browser->>Flask: POST /favorites/toggle/<recipe_id>
    Flask->>Flask: 確認使用者已登入（@login_required）
    Flask->>FavModel: 查詢是否已收藏
    FavModel->>DB: SELECT FROM favorites\nWHERE user_id=? AND recipe_id=?
    DB-->>FavModel: 查詢結果

    alt 尚未收藏
        Flask->>FavModel: 建立收藏記錄
        FavModel->>DB: INSERT INTO favorites
        DB-->>FavModel: 成功
        Flask-->>Browser: JSON { "action": "added" }
        Browser-->>User: 愛心變實心（已收藏）
    else 已收藏
        Flask->>FavModel: 刪除收藏記錄
        FavModel->>DB: DELETE FROM favorites
        DB-->>FavModel: 成功
        Flask-->>Browser: JSON { "action": "removed" }
        Browser-->>User: 愛心變空心（取消收藏）
    end
```

---

## 3. 功能清單對照表

| # | 功能 | URL 路徑 | HTTP 方法 | 權限 |
|---|------|---------|----------|------|
| 1 | 首頁（食譜列表） | `/` | GET | 公開 |
| 2 | 使用者註冊 | `/auth/register` | GET / POST | 未登入 |
| 3 | 使用者登入 | `/auth/login` | GET / POST | 未登入 |
| 4 | 使用者登出 | `/auth/logout` | POST | 已登入 |
| 5 | 食譜詳情頁 | `/recipes/<id>` | GET | 公開 |
| 6 | 新增食譜 | `/recipes/create` | GET / POST | 已登入 |
| 7 | 編輯食譜 | `/recipes/<id>/edit` | GET / POST | 作者本人 / 管理員 |
| 8 | 刪除食譜 | `/recipes/<id>/delete` | POST | 作者本人 / 管理員 |
| 9 | 關鍵字搜尋 | `/search?q=<keyword>` | GET | 公開 |
| 10 | 食材搜尋 | `/search/ingredients?q=<食材>` | GET | 公開 |
| 11 | 收藏/取消收藏 | `/favorites/toggle/<recipe_id>` | POST | 已登入 |
| 12 | 我的收藏清單 | `/user/favorites` | GET | 已登入 |
| 13 | 個人主頁 | `/user/profile` | GET | 已登入 |
| 14 | 新增留言/評分 | `/recipes/<id>/comments` | POST | 已登入 |
| 15 | 管理員 — 總覽 | `/admin/` | GET | 管理員 |
| 16 | 管理員 — 食譜管理 | `/admin/recipes` | GET / POST | 管理員 |
| 17 | 管理員 — 用戶管理 | `/admin/users` | GET / POST | 管理員 |
| 18 | 管理員 — 刪除留言 | `/admin/comments/<id>/delete` | POST | 管理員 |
