# Privacy, retention and data minimization — DRAFT normalization

Conventions: `spec/README.md`.

### PRIV-001 — Durability is bounded by privacy and minimization
<a id="priv-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §17] [FND §7.1] [FND §19] [MVP §9]

Data durability is constrained by privacy and data minimization: research value does not justify
retaining unnecessary sensitive raw data indefinitely. Retention policy is separate from
evidential authority. "Store everything forever" is not a Foundation requirement.

### PRIV-002 — Richest useful observation, not everything
<a id="priv-002"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §9] [R00 §7.1] [R03 §18] [R04 §20] [R04 §10]

Persist the richest observation reasonably useful for reinterpretation, subject to explicit
privacy, retention and minimization choices. Collect only observations with plausible
reinterpretation value; do not require or retain heavy audio/video/raw artifacts by default merely
because the schema permits them.

### PRIV-003 — Local by default; no silent transmission
<a id="priv-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §9] [R03 §18] [R04 §20]

Free-text, work and professional content stays local by default unless the user explicitly exports
or enables an external evaluator. Optional integrations must not silently copy local history into
remote services; export adapters must not silently transmit private history; backup and export
preserve user control.

### PRIV-004 — Logs and telemetry avoid content
<a id="priv-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §20] [R05 §15]

Logs, debug exports and telemetry must not include full raw responses or private content unless
explicitly requested; telemetry prefers bounded metadata over content.

### PRIV-005 — Honest about what was not retained
<a id="priv-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R05 §6] [R03 §21]

When retention/privacy policy intentionally avoids keeping full raw content, the retained
representation must be honest about what was not preserved.

### PRIV-006 — Agent memory privacy is first-class
<a id="priv-006"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §15]

Agent memory may contain user, project, tool, workplace or other sensitive context. Scope
enforcement, retention, deletion/retirement semantics, raw-content minimization and auditability
are first-class. A projection may omit private records even when they are semantically relevant.
