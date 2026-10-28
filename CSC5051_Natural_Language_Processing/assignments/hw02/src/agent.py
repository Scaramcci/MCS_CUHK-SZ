"""Future feedback-driven agent contract; no implementation or API access.

Input: one record, common rubric/settings, bounded call/token/cost allowance.
Observe: current assessment, uncertainty and validation feedback.
Decide: choose finish, reassess a specific disputed criterion, or request review.
Act: perform the selected allowed action and collect its feedback.
Repeat: use the new observation to select the next action; stop on a final
decision or step/cost limit. Unresolved items must remain review, not keep.
Output: the common assessment schema plus an auditable action/feedback trace.

A later implementation must enforce limits before calls and must demonstrate
that feedback changes action selection. This module does neither yet.
"""


def evaluate_with_agent(*args, **kwargs):
    raise NotImplementedError("Agent execution is deferred until the experiment phase.")
