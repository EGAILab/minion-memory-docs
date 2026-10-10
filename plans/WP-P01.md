# WP-P01 — Process hardening 1 (carried forward from WP-00)

**Status:** `SCOPING` (state: `process/state/WP-P01.yaml`). **Owner of this pass:** Claude.
**Requirements:** none (process-only). **Governance:** G-011 created this WP; G-009 delegation
covers acceptance after an independent `APPROVED` review.
**Route:** same as WP-00 — independent Codex review of the exact candidate, recorded as
`scoping_review`, then `SCOPING → CLOSED` once accepted onto `main`.

## Scope

| Item | Source | Change |
|---|---|---|
| 1 | WP00-CR-014 (non-blocking, Codex targeted closure review 2) | FROZEN-citation guard recognizes **positive** status labels only (`has_positive_frozen_label`): table cell that is/starts with `FROZEN`, or a line starting `FROZEN —`; rejects `NOT FROZEN`, prose/cell mentions and `->` change records. Rule documented in `spec/README.md` §3. All 49 current FROZEN requirements still satisfy it. |
| 2 | WP-00 remediation records (false round-trip mismatch) | `mneme-process state roundtrip`: raw git bytes, explicit UTF-8, CRLF/LF-insensitive, semantic equality. The validator's own `git` calls now decode UTF-8 explicitly instead of the platform code page. |
| 3 | WP-00 closure (post-acceptance records) | A `CLOSED` WP's candidates are protected by `main` ancestry; the state-only descendant rule applies only to non-closed states (`process/coordination-state.md` §2). |
| 4 | G-011 | WP-00's post-acceptance records (Codex review record 2, governance G-008..G-011, closing state) reach `main` because this WP's branch `wpP01/hardening` descends from them; accepting WP-P01 fast-forwards `main` over them. |

## Non-scope

No spec semantics, no product code, no Layer-01 decisions (NF-010…NF-019 stay with WP-01 and the
Owner).

## Controls added

Unit: 11 label-rule cases. Repository-level: 3 non-label negatives and 2 positive label forms
(CR-014), NORMATIVE citing only an unlabelled section, round-trip positive / uncommitted-change
negative / non-ASCII (em dash, ü) / CRLF-only, CLOSED-state post-acceptance records positive and
active-state chain negative. Known-bad replay: see the hand-off.

## CE-P01-01 convergence (G-018)

The validator trust boundary was characterized by Codex: 688 rows, `281b81a`.

Claude challenged and classified it, adding 12 controls. Revision 2 was AGREED by Codex
`APPROVED` (`1845aa9b`).

The implementation is in `assurance/reviews/WP-P01-remediation-claude-3.md`:
- decisions D1–D16;
- 115 row-keyed controls;
- kill run on the frozen modules: no FIX control passes.

Findings WPP01-CR-001…006 await Codex targeted closure.

## Closure (2026-10-10)

The CE-P01-01 implementation went through Codex targeted closure:
- `c7dadc07`: CHANGES_REQUIRED, CL-001…005;
- Owner G-024 fix pass, `c9be60e8`;
- recheck `e557098b`: CHANGES_REQUIRED, R1;
- Owner G-027 narrow fix, `be2f4e29`;
- R1 recheck `c73f4410`: **APPROVED** for docs `be2f4e29` / code `bb05e395`.

WPP01-CR-001…006 are all closed.

Docs `main` was fast-forwarded to `be2f4e29` under the G-009 standing delegation, and code `main`
is unchanged. WP-P01 is **CLOSED**. WP-00's post-acceptance records reached `main` through this
acceptance (G-011).

Carried forward: NF-023 (`CARGO_HOME`), now unblocked because the frozen process surface is
released.
