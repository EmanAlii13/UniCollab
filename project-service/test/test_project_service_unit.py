from app.services.project_service import ProjectService
from app.storage.storage_interface import StorageInterface

class MockStorage(StorageInterface):
    def __init__(self):
        self.data = {"projects": {}}

    def load(self):
        return self.data

    def save(self, data):
        self.data = data

def test_create_project():
    storage = MockStorage()
    service = ProjectService(storage=storage)
    project_id = service.create_project("AI Project", "ML System", "ayat")
    
    # بدل المقارنة بـ "1"، نتأكد فقط أن الـ ID موجود في dict
    assert project_id in storage.data["projects"]
    
    project = service.get_project(project_id)
    assert project["title"] == "AI Project"
    assert project["desc"] == "ML System"
    assert project["leader"] == "ayat"
