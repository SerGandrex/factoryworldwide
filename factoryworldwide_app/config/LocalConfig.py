import datetime

SQLALCHEMY_DATABASE_URI = 'sqlite:///factoryworldwide.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'p9Bv<3Eid9%$i01'
EMAILHUNTER_API_KEY = '438b7edcca5e91160ec150214c0bea197ddf2665'
JWT_SECRET_KEY = 'ssdkjnvskjdfnsdngskjdnns4r9034'
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=60000)
JWT_COOKIE_SECURE = False
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=15)
JWT_COOKIE_CSRF_PROTECT = False
JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
JWT_AUTH_URL_RULE = "/login"
# JWT_HEADER_NAME = 'Authorization'
# JWT_HEADER_TYPE = 'Bearer'
# JWT_TOKEN_LOCATION = ['headers']
