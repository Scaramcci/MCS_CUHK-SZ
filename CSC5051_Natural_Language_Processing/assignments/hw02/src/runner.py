"""Concurrent dataset runner with immutable provenance and resumable predictions."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import threading
import time

from agent import evaluate_with_agent
from budget import BudgetExceeded, BudgetLedger
from client import APIClient
from core import (ROOT, METHODS, ExperimentError, InvalidAssessment, append_jsonl, file_lock,
                  fingerprint, model_record, parse_assessment, parse_env, read_jsonl,
                  redact, sha256_file, utc_now, write_once_json)
from prompting import messages_for


def code_hashes():
    files = [ROOT / "src" / (name + ".py") for name in ("core", "budget", "client", "prompting", "agent", "runner", "main")]
    files.extend(sorted((ROOT / "prompts").glob("*.txt")))
    return {str(p.relative_to(ROOT)): sha256_file(p) for p in files}


def evaluate(record, method, config, client, experiment_id, stop_event):
    calls = []
    trace = []
    start = time.monotonic()
    result = {"id": record["id"], "method": method, "status": "error", "assessment": None,
              "experiment_fingerprint": experiment_id, "timestamp": utc_now()}

    def call(messages, step):
        if stop_event.is_set():
            raise BudgetExceeded("Experiment stopped after budget/usage failure")
        try:
            response = client.complete(messages, {"experiment": experiment_id,
                "record": record["id"], "method": method, "step": step})
        except Exception as exc:
            if hasattr(exc, "call_info"):
                calls.append(exc.call_info)
            raise
        calls.append({k: v for k, v in response.items() if k != "content"})
        return response

    try:
        if method.startswith("agent"):
            assessment, trace = evaluate_with_agent(record, config, call, feedback_enabled=method == "agent")
        else:
            response = call(messages_for(method, config, record), 0)
            assessment = parse_assessment(response["content"])
        result.update(status="success", assessment=assessment)
    except InvalidAssessment as exc:
        result.update(status="invalid", error_type=type(exc).__name__)
        trace = getattr(exc, "trace", trace)
    except BudgetExceeded as exc:
        result.update(status="budget_exhausted", error_type=type(exc).__name__)
        trace = getattr(exc, "trace", trace)
        stop_event.set()
    except Exception as exc:
        result.update(status="error", error_type=type(exc).__name__)
        trace = getattr(exc, "trace", trace)
    result.update(latency_seconds=sum(c["latency_seconds"] for c in calls),
                  wall_seconds=time.monotonic() - start,
                  usage={key: sum(c.get("usage", {}).get(key, 0) for c in calls)
                         for key in ("prompt_tokens", "completion_tokens")},
                  cost_cny_upper_bound=sum(c["cost_micro_cny"] for c in calls) / 1_000_000,
                  cost_micro_cny=sum(c["cost_micro_cny"] for c in calls),
                  calls=len(calls), call_details=calls, trace=trace)
    return redact(result, client.secrets)


def run(dataset_path, output_path, methods, config, workers, allow_paid=False, env_path=None):
    if not allow_paid:
        raise ExperimentError("Explicit --allow-paid is required before credentials or network access")
    if not methods or any(m not in METHODS for m in methods) or len(set(methods)) != len(methods):
        raise ExperimentError("Invalid or duplicate methods")
    if type(workers) is not int or not 1 <= workers <= 3:
        raise ExperimentError("Workers must be between 1 and 3")
    dataset_path, output_path = Path(dataset_path).resolve(), Path(output_path).resolve()
    allowed = [ROOT / "local_artifacts", ROOT / "results/raw"]
    if not any(p.resolve() in output_path.parents for p in allowed):
        raise ExperimentError("Raw run outputs must be inside local_artifacts/ or results/raw/")
    rows = read_jsonl(dataset_path)
    if not rows:
        raise ExperimentError("Dataset is empty or missing")
    for row in rows:
        model_record(row)
    if len({r["id"] for r in rows}) != len(rows):
        raise ExperimentError("Dataset ids must be unique")
    credentials = parse_env(env_path or ROOT / ".env")
    budget = credentials.get("EXPERIMENT_BUDGET_CNY", "")
    # Invalid budget is rejected before client construction or requests.
    ledger = BudgetLedger(ROOT / "results/raw/budget.jsonl", budget, config["pricing"])
    client = APIClient(credentials, config["settings"], ledger, ROOT / "results/raw/requests", allow_paid=True)
    dataset_hash = sha256_file(dataset_path)
    provenance = {"dataset_sha256": dataset_hash, "config": config, "source_hashes": code_hashes(),
                  "model": client.model, "endpoint": client.url, "methods": methods,
                  "record_ids": [r["id"] for r in rows]}
    experiment_id = fingerprint(provenance)
    output_path.mkdir(parents=True, exist_ok=True)
    with file_lock(output_path / ".run-lock", blocking=False):
        metadata = output_path / "run.json"
        if metadata.exists():
            existing = json.loads(metadata.read_text(encoding="utf-8"))
            if existing["experiment_fingerprint"] != experiment_id:
                raise ExperimentError("Existing run differs; preserve it and use a new output directory")
        else:
            write_once_json(metadata, {**provenance, "experiment_fingerprint": experiment_id,
                                       "started_at": utc_now(), "workers": workers}, client.secrets)
        predictions = output_path / "predictions.jsonl"
        prior = read_jsonl(predictions)
        if any(r.get("experiment_fingerprint") != experiment_id for r in prior):
            raise ExperimentError("Predictions belong to a different experiment")
        done = {(r["id"], r["method"]) for r in prior}
        if len(done) != len(prior):
            raise ExperimentError("Duplicate terminal predictions found")
        jobs = [(row, method) for row in rows for method in methods if (row["id"], method) not in done]
        stop = threading.Event()
        if ledger.snapshot()["requires_reconciliation"]:
            raise BudgetExceeded("Ledger requires manual reconciliation")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(evaluate, row, method, config, client, experiment_id, stop) for row, method in jobs]
            for future in as_completed(futures):
                result = future.result()
                result["dataset_sha256"] = dataset_hash
                append_jsonl(predictions, result, client.secrets)
                print(f"{result['method']}: {result['status']} ({result['calls']} calls)", flush=True)
        final = read_jsonl(predictions)
        statuses = {status: sum(r["status"] == status for r in final)
                    for status in ("success", "invalid", "error", "budget_exhausted")}
        summary = {"experiment_fingerprint": experiment_id, "completed_predictions": len(final),
                   "statuses": statuses, "ledger": ledger.snapshot(), "timestamp": utc_now()}
        append_jsonl(output_path / "sessions.jsonl", summary)
        return summary
