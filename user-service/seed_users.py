# uniCollab - User Service - file: seed_users.py
# purpose: Seed initial users into the UniCollab User Service database
import bcrypt
from database import users_collection

students = [
    {"username": "student1", "email": "s1@uni.edu", "password": "pass1"},
    {"username": "student2", "email": "s2@uni.edu", "password": "pass2"},
    {"username": "student3", "email": "s3@uni.edu", "password": "pass3"},
    {"username": "student4", "email": "s4@uni.edu", "password": "pass4"},
    {"username": "student5", "email": "s5@uni.edu", "password": "pass5"},
]

def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

for s in students:
    s["password"] = hash_password(s["password"])
    s["role"] = None
    s["project_id"] = None
    s["last_message"] = None

users_collection.insert_many(students)
print("✅ Users seeded successfully")
