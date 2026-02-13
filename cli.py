#!/usr/bin/env python3
import requests
from getpass import getpass

BASE_USER_URL = "http://localhost:8001"      # user-service
BASE_PROJECT_URL = "http://localhost:8002"   # project-service


def login_prompt():
    while True:
        print("===== تسجيل الدخول =====")
        email = input("Email: ").strip()
        password = getpass("Password: ").strip()

        try:
            resp = requests.post(f"{BASE_USER_URL}/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                user = resp.json()
                print(f"\n✅ تم تسجيل الدخول بنجاح، مرحبا {user['username']}!\n")
                return user
            elif resp.status_code == 401:
                print("❌ كلمة المرور خاطئة، حاول مرة أخرى.\n")
            elif resp.status_code == 404:
                print("❌ المستخدم غير موجود، حاول مرة أخرى.\n")
            else:
                print(f"❌ خطأ غير متوقع: {resp.text}\n")
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ في الاتصال بالخادم: {e}\n")


def main_menu(user):
    while True:
        print("===== القائمة الرئيسية =====")
        print("1. إنشاء مشروع")
        print("2. الانضمام إلى مشروع")
        print("3. مغادرة المشروع")
        print("4. الخروج")
        choice = input("اختر خيار: ").strip()

        if choice == "1":
            create_project(user)
        elif choice == "2":
            join_project(user)
        elif choice == "3":
            leave_project(user)
        elif choice == "4":
            print("👋 تم تسجيل الخروج. إلى اللقاء!")
            break
        else:
            print("❌ خيار غير صالح، حاول مرة أخرى.\n")


def create_project(user):
    title = input("عنوان المشروع: ").strip()
    description = input("وصف المشروع: ").strip()
    data = {
        "title": title,
        "description": description,
        "leader": user["username"]
    }
    try:
        resp = requests.post(f"{BASE_PROJECT_URL}/api/v1/projects", json=data)
        if resp.status_code == 200:
            project_id = resp.json().get("project_id")
            print(f"✅ تم إنشاء المشروع بنجاح! Project ID: {project_id}\n")
        else:
            print(f"❌ فشل إنشاء المشروع: {resp.text}\n")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في الاتصال بالخادم: {e}\n")


def join_project(user):
    project_id = input("ادخل معرف المشروع للانضمام: ").strip()
    role = input("اختر الدور (leader/member): ").strip().lower()
    data = {"project_id": project_id, "role": role}

    try:
        resp = requests.post(f"{BASE_USER_URL}/users/{user['email']}/assign-project", json=data)
        if resp.status_code == 200:
            print(f"✅ تم الانضمام إلى المشروع بنجاح!\n")
        else:
            print(f"❌ فشل الانضمام: {resp.json().get('detail', resp.text)}\n")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في الاتصال بالخادم: {e}\n")


def leave_project(user):
    try:
        resp = requests.post(f"{BASE_USER_URL}/users/{user['email']}/remove-project")
        if resp.status_code == 200:
            print(f"✅ تم مغادرة المشروع بنجاح!\n")
        else:
            print(f"❌ فشل المغادرة: {resp.json().get('detail', resp.text)}\n")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في الاتصال بالخادم: {e}\n")


if __name__ == "__main__":
    user = login_prompt()
    main_menu(user)
