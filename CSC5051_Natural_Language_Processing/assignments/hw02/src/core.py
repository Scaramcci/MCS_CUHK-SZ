"""Shared parsing, deterministic scoring and local append-only storage."""

from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_CEILING
import fcntl
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ("instruction_following", "correctness", "relevance_completeness", "clarity")
METHODS = ("zero_shot", "few_shot", "chain_of_thought", "agent", "agent_no_feedback")


class ExperimentError(Exception):
    """Expected failure; error messages must never contain external content."""


class InvalidAssessment(ExperimentError):
    pass


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def redact(value, secrets):
    """Recursively remove configured secrets before any persistent output."""
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, dict):
        return {redact(str(k), secrets): redact(v, secrets) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(v, secrets) for v in value]
    return value


@contextmanager
def file_lock(path, blocking=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        except BlockingIOError:
            raise ExperimentError("Another process owns this run") from None
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def append_jsonl(path, value, secrets=()):
    path = Path(path)
    with file_lock(path.with_suffix(path.suffix + ".lock")):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(canonical(redact(value, secrets)) + "\n")
            handle.flush()
            os.fsync(handle.fileno())


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (ValueError, OSError):
        raise ExperimentError("Cannot read an intact JSONL journal; preserve it for recovery") from None


def write_once_json(path, value, secrets=()):
    """Never replace an existing artifact; callers serialize concurrent writes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(canonical(redact(value, secrets)) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def decimal_value(value):
    if isinstance(value, bool):
        raise ExperimentError("Invalid decimal configuration")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ExperimentError("Invalid decimal configuration") from None
    if not result.is_finite() or result < 0:
        raise ExperimentError("Invalid decimal configuration")
    return result


def micro_cny(value):
    return int((decimal_value(value) * 1_000_000).to_integral_value(rounding=ROUND_CEILING))


def parse_env(path):
    """Read KEY=VALUE data. No expansion, eval, subprocess or shell sourcing."""
    allowed = {"DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL", "EXPERIMENT_BUDGET_CNY"}
    result = {}
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        raise ExperimentError("Local env file is unavailable") from None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ExperimentError("Invalid env assignment")
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if key not in allowed:
            continue
        if key in result:
            raise ExperimentError("Duplicate env field")
        if value.startswith(("'", '"')):
            if len(value) < 2 or value[-1] != value[0]:
                raise ExperimentError("Unterminated env value")
            value = value[1:-1]
        result[key] = value
    return result


def strict_json(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidAssessment("Duplicate JSON key")
            result[key] = value
        return result
    def invalid_constant(_):
        raise InvalidAssessment("Non-finite JSON number")
    try:
        return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant)
    except (ValueError, TypeError):
        raise InvalidAssessment("Response is not strict JSON") from None


def validate_assessment(value):
    if not isinstance(value, dict) or set(value) != {"scores", "decision", "reason"}:
        raise InvalidAssessment("Invalid assessment keys")
    scores = value["scores"]
    if not isinstance(scores, dict) or set(scores) != set(DIMENSIONS):
        raise InvalidAssessment("Invalid score keys")
    if any(v is not None and (type(v) not in (int, float) or v not in (0, 1, 2)) for v in scores.values()):
        raise InvalidAssessment("Scores must be 0, 1, 2 or null")
    if not isinstance(value["reason"], str) or not value["reason"].strip() or len(value["reason"]) > 6000:
        raise InvalidAssessment("Missing or excessive reason")
    decision = "reject" if 0 in scores.values() else "keep" if all(v == 2 for v in scores.values()) else "review"
    if value["decision"] != decision:
        raise InvalidAssessment("Decision conflicts with deterministic rubric rule")
    return {"scores": scores, "decision": decision, "reason": value["reason"]}


def parse_assessment(text):
    return validate_assessment(strict_json(text))


def model_record(record):
    """Whitelist model-visible fields. Never send ids, labels or corruption metadata."""
    if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]:
        raise ExperimentError("Each record requires a nonempty string id")
    if any(not isinstance(record.get(k), str) for k in ("instruction", "input", "output")):
        raise ExperimentError("Record text fields must be strings")
    return {k: record[k] for k in ("instruction", "input", "output")}
