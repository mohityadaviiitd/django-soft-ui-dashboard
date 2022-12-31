import tweepy

TWITTER_API_KEY='oepijMpavfqqqpsDE072Hb28B'
TWITTER_API_SECRET='P1Ya8CrzKfrZIBIol31HF66grNLSqCBunouFWQqWMqaO4uXqm4'
TWITTER_CLIENT_ID='bGFvU3FZUXpiV05HLTVpLVFIeTQ6MTpjaQ'
TWITTER_CLIENT_SECRET='07N81g_X_f-ktsBH92P6a2m4j_PYNp4bubp_Oj5hx7zmg4YRSI'
TWITTER_OAUTH_CALLBACK_URL='https://4352-45-248-30-101.in.ngrok.io/twitter_callback'

class TwitterAPI:
    def __init__(self):
        self.api_key = TWITTER_API_KEY
        self.api_secret =TWITTER_API_SECRET
        self.client_id = TWITTER_CLIENT_ID
        self.client_secret = TWITTER_CLIENT_SECRET
        self.oauth_callback_url = TWITTER_OAUTH_CALLBACK_URL

    def twitter_login(self):
        oauth1_user_handler = tweepy.OAuthHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        request_token = oauth1_user_handler.request_token["oauth_token"]
        request_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        return url, request_token, request_secret

    def twitter_callback(self,oauth_verifier, oauth_token, oauth_token_secret):
        oauth1_user_handler = tweepy.OAuthHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        oauth1_user_handler.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
        return access_token, access_token_secret

    def get_me(self, access_token, access_token_secret):
        try:
            client = tweepy.Client(consumer_key=self.api_key, consumer_secret=self.api_secret, access_token=access_token,
                                   access_token_secret=access_token_secret)
            info = client.get_me(user_auth=True, expansions='pinned_tweet_id')
            return info
        except Exception as e:
            print(e)
            return None