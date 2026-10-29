"""Record one real command, its outputs, exit status and exact input versions."""

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import uuid


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required after --")
    if not all(c.isalnum() or c in "-_" for c in args.label):
        parser.error("label must contain only letters, numbers, hyphens or underscores")

    root = Path(__file__).resolve().parents[1]
    started = dt.datetime.now(dt.timezone.utc)
    run_id = started.strftime("%Y%m%dT%H%M%S%fZ") + "-" + args.label + "-" + uuid.uuid4().hex[:6]
    output = root / "results" / "selftest" / run_id
    output.mkdir(parents=True, exist_ok=False)
    inputs = sorted((root / "project_release_to_students").glob("*"))
    inputs += sorted((root / "src").glob("*.sql"))
    inputs += sorted((root / "tests").glob("*"))
    record = {
        "executor": "main Codex agent /root (implementation self-test)",
        "started_utc": started.isoformat(),
        "command": command,
        "cwd": str(root),
        "platform": platform.platform(),
        "python": sys.version,
        "input_sha256": {str(p.relative_to(root)): sha256(p) for p in inputs if p.is_file()},
        "random_seed": "N/A: deterministic SQL, unordered result comparison",
    }
    before = time.perf_counter()
    with (output / "stdout.txt").open("w") as stdout, (output / "stderr.txt").open("w") as stderr:
        try:
            process = subprocess.run(command, cwd=root, stdout=stdout, stderr=stderr, timeout=600)
            code = process.returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            stderr.write(str(error) + "\n")
            code = 124 if isinstance(error, subprocess.TimeoutExpired) else 127
    record.update(exit_code=code, elapsed_seconds=time.perf_counter() - before,
                  finished_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    (output / "record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(output.relative_to(root))
    print((output / "stdout.txt").read_text(), end="")
    print((output / "stderr.txt").read_text(), end="", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
