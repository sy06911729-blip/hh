import subprocess
import sys
from pathlib import Path


APP_NAME = "video-downloader"
APP_VERSION = "0.1.0"
COMPANY_NAME = "Video Downloader"
COPYRIGHT = "Copyright (c) 2024 Video Downloader"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    main_py = root / "main.py"
    if not main_py.exists():
        print("main.py introuvable.", file=sys.stderr)
        return 1

    version_file = root / "scripts" / "version_info.txt"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name",
        APP_NAME,
        "--version-file",
        str(version_file),
        str(main_py),
    ]
    if sys.platform != "win32":
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--windowed",
            "--name",
            APP_NAME,
            str(main_py),
        ]
    print("Exécution:", " ".join(cmd))
    return subprocess.call(cmd, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
