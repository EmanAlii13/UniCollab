# user-service/seed_users.py
from services.user_service import hash_password
from database import users_collection

students = [
    {"username": "student1", "email": "s1@uni.edu", "password": "pass1"},
    {"username": "student2", "email": "s2@uni.edu", "password": "pass2"},
    {"username": "student3", "email": "s3@uni.edu", "password": "pass3"},
    {"username": "student4", "email": "s4@uni.edu", "password": "pass4"},
    {"username": "student5", "email": "s5@uni.edu", "password": "pass5"},
]

# تحضير البيانات قبل الإدخال
for s in students:
    s["password"] = hash_password(s["password"])
    s["role"] = None
    s["project_id"] = None
    s["last_message"] = None

# إدخال البيانات بدون تكرار (idempotent)
for s in students:
    if not users_collection.find_one({"email": s["email"]}):
        users_collection.insert_one(s)

print("✅ Seeded initial students successfully!")
