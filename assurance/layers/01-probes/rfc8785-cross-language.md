# Probe — RFC 8785 cross-language: reference (Python) vs off-the-shelf Rust crate

> **Current interpretation (after Codex contract review 1, `2b388e62`).** This transcript is
> historical evidence.
> - `1e21` is no longer a valid Mneme value: G-025 bounds every integral value to
>   ±(2^53−1), whatever the spelling.
> - serde_jcs emitting 2^53 is not itself an RFC 8785 defect (RFC 8785 Appendix B includes that
>   binary64 value). Such values are excluded by Mneme's domain at the SER-008 seam.
> - The crate's actual defect is code-point key ordering.
>
> See `assurance/layers/01-feasibility-matrix.md`.

Executed 2026-10-10, Windows 11, OWN-001 (CARGO_HOME and target under .tmp). rustc 1.97.1 (8bab26f4f 2026-07-14); serde_jcs version = "0.1.0"; serde_json 1 (float_roundtrip). Python: rfc8785 0.1.4, CPython 3.12.8.

Feasibility probe only — not a Minion-Memory implementation. Rust implementation remains Codex-owned.

## Rust probe (`src/main.rs`)

```rust
// WP-01 feasibility probe (not implementation): third-party RFC 8785 crate behaviour.
use sha2::{Digest, Sha256};

fn jcs(text: &str) -> String {
    let value: serde_json::Value = match serde_json::from_str(text) {
        Ok(v) => v,
        Err(e) => return format!("PARSE-ERROR {e}"),
    };
    match serde_jcs::to_string(&value) {
        Ok(s) => s,
        Err(e) => format!("JCS-ERROR {e}"),
    }
}

fn main() {
    let cases = [
        ("2^53-1", r#"{"v":9007199254740991}"#),
        ("2^53", r#"{"v":9007199254740992}"#),
        ("2^53+1", r#"{"v":9007199254740993}"#),
        ("i64max", r#"{"v":9223372036854775807}"#),
        ("float 1.0", r#"{"v":1.0}"#),
        ("float 1e21", r#"{"v":1e21}"#),
        ("float 0.1", r#"{"v":0.1}"#),
        ("-0.0", r#"{"v":-0.0}"#),
        ("utf16 order", r#"{"\uff61":1,"\ud83d\ude00":2,"b":3,"a":4}"#),
        ("lone surrogate", r#"{"v":"\ud800"}"#),
    ];
    for (name, text) in cases {
        let out = jcs(text);
        let hash = if out.starts_with('{') { format!("{:x}", Sha256::digest(out.as_bytes())) } else { String::new() };
        println!("{name:15} {out}  {hash}");
    }
}
```

## Rust output (case, canonical, sha256)

```text
2^53-1          {"v":9007199254740991}  210e9afd5b97d46616c53c7bc51eb7349d44183691bb0866ae2ef6a2b798823f
2^53            {"v":9007199254740992}  e7b4b245a4ee0feb03c7c89a9f9a4fff2ef33d95b8fc40b016cd2620d49842bd
2^53+1          {"v":9007199254740993}  b33840c3287663f6da0c495884bd8d587474de0391f249e29a4115fd1229b6e1
i64max          {"v":9223372036854775807}  4d5d642a64e3c1a8e596e38aee8553a52eac57e39cf8c545a0960260c9a9af7d
float 1.0       {"v":1}  afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91
float 1e21      {"v":1e+21}  9e24d139b060bd89f98e510a1e34d48fade6aeb668a016e6fb2e296762a3aefa
float 0.1       {"v":0.1}  8ec9c466832e74cab1700269790aa649b06fb67989ecf3ac8e6e3c2e5cde2b3a
-0.0            {"v":0}  ec4f95abcb4e2e3dbe856c3eb2f81995eacb3823d40aa2e78ed4c5e1798f664d
utf16 order     {"a":4,"b":3,"｡":1,"😀":2}  f50c2f946813c36e29e1a1ee426edceeb0495f67f085bac5bd40937d0c991099
lone surrogate  PARSE-ERROR unexpected end of hex escape at line 1 column 13  
```

## Python reference, same UTF-16 case, and the Rust bytes re-hashed

```text
utf16 order      {"a":4,"b":3,"\U0001f600":2,"\uff61":1} fd1c2455e650903b956c6ce4788b1766e7b4510c58b7ea25b563c79ed7fd122c
serde_jcs order  f50c2f946813c36e29e1a1ee426edceeb0495f67f085bac5bd40937d0c991099 (code-point order, re-hashed)
```

## Conclusions

- Conformant cases (2^53−1, 1.0, 1e21, 0.1, −0.0) are byte-identical with identical SHA-256 across the two.
- **Key order diverges**: serde_jcs orders by code point (`｡` before `😀`); RFC 8785 requires UTF-16 code-unit order (`😀` first). Hashes differ (`fd1c…` reference vs `f50c…` crate).
- **Integer range diverges**: serde_jcs emits 2^53, 2^53+1 and i64::MAX; the reference rejects ≥ 2^53. Under G-016 such values are outside the domain and must be rejected at the seam (SER-008) before canonicalization.
- Lone surrogate: serde_json rejects at parse time (consistent with SER-008 rejection).
