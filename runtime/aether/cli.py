import sys

from .brain import act


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    intent = " ".join(args).strip() or "who are you and what machine is this?"
    print(act(intent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
