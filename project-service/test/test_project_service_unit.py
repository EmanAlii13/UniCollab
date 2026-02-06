from unittest.mock import MagicMock

from app.services.project_service import ProjectService


def test_create_project():
    # 1️⃣ Mock storage
    mock_storage = MagicMock()
    mock_storage.load.return_value = {"projects": {}}

    # 2️⃣ Inject mock
    service = ProjectService(mock_storage)

    # 3️⃣ Act
    project_id = service.create_project("AI", "ML", "ayat")

    # 4️⃣ Assert logic
    assert project_id == "1"

    # 5️⃣ Assert interaction
    mock_storage.save.assert_called_once()
