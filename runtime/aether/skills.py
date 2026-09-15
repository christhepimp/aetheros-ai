import platform
import subprocess
from pathlib import Path


def skill_identity() -> str:
    return (
        f"host={platform.node()}\n"
        f"system={platform.system()} {platform.release()}\n"
        f"python={platform.python_version()}\n"
        f"machine={platform.machine()}\n"
    )


def skill_witness() -> str:
    """Read-only local witness. On-device use lab/witness.sh instead."""
    bits = [skill_identity()]
    for cmd in (["uname", "-a"], ["id"]):
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
            bits.append(out.strip())
        except Exception as exc:  # noqa: BLE001 — lab code
            bits.append(f"{' '.join(cmd)}: {exc}")
    return "\n".join(bits) + "\n"


def skill_shell(command: str, cwd: Path | None = None) -> str:
    """Constrained shell. Policy layer must already have approved this."""
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=30,
    )
    body = (result.stdout or "") + (result.stderr or "")
    return f"exit={result.returncode}\n{body}"


SKILLS = {
    "identity": lambda **_: skill_identity(),
    "witness": lambda **_: skill_witness(),
}
