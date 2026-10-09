# Design

Mneme architecture is defined by the authority bundle (Foundation v2.3 and its companions); this
directory does not restate it. It records Minion-Memory-side design decisions the bundle leaves to
implementation, each with its finding/decision provenance.

## D-001 — Repository topology (WP-00, PROPOSED)

```text
Minion-Memory/                       project root (not a git repository)
├── artifacts/                       upstream bundles, read-only
├── minion-memory/                   code repo: manifest, conformance, schemas, Python, Rust
├── minion-memory-docs/              docs repo: reference, spec, process, assurance, plans, design
├── .tmp/{process-temp,cache,work}   OWN-001 scratch/caches (never committed)
└── review-worktrees/                OWN-001 review worktrees
```

Matches the kickoff §11 target shape and the bundle bootstrap topology. The two repos are siblings,
never nested; validated by `mneme-process check repos`. Rust crate layout is Codex's decision.
