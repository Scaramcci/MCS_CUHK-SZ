"""Exercise scaffold boundaries without API access or actual credentials."""

import contextlib
import importlib.util
import io
from pathlib import Path
import socket
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scaffold", ROOT / "src/main.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sentinel = "synthetic-secret-for-local-test-only"
original_read = Path.read_text


def guarded_read(path, *args, **kwargs):
    if path.name == ".env":
        raise AssertionError("scaffold must not read local credentials")
    return original_read(path, *args, **kwargs)


def invoke(args, expected):
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        assert module.main(args) == expected
    assert sentinel not in output.getvalue()
    return output.getvalue()


with patch.dict("os.environ", {"DEEPSEEK_API_KEY": sentinel, "EXPERIMENT_BUDGET_CNY": "10"}), \
     patch.object(Path, "read_text", guarded_read), \
     patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
     patch.object(socket, "getaddrinfo", side_effect=AssertionError("network forbidden")):
    invoke(["check"], 0)
    for method in module.METHODS:
        assert "NOT A MODEL RESPONSE" in invoke(["preview", "--method", method], 0)
    assert "Unavailable" in invoke(["run"], 2)
    with patch.object(module, "load_config", side_effect=ValueError(sentinel)):
        invoke(["check"], 1)

print("PASS: check/previews require no env read or socket/DNS; configured key/budget cannot enable run; error values are not printed.")
