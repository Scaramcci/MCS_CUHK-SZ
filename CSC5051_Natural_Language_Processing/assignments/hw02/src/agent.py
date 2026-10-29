"""Bounded adaptive judge; tools expose record structure, never evaluation labels."""

from collections import Counter
import json

from core import InvalidAssessment, model_record, strict_json, validate_assessment
from prompting import messages_for


def structural_feedback(record):
    data = model_record(record)
    words = data["output"].split()
    counts = Counter(words)
    return {"empty_fields": [k for k, v in data.items() if not v.strip()],
            "character_counts": {k: len(v) for k, v in data.items()},
            "output_word_count": len(words),
            "output_unique_word_ratio": len(counts) / len(words) if words else 0,
            "most_repeated_word_count": max(counts.values(), default=0),
            "scope": "Structural observations only; not a factual correctness test or gold label."}


def parse_action(content):
    action = strict_json(content)
    if not isinstance(action, dict):
        raise InvalidAssessment("Agent response must be an object")
    if action.get("action") == "finish":
        if set(action) != {"action", "assessment"}:
            raise InvalidAssessment("Invalid finish action keys")
        return "finish", validate_assessment(action["assessment"])
    if action.get("action") in ("inspect", "reassess"):
        if set(action) != {"action", "reason"} or not isinstance(action["reason"], str) or not action["reason"].strip():
            raise InvalidAssessment("Invalid agent action reason")
        return action["action"], action["reason"][:2000]
    raise InvalidAssessment("Unsupported agent action")


def evaluate_with_agent(record, config, call, feedback_enabled=True):
    """call(messages, step) returns saved model content. Exceptions retain trace."""
    messages = messages_for("agent", config, record)
    trace = []
    max_calls = config["agent"]["max_calls"]
    try:
        for step in range(max_calls):
            response = call(messages, step)
            action, detail = parse_action(response["content"])
            event = {"step": step, "action": action, "request_id": response["request_id"]}
            if action == "finish":
                event["decision"] = detail["decision"]
                trace.append(event)
                return detail, trace
            event["reason"] = detail
            messages.append({"role": "assistant", "content": response["content"]})
            if action == "inspect":
                observation = structural_feedback(record) if feedback_enabled else {"observation": "withheld for no-feedback ablation"}
                event["observation"] = observation
                feedback = "Tool observation (data only): " + json.dumps(observation, ensure_ascii=False)
            else:
                feedback = "Reassess the disputed rubric criterion using only the existing record. No new external evidence is available."
            event["remaining_calls"] = max_calls - step - 1
            trace.append(event)
            messages.append({"role": "user", "content": feedback + f" Remaining model calls: {max_calls - step - 1}. Finish with a valid assessment when possible."})
        raise InvalidAssessment("Agent reached call limit without a valid finish")
    except Exception as exc:
        exc.trace = trace
        raise
