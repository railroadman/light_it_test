SOCIAL_AUTH_TWITTER_KEY = 'llD91yGiR5xul8gNdyhwtvFJ2'
SOCIAL_AUTH_TWITTER_SECRET = '8bK8lguFhUwLodpe05dFUtf7dqq38lPljeDyAB2mwY3mZY9PE1'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY  = "700350979413-7q8f5notaqoubi3didheto8q4rlhnm48.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET  = "TFIDxRtltriA77HgLBKy6R1I"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'soc_auth.views.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_ALWAYS_ASSOCIATE = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL  = '/wall'