import platform
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if platform.system() != "Windows":
        print("L'installateur est disponible uniquement sur Windows.")
        return 1

    root = Path(__file__).resolve().parents[1]
    build_exe = root / "scripts" / "build_exe.py"
    installer_script = root / "scripts" / "installer.iss"

    if not build_exe.exists() or not installer_script.exists():
        print("Scripts de build manquants.", file=sys.stderr)
        return 1

    exe_result = subprocess.call([sys.executable, str(build_exe)], cwd=root)
    if exe_result != 0:
        return exe_result

    iscc = "iscc"
    return subprocess.call([iscc, str(installer_script)], cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
