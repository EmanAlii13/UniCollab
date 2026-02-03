from app.services.project_service import ProjectService
from app.services.storage import JSONStorage


def test_create_project(tmp_path):
    db = tmp_path / "test.json"
    storage = JSONStorage(str(db))
    service = ProjectService(storage)

    project_id = service.create_project("AI", "ML", "ayat")

    data = storage.load()
    assert project_id in data["projects"]
    assert data["projects"][project_id]["leader"] == "ayat"
