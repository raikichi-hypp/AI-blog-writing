import pyautogui
import time
import pyperclip # クリップボード操作用のライブラリが必要です (pip install pyperclip)
import os
import glob
import shutil
import subprocess

# --- 関数定義 ---
def create_new_blog_folder():
    # 既存のAIblogフォルダを検索
    existing_folders = glob.glob("AIblog*")
    # 次の番号を決定
    next_num = 1
    if existing_folders:
        numbers = [int(folder.replace("AIblog", "")) for folder in existing_folders if folder.replace("AIblog", "").isdigit()]
        if numbers:
            next_num = max(numbers) + 1
    
    # 新しいフォルダ名
    new_folder = f"AIblog{next_num}"
    os.makedirs(new_folder, exist_ok=True)
    return new_folder

def create_index_html(folder_name):
    # クリップボードの内容を取得（すでにHTML形式）
    content = pyperclip.paste()
    
    # クリップボードの内容をそのまま保存
    with open(os.path.join(folder_name, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

def publish_to_github():
    try:
        # Gitリポジトリの設定を確認
        repo_url = "https://github.com/raikichi-hypp/AI-blog-writing.git"
        
        # Gitリポジトリが初期化されているか確認
        is_new_repo = False
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            is_new_repo = True
        else:
            # リモートURLを確認・更新
            try:
                current_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
                if current_url != repo_url:
                    subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
            except subprocess.CalledProcessError:
                # originが設定されていない場合
                subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        # 現在のブランチ名を確認
        try:
            current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        except subprocess.CalledProcessError:
            # 初回コミット前は branch がない
            current_branch = None

        # Gitコマンドを実行
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Add new blog post {time.strftime('%Y-%m-%d %H:%M:%S')}"], check=True)

        if is_new_repo or not current_branch:
            # 新規リポジトリの場合、mainブランチを作成
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        else:
            # 既存のリポジトリの場合、現在のブランチにプッシュ
            subprocess.run(["git", "push", "-u", "origin", current_branch], check=True)

        print("Successfully published to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Git操作でエラーが発生しました: {e}")
        print("エラーの詳細:")
        print(f"コマンド: {e.cmd}")
        print(f"リターンコード: {e.returncode}")
        if e.output:
            print(f"エラー出力: {e.output}")
        raise
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        raise

# テキスト入力前の待機時間（秒） #カーソルの座標はパソコンによってそれぞれ異なりますので、適宜変更してください。
WAIT_BEFORE_INPUT = 10

# --- 最初の操作セット ---
first_target_x = 300
first_target_y = 750
first_text_to_type = "https://www.genspark.ai/?ref"

# --- 次の操作セット ---
second_target_x = 450
second_target_y = 220 # <-- ご使用の画面解像度によってはこのY座標が存在しない場合があります。ご確認ください。
second_text_to_type = "今日の世界のニュースの中で興味深いものを見つけ出しブログ記事にまとめてください"

# --- 追加の操作 ---
third_target_x = 1130
third_target_y = 460

# --- 長押し操作の設定 ---
long_press_x = 1333
long_press_y = 200
long_press_duration = 20 # 長押しする時間（秒）

# --- 追加の操作設定 ---
blog_click_x = 1290
blog_click_y = 230

print("--- 自動操作を開始します ---")
print(f"各テキスト入力前に {WAIT_BEFORE_INPUT} 秒待機します。")
print("操作を停止するには、マウスカーソルを画面の左上隅に素早く移動してください。") # Fail-Safeの説明

try:
    # --- 最初の操作を実行 ---
    print(f"\n1. カーソルを X:{first_target_x}, Y:{first_target_y} に移動してクリックします。")
    pyautogui.click(first_target_x, first_target_y)

    print(f"   クリックしました。{WAIT_BEFORE_INPUT}秒待機します...")
    time.sleep(WAIT_BEFORE_INPUT)

    print(f"   「{first_text_to_type}」をクリップボードにコピーして貼り付けます...")
    pyperclip.copy(first_text_to_type)
    time.sleep(0.5) # クリップボードへのコピーが完了するまで少し待つ

    # 貼り付けのキーボードショートカットを実行
    # お使いのOSに合わせてコメントを切り替えてください
    # Windows/Linux の場合: Ctrl+V
    pyautogui.hotkey('ctrl', 'v')
    # macOS の場合: Cmd+V
    # pyautogui.hotkey('command', 'v')
    print("   貼り付け完了。")

    # ユーザーが追加した待機時間
    time.sleep(WAIT_BEFORE_INPUT)

    # --- 次の操作を実行 ---
    print(f"\n2. カーソルを X:{second_target_x}, Y:{second_target_y} に移動してクリックします。")
    pyautogui.click(second_target_x, second_target_y)

    print(f"   クリックしました。{WAIT_BEFORE_INPUT}秒待機します...")
    time.sleep(WAIT_BEFORE_INPUT)

    # --- 以前追加した操作 (800, 400へのクリック) ---
    print(f"   追加操作: カーソルを X:800, Y:400 に移動してクリックします。")
    pyautogui.click(800, 400)
    print("   追加操作: クリック完了。")
    # --- 以前追加した操作ここまで ---

    print(f"   「{second_text_to_type}」をクリップボードにコピーして貼り付けます...")
    pyperclip.copy(second_text_to_type)
    time.sleep(0.5) # クリップボードへのコピーが完了するまで少し待つ

    # 貼り付けのキーボードショートカットを実行
    # お使いのOSに合わせてコメントを切り替えてください
    # Windows/Linux の場合: Ctrl+V
    pyautogui.hotkey('ctrl', 'v')
    # macOS の場合: Cmd+V
    # pyautogui.hotkey('command', 'v')
    print("   貼り付け完了。")

    # --- 追加の操作 (1130, 460へのクリック) を実行 ---
    # 2番目のテキスト入力後に続けて実行します
    print(f"\n3. カーソルを X:{third_target_x}, Y:{third_target_y} に移動してクリックします。")
    pyautogui.click(third_target_x, third_target_y)
    print("   クリック完了。")

    # --- 新規追加した操作 (長押し) ---
    print("10分待ちます")
    time.sleep(600)
    pyautogui.click(930, 160)
    print(f"\n4. カーソルを X:{long_press_x}, Y:{long_press_y} に移動して {long_press_duration}秒間長押しします。")
    # 指定座標に移動
    pyautogui.moveTo(long_press_x, long_press_y)
    # マウスボタンを押し下げる
    pyautogui.mouseDown(long_press_x, long_press_y)
    print(f"   マウスボタンを押し下げました。{long_press_duration}秒待機します...")
    # 指定時間待機
    time.sleep(long_press_duration)
    # マウスボタンを離す
    pyautogui.mouseUp(long_press_x, long_press_y)
    print("   長押し完了。マウスボタンを離しました。")

    # --- ブログ記事の保存と公開 ---
    print(f"\n5. カーソルを X:{blog_click_x}, Y:{blog_click_y} に移動してクリックします。")
    pyautogui.click(blog_click_x, blog_click_y) #この動作でブログ記事のコピーが完了します。既にhtml形式になっているので、そのまま
    print("   クリック完了。")

    # 新しいブログフォルダを作成
    new_folder = create_new_blog_folder()
    print(f"   新しいフォルダを作成しました: {new_folder}")

    # index.htmlを作成して内容を保存
    create_index_html(new_folder)
    print(f"   {new_folder}/index.htmlを作成しました")

    # GitHubに公開
    publish_to_github()

    print("\n--- すべての操作が完了しました ---")

except pyautogui.FailSafeException:
    print("\n--- Fail-Safe トリガー: カーソルを画面左上に移動したため処理を停止しました ---", flush=True)
except Exception as e:
    print(f"\n--- エラーが発生しました ---", flush=True)
    print(f"エラー内容: {e}", flush=True)