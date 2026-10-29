"""Prepare a local import copy for a non-superuser-owned PostgreSQL database.

Only the COMMENT on the preinstalled, administrator-owned plpgsql extension is
omitted. No schema, data or executable database behavior is changed.
"""

from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
source = root / "project_release_to_students" / "MyDATASET.dump"
target = root / "data" / "import" / "MyDATASET.sql"
comment = b"COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';"
original = source.read_bytes()
if original.count(comment) != 1:
    raise SystemExit("Expected exactly one known extension COMMENT; refusing to alter this input.")
prepared = original.replace(comment, b"-- Extension COMMENT omitted for non-superuser import.", 1)
target.parent.mkdir(parents=True, exist_ok=True)
if target.exists() and target.read_bytes() != prepared:
    raise SystemExit("Existing prepared import differs; preserve it and investigate before regenerating.")
target.write_bytes(prepared)
print(json.dumps({
    "source": str(source.relative_to(root)),
    "source_sha256": hashlib.sha256(original).hexdigest(),
    "target": str(target.relative_to(root)),
    "target_sha256": hashlib.sha256(prepared).hexdigest(),
    "change": "Omit exactly one COMMENT ON EXTENSION plpgsql statement; no schema/data changes.",
}, indent=2))
