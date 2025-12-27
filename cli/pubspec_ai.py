import argparse
import json
import sys
from pathlib import Path

import requests


def main() -> int:
    ap = argparse.ArgumentParser(description="Pubspec AI Extractor (file path input)")
    ap.add_argument("--input", required=True, help="Path to pubspec.yaml")
    ap.add_argument("--api", default="http://localhost:8000", help="API base URL")
    ap.add_argument("--timeout", type=int, default=600, help="Timeout seconds")
    args = ap.parse_args()

    p = Path(args.input)
    if not p.exists():
        print(f"[error] File not found: {p}", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8", errors="ignore")
    url = args.api.rstrip("/") + "/extract"

    r = requests.post(url, json={"pubspec_text": text}, timeout=args.timeout)
    try:
        data = r.json()
    except Exception:
        print(f"[error] Non-JSON response (HTTP {r.status_code}):", file=sys.stderr)
        print(r.text, file=sys.stderr)
        return 1

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
