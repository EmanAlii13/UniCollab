from app.services.project_service import ProjectService

class MockStorage:
    def __init__(self):
        self.data = {"projects": {}}
    def load(self):
        return self.data
    def save(self, data):
        self.data = data

def test_create_project():
    # 1️⃣ إنشاء خدمة بدون MongoDB باستخدام MockStorage
    storage = MockStorage()
    service = ProjectService(storage=storage)

    # 2️⃣ Act: إنشاء مشروع جديد
    project_id = service.create_project("AI Project", "ML System", "ayat")

    # 3️⃣ Assert: التحقق من النتائج
    assert project_id == "1"
    project = service.get_project("1")
    assert project["title"] == "AI Project"
    assert project["desc"] == "ML System"
    assert project["leader"] == "ayat"

    # 4️⃣ تحديث المشروع للتأكد من تحديث البيانات
    service.update_project("1", "AI Project Updated", None)
    updated_project = service.get_project("1")
    assert updated_project["title"] == "AI Project Updated"
