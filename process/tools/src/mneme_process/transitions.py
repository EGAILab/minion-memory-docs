"""Legal work-package status transitions (process/coordination-state.md §5).

Adopted from Minion-Agent coordination-state.md §10, §10.1, §10.2, §10.3 @ 8744bd0. Mechanical
legality only: route prerequisites that need evidence (approval recorded, findings closed) are
checked by the state validator, and semantics are never decided here.
"""

from __future__ import annotations

STATUSES: tuple[str, ...] = (
    "SCOPING",
    "CONTRACT_DRAFT",
    "CONTRACT_REVIEW",
    "PYTHON_IMPLEMENTATION",
    "IMPLEMENTATION_REVIEW",
    "REMEDIATION",
    "CONTRACT_CONVERGENCE",
    "FINAL_CONTRACT_REVIEW",
    "RUST_IMPLEMENTATION",
    "CLOSURE_REVIEW",
    "WAITING_FOR_TRIGGER",
    "CLOSED",
    "INCIDENT",
    "INVALID_UNAUTHORIZED",
    "BLOCKED_FOR_OWNER",
)

ACTIVE: frozenset[str] = frozenset(
    {
        "SCOPING",
        "CONTRACT_DRAFT",
        "CONTRACT_REVIEW",
        "PYTHON_IMPLEMENTATION",
        "IMPLEMENTATION_REVIEW",
        "REMEDIATION",
        "CONTRACT_CONVERGENCE",
        "FINAL_CONTRACT_REVIEW",
        "RUST_IMPLEMENTATION",
        "CLOSURE_REVIEW",
        "BLOCKED_FOR_OWNER",
    }
)

NON_ACTIONABLE: frozenset[str] = frozenset({"INCIDENT", "INVALID_UNAUTHORIZED"})

_TABLE: dict[str, frozenset[str]] = {
    "SCOPING": frozenset({"CONTRACT_DRAFT", "WAITING_FOR_TRIGGER", "BLOCKED_FOR_OWNER", "CLOSED"}),
    "CONTRACT_DRAFT": frozenset({"CONTRACT_REVIEW"}),
    "CONTRACT_REVIEW": frozenset(
        {"PYTHON_IMPLEMENTATION", "CONTRACT_DRAFT", "CONTRACT_CONVERGENCE", "FINAL_CONTRACT_REVIEW"}
    ),
    "PYTHON_IMPLEMENTATION": frozenset({"IMPLEMENTATION_REVIEW"}),
    "IMPLEMENTATION_REVIEW": frozenset(
        {"RUST_IMPLEMENTATION", "FINAL_CONTRACT_REVIEW", "REMEDIATION", "CONTRACT_CONVERGENCE"}
    ),
    "REMEDIATION": frozenset({"IMPLEMENTATION_REVIEW", "CONTRACT_CONVERGENCE"}),
    "CONTRACT_CONVERGENCE": frozenset({"FINAL_CONTRACT_REVIEW"}),
    "FINAL_CONTRACT_REVIEW": frozenset(
        {
            "RUST_IMPLEMENTATION",
            "REMEDIATION",
            "CONTRACT_CONVERGENCE",
            "PYTHON_IMPLEMENTATION",
            "CONTRACT_DRAFT",
            "CLOSED",
        }
    ),
    "RUST_IMPLEMENTATION": frozenset({"CLOSURE_REVIEW"}),
    "CLOSURE_REVIEW": frozenset({"CLOSED", "RUST_IMPLEMENTATION"}),
    "WAITING_FOR_TRIGGER": frozenset({"SCOPING"}),
}


def is_legal(source: str, target: str) -> bool:
    """Whether `source -> target` is in the reconciled table.

    Any active state may go to BLOCKED_FOR_OWNER. BLOCKED_FOR_OWNER may continue to any state the
    recorded governance source authorizes, so mechanically it may go to any non-terminal state
    except INCIDENT/INVALID_UNAUTHORIZED; the governance source itself is checked separately.
    """
    if source not in STATUSES or target not in STATUSES:
        return False
    if target == "BLOCKED_FOR_OWNER" and source in ACTIVE and source != "BLOCKED_FOR_OWNER":
        return True
    if source == "BLOCKED_FOR_OWNER":
        return target in ACTIVE and target != "BLOCKED_FOR_OWNER"
    return target in _TABLE.get(source, frozenset())
