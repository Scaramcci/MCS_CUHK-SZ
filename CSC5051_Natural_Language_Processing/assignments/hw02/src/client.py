"""Explicit paid HTTPS requests with durable reservations and no automatic retries."""

import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from budget import BudgetExceeded
from core import ExperimentError, append_jsonl, canonical, file_lock, fingerprint, read_jsonl, redact, utc_now


class IncompleteRequest(ExperimentError):
    pass


class ProviderFailure(ExperimentError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderFailure("Redirects are disabled")


class APIClient:
    def __init__(self, credentials, settings, ledger, cache_dir, allow_paid=False, transport=None):
        if not allow_paid:
            raise ExperimentError("Explicit --allow-paid is required")
        key = credentials.get("DEEPSEEK_API_KEY", "")
        model = credentials.get("DEEPSEEK_MODEL", "")
        base = credentials.get("DEEPSEEK_BASE_URL", "").rstrip("/")
        parts = urlsplit(base)
        if (not key or not model or any(c.isspace() for c in key)
                or parts.scheme != "https" or not parts.hostname or parts.username
                or parts.password or parts.query or parts.fragment):
            raise ExperimentError("Missing credentials/model or invalid HTTPS base URL")
        self.url = base if base.endswith("/chat/completions") else base + "/chat/completions"
        self.key, self.model = key, model
        self.secrets = (key,)
        self.settings = settings
        self.ledger = ledger
        self.cache_dir = Path(cache_dir)
        self.transport = transport or self._http
        if model != settings.get("allowed_requested_model"):
            raise ExperimentError("Requested model differs from the model with verified pricing")
        if type(settings.get("max_completion_tokens")) is not int or not 1 <= settings["max_completion_tokens"] <= 4096:
            raise ExperimentError("Invalid completion token cap")
        if settings.get("reasoning_effort") != "none":
            raise ExperimentError("This comparison requires reasoning_effort none")

    def _http(self, payload):
        request = Request(self.url, data=canonical(payload).encode("utf-8"),
                          headers={"Authorization": "Bearer " + self.key, "Content-Type": "application/json"}, method="POST")
        try:
            with build_opener(NoRedirect()).open(request, timeout=self.settings["timeout_seconds"]) as response:
                raw = response.read(2_000_001)
                if len(raw) > 2_000_000:
                    raise ProviderFailure("Provider response exceeds local limit")
                return json.loads(raw)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError):
            raise ProviderFailure("Provider request failed; reservation retained, no automatic retry") from None

    def complete(self, messages, context_id):
        payload = {"model": self.model, "messages": messages, "temperature": self.settings["temperature"],
                   "max_completion_tokens": self.settings["max_completion_tokens"], "reasoning_effort": "none"}
        request_id = fingerprint({"context": context_id, "url": self.url, "payload": payload})
        journal = self.cache_dir / (request_id + ".jsonl")
        with file_lock(self.cache_dir / (request_id + ".request-lock")):
            events = read_jsonl(journal)
            if events:
                if events[-1].get("event") == "response":
                    return {**events[-1]["result"], "cached": True}
                error = IncompleteRequest("Existing incomplete/failed request requires reconciliation; no retry")
                error.call_info = events[-1].get("call_info", {
                    "request_id": request_id, "usage": {}, "cost_micro_cny": events[0]["reserved_micro_cny"],
                    "latency_seconds": 0, "cost_basis": "retained_reservation", "cached": True})
                raise error
            input_bound = len(canonical(messages).encode("utf-8")) + 512
            if input_bound > self.settings["max_input_tokens_bound"]:
                raise ExperimentError("Input exceeds configured conservative token bound")
            rid, reserved = self.ledger.reserve(input_bound, self.settings["max_completion_tokens"], request_id)
            append_jsonl(journal, {"event": "request", "time": utc_now(), "request_id": request_id,
                                   "reservation_id": rid, "reserved_micro_cny": reserved,
                                   "input_bound": input_bound, "payload": payload}, self.secrets)
            start = time.monotonic()
            call_info = {"request_id": request_id, "reservation_id": rid, "usage": {},
                         "cost_micro_cny": reserved, "cost_basis": "retained_reservation",
                         "latency_seconds": 0, "cached": False}
            try:
                response = self.transport(payload)
                elapsed = time.monotonic() - start
                append_jsonl(journal, {"event": "provider_response", "time": utc_now(),
                                       "latency_seconds": elapsed, "response": response}, self.secrets)
                usage = response.get("usage", {})
                inp, out = usage.get("prompt_tokens"), usage.get("completion_tokens")
                if any(type(x) is not int or x < 0 for x in (inp, out)):
                    raise ProviderFailure("Provider usage is missing or invalid; reservation retained")
                call_info.update(usage={"prompt_tokens": inp, "completion_tokens": out},
                                 cost_micro_cny=self.ledger.cost(inp, out), cost_basis="usage_peak_rates")
                cost = self.ledger.settle(rid, inp, out,
                    token_bound_exceeded=(inp > input_bound or out > self.settings["max_completion_tokens"]
                                          or response.get("model") != self.settings["expected_returned_model"]))
                choice = response["choices"][0]
                if choice.get("finish_reason") != "stop":
                    raise ProviderFailure("Provider did not finish normally")
                content = choice["message"]["content"]
                if not isinstance(content, str):
                    raise ProviderFailure("Provider response has no text content")
                result = {"request_id": request_id, "reservation_id": rid, "content": content,
                          "usage": {"prompt_tokens": inp, "completion_tokens": out},
                          "cost_micro_cny": cost, "latency_seconds": elapsed, "cached": False,
                          "cost_basis": "usage_peak_rates", "returned_model": response.get("model"),
                          "finish_reason": choice.get("finish_reason")}
                result = redact(result, self.secrets)
                append_jsonl(journal, {"event": "response", "time": utc_now(), "result": result}, self.secrets)
                return result
            except Exception as exc:
                call_info["latency_seconds"] = time.monotonic() - start
                append_jsonl(journal, {"event": "failure", "time": utc_now(), "error_type": type(exc).__name__,
                                       "reservation_id": rid, "reserved_micro_cny": reserved,
                                       "call_info": call_info}, self.secrets)
                error = BudgetExceeded("Budget/usage anomaly; stop the experiment") if isinstance(exc, BudgetExceeded) else ProviderFailure("Request failed; see local journal; no automatic retry")
                error.call_info = redact(call_info, self.secrets)
                raise error from None
