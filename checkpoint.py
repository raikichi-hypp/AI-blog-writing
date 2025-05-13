import pyautogui
import time
import pyperclip
import os
import glob
import shutil
import subprocess
import schedule
import datetime
import sys
import webbrowser

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
        # Gitリポジトリの初期化
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/raikichi-hypp/AI-blog-writing.git"], check=True)

        # 現在のブランチを確認
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
        current_branch = result.stdout.strip()
        
        # mainブランチが存在しない場合は作成
        if not current_branch:
            subprocess.run(["git", "checkout", "-b", "master"], check=True)
            current_branch = "master"
        
        # 変更をステージングに追加
        subprocess.run(["git", "add", "."], check=True)
        
        try:
            # コミットを作成（変更がない場合はスキップ）
            subprocess.run(["git", "commit", "-m", f"Update blog content {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:  # 変更がない場合
                print("変更がないため、コミットをスキップします。")
                return
            raise

        try:
            # リモートの変更を取得
            subprocess.run(["git", "fetch", "origin", current_branch], check=True)
            
            # リモートの変更をマージ
            try:
                subprocess.run(["git", "pull", "--rebase", "origin", current_branch], check=True)
            except subprocess.CalledProcessError:
                # コンフリクトが発生した場合は、ローカルの変更を優先
                subprocess.run(["git", "rebase", "--skip"], check=True)
            
            # 変更をプッシュ
            subprocess.run(["git", "push", "-u", "origin", current_branch], check=True)
            print("GitHubへの公開が完了しました。")
            
        except subprocess.CalledProcessError as e:
            print(f"Git操作でエラーが発生しました: {e}")
            print("エラーの詳細:")
            print(f"コマンド: {e.cmd}")
            print(f"リターンコード: {e.returncode}")
            if e.stdout:
                print(f"標準出力: {e.stdout.decode()}")
            if e.stderr:
                print(f"エラー出力: {e.stderr.decode()}")
            raise

    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        raise

def run_scheduled():
    print(f"\n=== スケジュール実行を開始します（{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}） ===")
    success = main_process()
    if not success:
        print("エラーが発生しました。次のスケジュール実行をお待ちください。")

def run_scheduler():
    show_initial_messages()
    print("\nスケジューラーを開始します。")
    print("実行スケジュール:")
    print("- 毎日 午前4:00")
    print("- 毎日 午前4:30")
    
    # スケジュールの設定
    schedule.every().day.at("04:00").do(run_scheduled)
    schedule.every().day.at("04:30").do(run_scheduled)
    
    try:
        while True:
            # 次の実行までの時間を計算
            next_run = schedule.next_run()
            if next_run:
                time_until_next = next_run - datetime.datetime.now()
                print(f"\n次の実行まで: {time_until_next}")
            
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにスケジュールをチェック
            
    except KeyboardInterrupt:
        print("\nプログラムを終了します。Ctrl+Cが押されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
        sys.exit(1)

def main_process():
    try:
        # --- 最初の操作を実行 ---
        print(f"\n1. https://www.genspark.ai/?refを開きます。")
        webbrowser.open("https://www.genspark.ai/?ref")
        time.sleep(10)
        print("10秒待機します")
        webbrowser.open("https://www.genspark.ai/?ref")
        print("10秒待機します")
        time.sleep(10)

        # --- 以前追加した操作 (800, 400へのクリック) ---
        print(f"   追加操作: カーソルを X:800, Y:400 に移動してクリックします。")
        pyautogui.click(800, 400)
        print("   追加操作: クリック完了。")
        # --- 以前追加した操作ここまで ---

        print(f"   「今日の世界のニュースの中で興味深いものを見つけ出しブログ記事にまとめてください」をクリップボードにコピーして貼り付けます...")
        pyperclip.copy("今日の世界のニュースの中で興味深いものを見つけ出しブログ記事にまとめてください")
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
        print(f"\n3. カーソルを X:1130, Y:460 に移動してクリックします。")
        pyautogui.click(1130, 460)
        print("   クリック完了。")

        # --- 新規追加した操作 (長押し) ---
        print("10分待ちます")
        time.sleep(600)
        pyautogui.click(930, 160)
        print(f"\n4. カーソルを X:1333, Y:200 に移動して 20秒間長押しします。")
        # 指定座標に移動
        pyautogui.moveTo(1333, 200)
        # マウスボタンを押し下げる
        pyautogui.mouseDown(1333, 200)
        print(f"   マウスボタンを押し下げました。20秒待機します...")
        # 指定時間待機
        time.sleep(20)
        # マウスボタンを離す
        pyautogui.mouseUp(1333, 200)
        print("   長押し完了。マウスボタンを離しました。")

        # --- ブログ記事の保存と公開 ---
        print(f"\n5. カーソルを X:1290, Y:230 に移動してクリックします。")
        pyautogui.click(1290, 230) #この動作でブログ記事のコピーが完了します。既にhtml形式になっているので、そのまま
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
        return True
    except pyautogui.FailSafeException:
        print("\n--- Fail-Safe トリガー: カーソルを画面左上に移動したため処理を停止しました ---", flush=True)
        return False
    except Exception as e:
        print(f"\n--- エラーが発生しました ---", flush=True)
        print(f"エラー内容: {e}", flush=True)
        return False

def show_initial_messages():
    print("--- 自動操作を開始します ---")
    print(f"各テキスト入力前に 10 秒待機します。")
    print("操作を停止するには、マウスカーソルを画面の左上隅に素早く移動してください。") # Fail-Safeの説明

def run_with_loop():
    show_initial_messages()
    while True:
        main_process()

# プログラムの実行
if __name__ == "__main__":
    # コマンドライン引数でモードを選択
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        run_scheduler()
    else:
        print("使用方法:")
        print("通常実行: python blogtest.py")
        print("スケジュール実行: python blogtest.py --schedule")
        choice = input("スケジュール実行を開始しますか？ (y/n): ").lower()
        if choice == 'y':
            run_scheduler()
        else:
            run_with_loop()  # 通常の繰り返し実行
