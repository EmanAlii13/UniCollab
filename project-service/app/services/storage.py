import json
import os


class JSONStorage:
    def __init__(self, filename=None):
        self.filename = filename or os.path.join(
            os.path.dirname(__file__), "..", "data", "projects.json"
        )
        dir_name = os.path.dirname(self.filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"projects": {}}, f)

    def load(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)
