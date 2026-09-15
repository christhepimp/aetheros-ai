"""Tiny planner.

This is intentionally local and rule-based so the repo runs offline.
Swap `plan()` for an LLM API later; keep skills and policy the same.
"""

from .policy import allow_skill, load_policy
from .skills import SKILLS, skill_shell


def plan(intent: str) -> list[dict]:
    text = intent.lower()
    steps: list[dict] = []
    if any(w in text for w in ("who", "machine", "kernel", "linux", "witness", "where")):
        steps.append({"skill": "witness"})
    if any(w in text for w in ("id", "identity", "host")):
        steps.append({"skill": "identity"})
    if text.startswith("!") or text.startswith("run "):
        cmd = intent[1:].strip() if text.startswith("!") else intent[4:].strip()
        steps.append({"skill": "shell", "command": cmd})
    if not steps:
        steps.append({"skill": "identity"})
        steps.append(
            {
                "skill": "say",
                "text": (
                    "I am Aether. I am the OS process, not an app. "
                    "Ask me to witness this machine, or prefix a command with ! "
                    "once policy allows shell."
                ),
            }
        )
    return steps


def act(intent: str) -> str:
    policy = load_policy()
    chunks: list[str] = [f"# intent\n{intent}\n"]
    for step in plan(intent):
        skill = step["skill"]
        if skill == "say":
            chunks.append(step["text"])
            continue
        if not allow_skill(policy, skill):
            chunks.append(f"policy denied skill={skill}")
            continue
        if skill == "shell":
            chunks.append(skill_shell(step.get("command", "true")))
            continue
        fn = SKILLS.get(skill)
        if fn is None:
            chunks.append(f"unknown skill={skill}")
            continue
        chunks.append(fn())
    return "\n".join(chunks)
