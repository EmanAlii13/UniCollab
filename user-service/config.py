# uniCollab - User Service - file: config.py
import os
from dotenv import load_dotenv

load_dotenv()  # لو .env موجود، هيدخل القيم منه

MONGO_URI = os.getenv("MONGO_URI", "fallback_mongo_uri_if_not_found")
DB_NAME = "unicollab_users"
JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "this_is_a_very_secure_and_long_jwt_secret_1234567890!"  # القيمة الافتراضية
)
