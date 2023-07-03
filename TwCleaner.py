from requests_oauthlib import OAuth1Session
import urllib.parse
import tweepy
import webbrowser
import subprocess

print("-----------------------------------------------------")
print("           Twitter黒歴史クリーナー for Windows")
print("      Dev:aoi_satou https://twitter.com/aoi_0020")
print("-----------------------------------------------------")


CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
API_ROOT = "https://api.twitter.com"

session = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET)
token_endpoint = API_ROOT + "/oauth/request_token"
response = session.post(token_endpoint, params={"oauth_callback": "oob"})
oauth_token = dict(urllib.parse.parse_qsl(response.text))["oauth_token"]

auth_endpoint = API_ROOT + "/oauth/authenticate"
auth_url = f"{auth_endpoint}?oauth_token={oauth_token}"
print("URLを作成しました。アドレスにアクセスして認証した後、表示されたPINを入力してください")
webbrowser.open(auth_url)
print(auth_url)
# ユーザにPIN番号を入力させる
oauth_verifier = input("PIN入力: ")

access_token_endpoint = API_ROOT + "/oauth/access_token"
session = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET,
                        oauth_token, oauth_verifier)

response = session.post(
    access_token_endpoint,
    params={"oauth_verifier": oauth_verifier},
)

parsed_response = dict(urllib.parse.parse_qsl(response.text))
oauth_token = parsed_response["oauth_token"]
oauth_token_secret = parsed_response["oauth_token_secret"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)
user = api.verify_credentials()

print("トークンの取得に成功しました。\n")

# YESならTrue、NOならFalseを返す
def confirm():
    dic={'y':True,'yes':True,'n':False,'no':False}
    while True:
        try:
            return dic[input(user.screen_name + 'さんのツイートを消去します。よろしいですか？ [Y]es/[N]o >> ').lower()]
        except:
            pass
        print('入力された値が不正です')


# メイン
cut = 0
if __name__ == '__main__':
  if confirm():
    while True:
      i=0
      tweets = None
      tweets = api.user_timeline(count=200)  # 取得件数
      for tweet in tweets:
        i=i+1
      if (i ==0):
        break
      else:
        for tweet in tweets:
         print(tweet.text)
         try:
           api.destroy_status(tweet.id)
         except Exception:
           break
         print('ID:' + str(tweet.id) + 'を削除しました。\n')
         cut = cut + 1
    print(str(cut) + '個のツイートを削除しました。')
    
  else:
    print('キャンセルしました')
subprocess.call('PAUSE', shell=True)
