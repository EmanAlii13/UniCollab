import os
import subprocess
import sys
import tempfile


def test_cli_create_join_approve():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cli_path = os.path.join(root, "cli", "project_cli.py")

    assert os.path.isfile(cli_path), f"CLI file not found at {cli_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "projects.json")

        env = os.environ.copy()
        env["PYTHONPATH"] = root
        env["PROJECTS_DATA_FILE"] = data_file  # 🔥 المفتاح

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
