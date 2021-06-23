from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl



def get_authenticate_endpoint_url(cons_key, cons_sec, oauth_callback_url):
    '''
    CONSUMER_KEYを用いてエンドポイントURLを取得．リクエストに失敗した場合はレスポンスを返す
    '''
    tw_session = OAuth1Session(cons_key, cons_sec)
    request_token_url = "https://api.twitter.com/oauth/request_token"
    response = tw_session.post(
        request_token_url, params={"oauth_callback": oauth_callback_url}
    )
    if response.status_code == 200:
        request_token = dict(parse_qsl(response.content.decode("utf-8")))
        authenticate_url = "https://api.twitter.com/oauth/authenticate"
        authenticate_endpoint_url = "{}?oauth_token={}".format(
            authenticate_url, request_token["oauth_token"]
        )
        return True, authenticate_endpoint_url
    else:
        return False, response.text


def get_access_token(cons_key, cons_sec, oauth_token, oauth_ver):
    '''
    CONSUMERキーとOAuthトークン,認証を用いてOAuth Token Secretを取得．
    ''' 
    tw_session = OAuth1Session(cons_key, cons_sec, oauth_token, oauth_ver)
    access_token_url = "https://api.twitter.com/oauth/access_token"
    res = tw_session.post(
        access_token_url,
        params={"oauth_verifier": oauth_ver},
    )
    if res.status_code == 200:
        return True, dict(parse_qsl(res.content.decode("utf-8")))
    else:
        return False, res.text


if __name__ == "__main__":
    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = "http://localhost:8000/auth"
    try:
        from .local_settings import apikeys
    except ImportError:
        print('try another path')
        from local_settings import apikeys


    print(
        get_authenticate_endpoint_url(
            cons_key=apikeys.CONSUMER_KEY,
            cons_sec=apikeys.CONSUMER_KEY_SECRET,
            oauth_callback_url=oauth_callback,
        )
    )
