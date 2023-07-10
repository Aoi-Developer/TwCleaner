import tweepy
import webbrowser
import subprocess
import os

print("-----------------------------------------------------")
print("           Twitter黒歴史クリーナー for Windows")
print("      Dev:aoi_satou https://twitter.com/aoi_0020")
print("-----------------------------------------------------")

CONSUMER_KEY = "3rJOl1ODzm9yZy63FACdg"
CONSUMER_KEY_SECRET = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"

settxt = "Setting.txt"

# トークンの取得
def makekey():
    oauth1_user_handler = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET,callback="oob")
    # 認証用のURLを取得する
    auth_url = str(oauth1_user_handler.get_authorization_url())
    print("URLを作成しました。アドレスにアクセスして認証した後、表示されたPINを入力してください\nURL: " + auth_url)
    webbrowser.open(auth_url)
    # ユーザにPIN番号を入力させる
    oauth_verifier = input("PIN入力: ")
    # アクセストークンを取得する
    oauth_token, oauth_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
    # ファイルに書き込みをする
    f = open(settxt, mode="w")
    f.write(str(oauth_token) + "\n" + str(oauth_token_secret))
    f.close()
    print("トークンの取得に成功しました。\n")
    # トークンを返す
    return oauth_token, oauth_token_secret

# YESならTrue、NOならFalseを返す
def confirm(removename):
    dic = {"y": True, "yes": True, "n": False, "no": False}
    while True:
        try:
            return dic[input(removename + " [Y]es/[N]o >> ").lower()]
        except:
            pass
        print("入力された値が不正です。")

# 前回取得したtokenの使用確認
if os.path.exists(settxt):
    removename = "前回取得したAPIKeyが見つかりました。使用しますか?"
    if confirm(removename):
        # Keyの読み込み
        with open(settxt, "r") as f:
            lines = f.readlines()
            oauth_token = lines[0].rstrip()
            oauth_token_secret = lines[1].rstrip()
            f.close()
    else:
        oauth_token, oauth_token_secret = makekey()
else:
    oauth_token, oauth_token_secret = makekey()

# 認証処理
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

user = api.verify_credentials()

removename = user.screen_name + "さんのツイートを消去します。よろしいですか？"

# メイン
cut = 0
j = 0
if __name__ == "__main__":
    if confirm(removename):
        while True:
            tweets = []
            tweets = api.user_timeline(count=200)  # 取得件数
            if len(tweets) == 0:
                break
            else:
                for tweet in tweets:
                    print(tweet.text)
                    try:
                        api.destroy_status(tweet.id)
                    except:
                        break
                    print("ID: " + str(tweet.id) + " を削除しました。\n")
                    cut += 1
        print(str(cut) + " 個のツイートを削除しました。")
    else:
        print("「ツイート消去」をキャンセルしました")
    removename = user.screen_name + " さんのいいねを取り消します。よろしいですか？"
    if confirm(removename):
        while True:
            tweets = []
            tweets = api.get_favorites(screen_name=user.screen_name, count=200)  # 取得件数
            if len(tweets) == 0:
                break
            else:
                for tweet in tweets:
                    print(tweet.text)
                    try:
                        api.destroy_favorite(tweet.id)
                    except tweepy.errors.NotFound:
                        pass
                    print("ID: " + str(tweet.id) + " のいいね削除しました。\n")
                    j += 1
        print(str(cut) + " 個のツイートを削除しました。")
        print(str(j) + " 個のいいねを取り消しました。")
    else:
        print("「いいね取り消し」をキャンセルしました")

subprocess.call("PAUSE", shell=True)
