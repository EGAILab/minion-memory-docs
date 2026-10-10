# Probe — RFC 8785 vs integer domain, negative zero, key order (WP-01 premise)

> **Current interpretation (after Codex contract review 1, `2b388e62`).** This transcript is
> historical evidence.
> - `1e21` is no longer a valid Mneme value: G-025 bounds every integral value to
>   ±(2^53−1), whatever the spelling.
> - serde_jcs emitting 2^53 is not itself an RFC 8785 defect (RFC 8785 Appendix B includes that
>   binary64 value). Such values are excluded by Mneme's domain at the SER-008 seam.
> - The crate's actual defect is code-point key ordering.
>
> See `assurance/layers/01-feasibility-matrix.md`.

Executed 2026-10-10 on Windows 11, CPython 3.12.8 via uv 0.10.9, package `rfc8785` 0.1.4, under OWN-001 (`.tmp/work/claude`). Command: `uv run --no-project --python 3.12 --with rfc8785 python probe_jcs.py`.

## Script

```python
"""WP-01 premise probe (agent-workflow §5 / Minion-Agent §9.3): RFC 8785 vs signed 64-bit integers."""

import importlib.metadata
import json

import rfc8785

print("rfc8785", importlib.metadata.version("rfc8785"))
cases = {
    "2^53-1": 2**53 - 1,
    "2^53": 2**53,
    "2^53+1": 2**53 + 1,
    "i64 max": 2**63 - 1,
    "i64 min": -(2**63),
    "float 1.0": 1.0,
    "float 1e21": 1e21,
    "float 0.1": 0.1,
    "-0.0": -0.0,
}
for name, value in cases.items():
    try:
        out = rfc8785.dumps({"v": value}).decode("utf-8")
    except Exception as error:  # noqa: BLE001 - probe records every outcome
        out = f"RAISES {type(error).__name__}: {error}"
    as_double = float(value)
    exact = isinstance(value, float) or int(as_double) == value
    print(f"{name:10} jcs={out!r:60} double-exact={exact}")
print("json.dumps(2**53+1) =", json.dumps(2**53 + 1), "| as double:", repr(float(2**53 + 1)))
print("key order:", rfc8785.dumps({"b": 1, "a": 2, "é": 3, "\U0001f600": 4}).decode("utf-8"))
```

## Output

```text
rfc8785 0.1.4
i64 max    jcs='RAISES IntegerDomainError: 9223372036854775807 exceeds safe integer domain for JSON floats' double-exact=False
i64 min    jcs='RAISES IntegerDomainError: -9223372036854775808 exceeds safe integer domain for JSON floats' double-exact=True
float 1.0  jcs='{"v":1}'                                                    double-exact=True
float 1e21 jcs='{"v":1e+21}'                                                double-exact=True
float 0.1  jcs='{"v":0.1}'                                                  double-exact=True
-0.0       jcs='{"v":0}'                                                    double-exact=True
json.dumps(2**53+1) = 9007199254740993 | as double: 9007199254740992.0
jcs order       : ['a', 'b', '\\U0001f600', '\\uff61']
codepoint order : ['a', 'b', '\\uff61', '\\U0001f600']
-0.0 vs 0.0 same bytes: True
```

The first run's key-order line failed on the Windows console code page (not a library result); it was re-run with `PYTHONIOENCODING=utf-8`, giving the last three lines above.
