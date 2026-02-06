# tests/test_project_service_unit.py

from unittest.mock import MagicMock
from app.services.project_service import ProjectService

def test_create_project():
    # 1️⃣ Mock storage
    mock_storage = MagicMock()
    mock_storage.load.return_value = {"projects": {}}

    # 2️⃣ Inject mock
    service = ProjectService()
    service.projects = None  # force mock mode
    service.data = {"projects": {}}

    # 3️⃣ Act
    project_id = service.create_project("AI", "ML", "ayat")

    # 4️⃣ Assert logic
    # إذا كنا بنستخدم mock storage، ID يجب أن يكون رقمي كسلسلة
    assert project_id == "1"
    project = service.get_project("1")
    assert project["title"] == "AI"
    assert project["leader"] == "ayat"
