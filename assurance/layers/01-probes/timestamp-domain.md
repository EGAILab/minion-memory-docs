# Probe — timestamp domain representation (WP01-CR-002)

**Question:** can the resolved HIST-004 domain (`0001-01-01T00:00:00.000000Z` …
`9999-12-31T23:59:59.999999Z`, G-022/G-029) be held losslessly in an internal integer-microsecond
representation in both languages (G-022 permits internal microseconds only with lossless round
trip)?

**Method:** two independent implementations convert canonical strings to epoch microseconds and
back, asserting exact round trips:
- **Python:** `datetime` and `timedelta`, CPython 3.12.8 (project-local).
- **Rust:** a dependency-free `i64` with civil-date arithmetic (proleptic Gregorian,
  days-from-civil / civil-from-days), rustc 1.97.1.

Their outputs are compared line by line. Sources: `.tmp/work/claude/ts-probe/{probe.py,rs/src/main.rs}`.

## Result (identical in both languages; `diff` empty)

```text
0001-01-01T00:00:00.000000Z -62135596800000000
0001-01-01T00:00:00.000001Z -62135596799999999
0001-03-01T00:00:00.000000Z -62130499200000000
1582-10-15T00:00:00.000000Z -12219292800000000
1900-02-28T23:59:59.999999Z -2203891200000001
1969-12-31T23:59:59.999999Z -1
1970-01-01T00:00:00.000000Z 0
2000-02-29T12:00:00.123456Z 951825600123456
2026-10-10T05:30:00.500000Z 1791610200500000
9999-12-31T23:59:59.999999Z 253402300799999999
```

## Conclusions

- **Fits `i64`.** The whole domain spans −62135596800000000 … 253402300799999999 µs. That fits
  `i64` exactly, at microsecond precision, with lossless round trips at both boundaries, at the
  Gregorian reform date, at century and leap days and across the epoch.
- **Not a JSON number.** Both bounds lie **outside** ±(2^53−1): epoch microseconds are an internal
  representation only, never a portable SER-008 JSON number. Timestamps cross seams as the
  canonical string (G-022), so no JSON-number form of a timestamp is defined or needed.
- **Host libraries.** Host time libraries are not the contract. Python `datetime` covers years
  1–9999 but rejects year 0. chrono accepts year 0 and emits extended years (Codex review
  `2b388e62`). Both must sit behind the HIST-004 grammar and range checks, which reject year 0000
  and out-of-range UTC results before any library sees them.
- **What this probe does not cover.** Parsing and normalizing *offset* inputs at the boundaries is
  covered by the canonical scenario `core.history.timestamp-seam-normalization`, whose
  expectations are checked by an independent strict implementation of the grammar.
