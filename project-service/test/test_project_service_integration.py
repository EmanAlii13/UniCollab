import os
import subprocess
import sys


def test_cli_create_join_approve():
    # 1️⃣ تحديد جذر المشروع بشكل ديناميكي
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # 2️⃣ طباعة للتأكد من المسارات
    print("Root:", root)
    print("Files in root:", os.listdir(root))
    cli_folder = os.path.join(root, "cli")
    print("Files in cli:", os.listdir(cli_folder))

    # 3️⃣ ضبط PYTHONPATH ليشمل جذر المشروع
    env = os.environ.copy()
    env["PYTHONPATH"] = root

    # 4️⃣ تحديد مسار CLI
    cli_path = os.path.join(cli_folder, "project_cli.py")
    print("CLI path:", cli_path)
    assert os.path.isfile(cli_path), f"CLI file not found at {cli_path}"

    # 5️⃣ تنفيذ الأمر
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

    # 6️⃣ التأكد من خروج أمر CLI
    print("CLI stdout:", result_create.stdout)
    print("CLI stderr:", result_create.stderr)
    assert result_create.stdout.strip()
