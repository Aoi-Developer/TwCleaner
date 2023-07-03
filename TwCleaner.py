import tweepy
import webbrowser
import subprocess

print("-----------------------------------------------------")
print("           Twitter黒歴史クリーナー for Windows")
print("      Dev:aoi_satou https://twitter.com/aoi_0020")
print("-----------------------------------------------------")


CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""

oauth1_user_handler = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_KEY_SECRET,
    callback="oob"
)
auth_url = str(oauth1_user_handler.get_authorization_url())

print("URLを作成しました。アドレスにアクセスして認証した後、表示されたPINを入力してください\nURL: " + auth_url)

webbrowser.open(auth_url)

# ユーザにPIN番号を入力させる
oauth_verifier = input("PIN入力: ")

oauth_token, oauth_token_secret = oauth1_user_handler.get_access_token(
    oauth_verifier
)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)
user = api.verify_credentials()

print("トークンの取得に成功しました。\n")
removename = 'ツイート'

# YESならTrue、NOならFalseを返す
def confirm():
    dic = {'y': True, 'yes': True, 'n': False, 'no': False}
    while True:
        try:
            return dic[input(user.screen_name + 'さんの' + removename + 'を消去します。よろしいですか？ [Y]es/[N]o >> ').lower()]
        except:
            pass
        print('入力された値が不正です')


# メイン
cut = 0
j = 0
if __name__ == '__main__':
  if confirm():
    while True:
      i = 0
      tweets = None
      tweets = api.user_timeline(count=200)  # 取得件数
      for tweet in tweets:
        i += 1
      if (i ==0):
        break
      else:
        for tweet in tweets:
         print(tweet.text)
         try:
           api.destroy_status(tweet.id)
         except:
           break
         print('ID:' + str(tweet.id) + 'を削除しました。\n')
         cut += 1
    print(str(cut) + '個のツイートを削除しました。')
  else:
    print('ツイート消去をキャンセルしました')
  removename = 'いいね'
  if confirm():
    while True:
      i = 0
      tweets = None
      tweets = api.get_favorites(screen_name=user.screen_name, count=200)  # 取得件数
      for tweet in tweets:
        i += 1
      if i == 0:
        break
      else:
        for tweet in tweets:
         print(tweet.text)
         try:
           api.destroy_favorite(tweet.id)
         except tweepy.errors.NotFound:
           pass
         print('ID:' + str(tweet.id) + 'のいいね削除しました。\n')
         j += 1
    print(str(cut) + '個のツイートを削除しました。')
    print(str(j) + '個のいいねを取り消しました。')
  else:
    print('いいね取り消しをキャンセルしました')
subprocess.call('PAUSE', shell=True)
