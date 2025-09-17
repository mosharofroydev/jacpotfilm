# ----------------------------
# Bot & API Config
# ----------------------------
API_ID = 1234567                  # উদাহরণ ID
API_HASH = "abcdef1234567890abcdef1234567890"  # উদাহরণ Hash
BOT_TOKEN = "1234567890:ABCDEF_example_bot_token"

# MongoDB
MONGO_URI = "mongodb+srv://user:pass@cluster0.mongodb.net/movie_bot?retryWrites=true&w=majority"

# Admins & Channels
ADMINS = [111111111]                # উদাহরণ admin user ID
FILE_STORE_CHANNEL = -1001234567890 # উদাহরণ file store channel
LOG_CHANNEL = -1009876543210        # উদাহরণ log channel

# Bot Options
MAX_BUTTONS = 8
TUTORIAL_MODE = True
SPELLCHECK = True
IMDB_INFO = False
PUBLIC_FILE_STORE = True
AUTO_FILTER = True
LONG_IMDB_DESCRIPTION = True
MULTI_LANGUAGE = True
BATCH_DOWNLOAD = True

# Video Expiry / Auto Delete
VIDEO_EXPIRY_DAYS = 5
SEARCH_RESULT_AUTO_DELETE = 300  # 5 minutes

# Forward Protection
FORWARD_PROTECT = True
ADVANCED_FORWARD = True  # Future: watermark + user-id tagging

# Branding
BRANDING_TEXT = "🎬 Jacpotfilm"

# Monetization / Ads
ENABLE_ADS = True
SHORT_LINKS = True
SPONSOR_BANNERS = True

# Cloud / Storage
ENABLE_CLOUD_STORE = True  # S3 / Google Drive / Telegram

# Token System
ONE_TIME_TOKEN = True
QR_CODE_VERIFY = False

# Analytics
ENABLE_ANALYTICS = True
