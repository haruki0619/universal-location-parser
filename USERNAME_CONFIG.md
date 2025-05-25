# ユーザー名生成設定の説明

## 🎯 ユーザー名の設定方法

`config.py` でユーザー名の生成方法を設定できます。

### 📝 設定項目

```python
# ユーザー名設定
USERNAME_MODE = "filename"        # モード選択
BASE_USERNAME = "user"            # ベースユーザー名
FIXED_USERNAME = "timeline_user"  # 固定ユーザー名
```

### 🔧 USERNAME_MODE の選択肢

#### 1. `"filename"` (デフォルト)
ファイル名からユーザー名を生成
```
ファイル名                  → 生成されるユーザー名
timeline_android.json     → user_timeline_android
my_iphone_data.json       → user_my_iphone_data
2024_march.json           → user_2024_march
```

#### 2. `"fixed"`
すべて同じユーザー名を使用
```
全ファイル → timeline_user (FIXED_USERNAMEの値)
```

#### 3. `"custom"`
ファイル名の内容に応じて自動分類
```
ファイル名                  → 生成されるユーザー名
android_timeline.json     → android_user
iphone_data.json          → iphone_user
timeline_2024.json        → timeline_user
location_history.json     → location_user
other_file.json           → user_other_file
```

### 🎨 カスタマイズ例

#### 例1: 全て同じユーザー名にしたい場合
```python
USERNAME_MODE = "fixed"
FIXED_USERNAME = "my_timeline"
```
→ 結果: 全データが `my_timeline` ユーザー

#### 例2: シンプルなファイル名ベース
```python
USERNAME_MODE = "filename"
BASE_USERNAME = "data"
```
→ 結果: `data_ファイル名` 形式

#### 例3: 端末別に自動分類
```python
USERNAME_MODE = "custom"
```
→ 結果: ファイル名に応じて android_user, iphone_user 等に自動分類

### 🔄 設定の変更

1. `config.py` を編集
2. `python main.py` を実行
3. 新しい設定でCSVが生成される

この設定により、データの管理方法を柔軟に変更できます！
