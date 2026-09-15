from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "policy" / "steward.yaml"


def load_policy(path: Path | None = None) -> dict:
    p = path or DEFAULT_POLICY
    with p.open() as f:
        return yaml.safe_load(f) or {}


def allow_skill(policy: dict, skill: str) -> bool:
    allowed = policy.get("allow_skills") or []
    return skill in allowed or "*" in allowed
