# tests/test_project_service_integration.py

import os
import subprocess
import sys


def test_cli_create_join_approve():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cli_folder = os.path.join(root, "cli")
    cli_path = os.path.join(cli_folder, "project_cli.py")
    assert os.path.isfile(cli_path), f"CLI file not found at {cli_path}"

    env = os.environ.copy()
    env["PYTHONPATH"] = root

    # 1️⃣ Create Project
    result_create = subprocess.run(
        [
            sys.executable,
            cli_path,
            "create-project",
            "--title",
            "AI Project",
            "--desc",
            "ML System",
            "--leader",
            "ayat",
        ],
        capture_output=True,
        text=True,
        cwd=root,
        env=env,
    )

    assert "Project created successfully" in result_create.stdout
