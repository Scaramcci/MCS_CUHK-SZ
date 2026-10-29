"""Cross-process append-only reservation ledger, in integer micro-CNY."""

from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import uuid

from core import ExperimentError, append_jsonl, decimal_value, file_lock, micro_cny, read_jsonl, utc_now


class BudgetExceeded(ExperimentError):
    pass


class BudgetLedger:
    def __init__(self, path, ceiling_cny, pricing):
        self.path = Path(path)
        self.limit = micro_cny(ceiling_cny)
        if self.limit <= 0 or self.limit > 10_000_000:
            raise ExperimentError("Budget must be positive and at most the authorized 10 CNY")
        self.input_rate = decimal_value(pricing["input_cny_per_million"])
        self.output_rate = decimal_value(pricing["output_cny_per_million"])
        if not self.input_rate or not self.output_rate:
            raise ExperimentError("Verified positive rates are required")
        self.prior = micro_cny(pricing["prior_spend_cny_upper_bound"])
        self.rate_signature = {"input": str(self.input_rate), "output": str(self.output_rate)}
        self.guard = self.path.with_suffix(".budget-lock")
        with file_lock(self.guard):
            events = read_jsonl(self.path)
            if not events:
                self._append({"event": "initialize", "limit": self.limit, "prior": self.prior, "rates": self.rate_signature})
            else:
                self._state(events)

    def _append(self, event):
        append_jsonl(self.path, {"time": utc_now(), **event})

    def _state(self, events):
        first = events[0]
        if (first.get("event") != "initialize" or first.get("prior") != self.prior
                or first.get("rates") != self.rate_signature):
            raise ExperimentError("Budget ledger configuration changed; manual reconciliation required")
        limit = min(self.limit, first["limit"])
        amounts = {}
        settled = set()
        for event in events[1:]:
            if event["event"] == "reserve":
                if event["reservation_id"] in amounts:
                    raise ExperimentError("Duplicate budget reservation")
                amounts[event["reservation_id"]] = event["amount"]
            elif event["event"] == "settle":
                rid = event["reservation_id"]
                if rid not in amounts or rid in settled:
                    raise ExperimentError("Invalid budget settlement")
                amounts[rid] = event["amount"]
                settled.add(rid)
            else:
                raise ExperimentError("Unknown budget event")
        return self.prior + sum(amounts.values()), limit, amounts, settled

    def cost(self, input_tokens, output_tokens):
        if any(type(v) is not int or v < 0 for v in (input_tokens, output_tokens)):
            raise ExperimentError("Invalid provider usage")
        # Rates are CNY / million tokens: multiplying yields micro-CNY directly.
        return int((Decimal(input_tokens) * self.input_rate + Decimal(output_tokens) * self.output_rate).to_integral_value(rounding=ROUND_CEILING))

    def reserve(self, input_bound, output_bound, request_id):
        amount = self.cost(input_bound, output_bound)
        with file_lock(self.guard):
            events = read_jsonl(self.path)
            spent, limit, _, _ = self._state(events)
            if any(e.get("exceeded_reservation") for e in events):
                raise BudgetExceeded("Prior charge exceeded reservation; manual reconciliation required")
            if spent + amount > limit:
                raise BudgetExceeded("Cumulative budget cannot cover the next request")
            rid = uuid.uuid4().hex
            self._append({"event": "reserve", "reservation_id": rid, "request_id": request_id,
                          "amount": amount, "input_bound": input_bound, "output_bound": output_bound})
            return rid, amount

    def settle(self, reservation_id, input_tokens, output_tokens, token_bound_exceeded=False):
        actual = self.cost(input_tokens, output_tokens)
        with file_lock(self.guard):
            _, _, amounts, settled = self._state(read_jsonl(self.path))
            if reservation_id not in amounts or reservation_id in settled:
                raise ExperimentError("Reservation cannot be settled twice")
            reserved = amounts[reservation_id]
            self._append({"event": "settle", "reservation_id": reservation_id, "amount": actual,
                          "input_tokens": input_tokens, "output_tokens": output_tokens,
                          "exceeded_reservation": actual > reserved or token_bound_exceeded})
            if actual > reserved or token_bound_exceeded:
                raise BudgetExceeded("Provider charge exceeded reservation; stop and reconcile")
        return actual

    def snapshot(self):
        with file_lock(self.guard):
            events = read_jsonl(self.path)
            spent, limit, _, _ = self._state(events)
        exceeded = any(e.get("exceeded_reservation") for e in events)
        return {"spent_or_reserved_micro_cny": spent, "limit_micro_cny": limit,
                "requires_reconciliation": exceeded}
