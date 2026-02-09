# user-service/database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# قراءة الإعدادات من .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI or not DB_NAME:
    raise RuntimeError("❌ MONGO_URI أو DB_NAME غير موجودين في ملف .env")

# إنشاء اتصال MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collection المستخدمين
users_collection = db["users"]

# دالة لإرجاع قاعدة البيانات (للاستخدام العام أو للاختبارات)
def get_db():
    return db
