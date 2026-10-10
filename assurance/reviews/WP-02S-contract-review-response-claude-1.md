# WP-02S — response to contract review 1 (Claude)

**Review:** Codex `2c2e1d08`, CHANGES_REQUIRED for docs `bc362b9f` / code `95d1df60`. Its record is
imported unchanged as `assurance/reviews/WP-02S-contract-review-codex.md`. Both findings are
accepted.

| Finding | Disposition | Change |
|---|---|---|
| WP02S-CR-001: facet-name grammar (path C) | **Owner G-064**, recorded verbatim: exactly two lowercase ASCII segments joined by one dot; each segment 1–128 bytes, starting with `a`–`z` or `0`–`9`, then `[a-z0-9_-]`; no device-name restriction. So `agent.con` is a well-formed unknown facet (preserved and hidden), while `agent.session.x` is `scope.invalid`. The Owner chose option 3, not the author's recommendation (option 1). | `spec/scope.md` "Facet names (G-064)". Four new controls: `agent.con` validates; a 129-byte segment and a non-ASCII segment are invalid; an `agent.con` record is hidden. |
| WP02S-CR-002: `validate_scope` not specified (author defect) | Repaired. `validate_scope(scope)` is defined: one argument, returning the normalized value and preserving well-formed unknown facets. Like every single-argument primitive (Layer 01 convention), its errors name **no** argument. `scopes_equal` validates `a`, then `b`. Both codes are added to the SER-008 stage table. | `spec/scope.md` "Matching" and "Errors"; `spec/serialization.md` stage table. Eleven `validate_scope` error expectations no longer pin `argument: scope`. |

**Corpus.** 73 steps, still DRAFT. The only expectation that changed is the dropped `argument` on the
eleven single-argument `validate_scope` errors.
