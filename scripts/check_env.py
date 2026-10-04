"""Check that the ClaimPilot development tools are installed.

Run:  uv run --python 3.12 scripts/check_env.py
Standard library only, works on Windows, macOS, Linux and WSL.
"""

import platform
import re
import shutil
import subprocess
import sys

MIN_PYTHON = (3, 12)


def run(cmd: list[str]) -> str | None:
    """Return the command's output, or None if it is missing or fails."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20, check=True)
    except (subprocess.SubprocessError, OSError):
        return None
    return (result.stdout or result.stderr).strip()


def version(text: str | None) -> str:
    match = re.search(r"\d+\.\d+(\.\d+)?", text or "")
    return match.group(0) if match else "?"


def check_python() -> tuple[bool, str]:
    current = sys.version_info[:3]
    ok = current >= MIN_PYTHON
    return ok, ".".join(map(str, current))


def check_tool(cmd: list[str]) -> tuple[bool, str]:
    out = run(cmd)
    return out is not None, version(out) if out else "not found"


def check_docker_running() -> tuple[bool, str]:
    out = run(["docker", "info", "--format", "{{.ServerVersion}}"])
    return out is not None, out or "daemon not running"


CHECKS = [
    # name, function, required, hint
    ("Python >= 3.12", check_python, True, "uv python install 3.12"),
    ("uv", lambda: check_tool(["uv", "--version"]), True, "https://docs.astral.sh/uv/getting-started/installation/"),
    ("Git", lambda: check_tool(["git", "--version"]), True, "https://git-scm.com/downloads"),
    ("Docker", lambda: check_tool(["docker", "--version"]), True, "Install Docker Desktop"),
    ("Docker running", check_docker_running, True, "Start Docker Desktop"),
    ("Docker Compose", lambda: check_tool(["docker", "compose", "version"]), True, "Included with Docker Desktop"),
    ("VS Code (code)", lambda: check_tool(["code", "--version"]), False, "https://code.visualstudio.com"),
]


def main() -> int:
    print(f"ClaimPilot environment check  ({platform.system()} {platform.release()})\n")
    failed = 0
    for name, check, required, hint in CHECKS:
        ok, detail = check()
        status = "OK" if ok else ("MISSING" if required else "optional")
        print(f"  {status:<9} {name:<16} {detail}")
        if not ok:
            print(f"            -> {hint}")
            failed += required
    print("\nAll required tools are ready." if not failed else f"\n{failed} required tool(s) missing.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
