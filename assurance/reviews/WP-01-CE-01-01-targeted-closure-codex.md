# WP-01 CE-01-01 targeted closure — Codex

**Verdict: APPROVED**

Exact reviewed pair:
- docs `18bc390c2e8102113b3c152ff21d79fdc3201a15`;
- code `4fe3ed34c29a6868a3f5050ecee95885b73bead0`.

Authority: agreed checkpoint revision 3, `assurance/convergence/CE-01-01-classification.md` at
`8e8d30a824dee743782db6b5a5179515bcd36819`, approved by `1d99bc2c`; G-037…G-043.
Handoff/state base: `b2ebe0d6051ed917bf3d2e663b7f512448509602`.
Review branch: `review/wp01-ce1-closure`; only this record is added.

This approves the exact candidate against the agreed episode surface. It is not acceptance onto
main or permission to skip the remaining WP-01 workflow. No production files, shared contract,
authoring worktrees, findings registers, remotes or main branches were modified by Codex.
Claude's implementation record was reviewed as a claim to reproduce, not closure evidence.

## Per-finding dispositions

| Finding / authoritative original ID | Disposition for the exact pair | Independently executed evidence |
|---|---|---|
| WP01-CR-007 = WP01-PY-004: admitted-value diagnostics leak hooks/host failures | CLOSED, candidate-specific | Stable error/code/argument cells match throughout the matrix, with zero user hooks. Invalid numerics, huge values, typed diagnostics, conflict formatting, unsupported kinds and stage-order controls pass. Stage-1 diagnostics never format caller objects; subsequent diagnostics see extracted exact built-ins. |
| WP01-CR-008 = WP01-PY-008: native subclasses affect semantic values/bytes/hashes | CLOSED, candidate-specific | All canonical/normalization/hash/typed cells match the extracted-base oracle, with zero hooks. The G-042 observer verifies exact results; private numeral str markers no longer infer numbers at native seams. Genuine ancestry, stored JsonText state, byte buffers, duplicate names, cycles and G-043 control-map rejection pass their agreed oracles. |

These are technical review dispositions for this candidate, not edits to shared registers or an
Owner acceptance claim. No new finding or convergence reopening is required by the executed scope.

## Independent results

| Check | Frozen eb47635c | Candidate 4fe3ed34 |
|---|---|---|
| Original normative matrix (25,470 rows) | Prior independent Windows/Linux evidence: 21,925 old-oracle OK / 3,545 WRONG; G-042 adds 537 FIX rows | 25,470/25,470 OK on Windows and POSIX; every hook log empty |
| Exact-return observer | 537 additional previously passing failures (570 non-exact successful observations overall, including 33 already WRONG) | 0 non-exact returns among 6,775 successful value rows, both hosts |
| 75 decided boundary oracles | 25 failing / 50 regression controls under the agreed decisions | 75/75 pass, both hosts |
| CH01–CH05, M01/M02, D01/D02, CM01/CM02 | Agreed before observations and dispositions retained | Required outcomes and zero hooks independently exercised through controls/suite |
| New unit-control file | Own Windows replay: 128 failed / 124 passed | All 252 pass inside the full suite, both hosts |
| Full earlier scenarios and unit suite | Not rerun in full on frozen code in this closure | 335 passed / 5 placeholder xfails, both hosts |
| Earlier targeted-closure neighborhood probes | Earlier independent baseline | All 105 pass, identical Windows/POSIX observations |
| Direct extraction/control-input regressions | New authority-derived controls, no new semantics | All 18 pass, identical Windows/POSIX observations |
| Ruff / format / strict mypy | Not repeated on frozen code | All checks pass; 11 formatted files, 6 source files type-checked |

The frozen unit replay uses the candidate's exact test file with PYTHONPATH bound to the clean
detached eb47635c checkout. The failed cyclic controls time out as designed on frozen code; all
candidate cycles return value.cyclic. Before/after kill credit belongs to genuinely failing rows,
not the 124 frozen unit regressions that already pass. No passing control was forced to fail.

All agreed normative row IDs, witness recipes, API/seam labels and required cells match the original
driver. The independent observer is the iterative exact-return observer used for my revision-2
review, not an oracle taken from production. It checks actual runtime types after the public call
and after disabling hook capture. Exact bytes are allowed for byte-returning APIs; the explicit
library-owned OperationIdentity adapter is checked through its exact string fields. Portable
tuple input normalizes to an exact list. The observer does not call caller hooks.

All 25,470 normative observations match across hosts, including exact-return flags and ordered
hook logs. All boundary outcomes match too. The three cycle subprocess tracebacks have platform
path differences; their return code and observed MnemeValidationError value.cyclic are normalized
for semantic comparison. They are not counted as a timeout or an inferred stable error on the
candidate. Each literal boundary oracle was checked individually.

The unchanged agreed classification contains 25,560 rows: 4,116 FIX, 21,440 KEEP, 4 construction N/A.
The candidate satisfies the normative/boundary rows and nine named challenge/control additions;
construction N/A rows remain Python restrictions. All four checkpoint blockers remain resolved.

## Source review and direct regressions

The code diff is limited to values.py, the argument-call-frame annotation in identity.py and the
new unit controls. The extraction pass uses genuine ancestry and explicit built-in slots; it
copies admitted scalar/container contents before domain/typed validation. Active-path identity
detects cycles while shared non-cyclic references are copied. Map names are base strings, ordered
by UTF-16, with duplicates rejected before silent collapse. Generic domain and typed stages then
process extracted exact values. Native str subclasses, including _Numeral, cannot bypass this
extraction as internal numeric tokens.

JsonText stores text in its own base member descriptor; stored reads bypass subclass text,
_text, __dict__ and __getattribute__ overrides. G-043 rejects a non-dict call-frame before reading
arguments. bytes/bytearray input is read through base buffer operations. No virtual input protocol
is used for these normative paths. Existing isinstance uses after extraction/inside the decoder
operate on exact values or library-owned tokens, rather than caller-controlled kinds.

The 18 independent direct witnesses cover:
- insertion-order permutations for earlier unsupported kinds, cycles, duplicates and stage-2
  numerics, including stage-1 failures in later arguments;
- UTF-16 ordering with supplementary vs BMP names and native surrogate names vs stage-1 faults;
- shared aliases in tuple/map structures;
- JsonText overrides of both public text and private slot-name properties;
- non-dict call-frame refusal before inspecting a poison argument;
- hostile dict call-frames carrying bytearray JsonText.

All pass without any user hook. The 105 earlier closure probes separately retain cross-argument
stage precedence, canonical typed-field order, source-text rejection order, closed revision shape,
list/tuple binding, raw hashing and the earlier PY-001…007 neighborhoods. The unchanged full
conformance runner/scenarios and existing units pass on both hosts. No earlier closure regression
was found. These are scoped executable conclusions, not a proof over arbitrary Python programs,
concurrent mutation or every possible C-extension subtype.

## Environment and ownership facts

Windows used project-local managed CPython 3.12.8 at
`.tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe`.
POSIX used the project-local managed Linux CPython 3.12.8 in
`.tmp/cache/uv-python/cpython-3.12.8-linux-x86_64-gnu` under WSL Ubuntu.
The damaged system interpreter was not used.

POSIX tests ran on an isolated ext4/FUSE checkout created from git archive of the exact code SHA,
inside `.tmp/work/codex/ce01-closure-posix`. An executed A/a probe verified case sensitivity.
All temp, pycache, test basetemp and tooling-cache paths remained under the project; the FUSE mount
was unmounted after the suite and matrix completed. Later direct witnesses imported the same
exact detached candidate from the mounted project drive; no filename semantics are involved there.

The docs worktree is based on the handoff state head; its only descendants beyond the exact docs
candidate are the handoff and coordination-state record. The shared main docs working tree remains
on wpP01/hardening. The code candidate checkout is detached and clean; WP-01 authoring worktrees
were not touched. No implementation, remote, branch movement of authoring worktrees or push occurred.

## Evidence and reproducibility

Project-local scratch evidence:
- `.tmp/work/codex/ce01-closure-matrix/{win32,linux}/matrix.json`, controls.json and direct-regressions.json;
- `.tmp/work/codex/ce01-closure-matrix/summary.json`;
- `.tmp/work/codex/ce01-closure-tests-win.xml` and ce01-closure-negative-win.xml/log;
- `.tmp/work/codex/ce01-closure-posix/tests.xml`, tests.log, host.json and prior-regressions.json;
- `.tmp/work/codex/ce01-closure-prior-win.json`.

The original committed characterization embeds the complete witness driver. My revision-2 review
at ae875102 embeds the independent exact-return preparation and control driver. Reproduce those
against the exact candidate source via PYTHONPATH, changing only the scratch output directory.
Every shell first sources the project environment. Full-suite command: project-local Python
`-m pytest tests --basetemp=<project-local path> -p no:cacheprovider --junitxml=<project-local path>`
from minion-memory-python. For frozen kill replay, run only tests/core/test_ce0101_native_binding.py
with PYTHONPATH pointing to eb47635c. No source edits are needed.

Executed summary:

```json
{
  "normative_pass": 25470,
  "hooks_fired": 0,
  "value_returns_exact": 6775,
  "non_exact_returns": 0,
  "boundary_pass": 75,
  "direct_regressions": 18,
  "prior_regressions": 105,
  "Windows_POSIX_semantics_match": true,
  "suite": {
    "tests": 340,
    "failed": 0,
    "skipped": 5,
    "errors": 0,
    "CE_controls": 252
  },
  "frozen_unit_replay": {
    "tests": 252,
    "failed": 128,
    "skipped": 0,
    "errors": 0,
    "CE_controls": 252
  },
  "case_sensitive_POSIX": {
    "case_sensitive": true,
    "python": "3.12.8 (main, Jan 14 2025, 22:49:14) [Clang 19.1.6 ]",
    "platform": "Linux-6.18.40.1-microsoft-standard-WSL2-x86_64-with-glibc2.35",
    "TMPDIR": "/mnt/e/AI/Projects/OpenMinds/Minions/Minion-Memory/.tmp/work/codex/ce01-closure-posix/mount/process-temp"
  }
}
```

Evidence SHA-256 values (exact scratch bytes):
- Windows matrix: `508f71f4e72e21409183e7baf3f3dc8be1a67c9179d82a8325d338331ef18d51`.
- POSIX matrix: `adaf6fdc0a30ef74b6c54d296d53f402eb1bef0b1a366e2fd1d18f90fbe9bcf2`.
- Windows suite XML: `5f3006278a3d0e1d0a60e175fa450b740d76b3aa2130c189587da9066ec8dae9`.
- POSIX suite XML: `63224592746c973485f7b47c2a219ec2078c0a7c509d0474c5e5ba2e3fa07c6a`.
- Frozen unit replay XML: `ba219360e16f63161e9e07bfc61f443358bebd7b0019ecd7525f343d103c3bb5`.

## Independent direct-regression driver

Save below under `.tmp/work/codex/ce01-closure-regressions.py`, source the project environment,
bind PYTHONPATH to the exact candidate src and run with project-local managed Python. It writes
only scratch observations; it does not patch or edit production modules.

```python
import itertools,json,pathlib,sys
from minion_memory import core as m
calls=[];rows=[]
def run(label,fn,want):
    calls.clear()
    try:
        value=fn();out={'value':value}
    except m.MnemeValidationError as e:out={'error':e.code,'argument':e.argument}
    except Exception as e:out={'host':type(e).__name__}
    rows.append({'case':label,'current':out,'required':want,'hooks':list(calls),'pass':out==want and not calls})
def err(code,argument=None):return {'error':code,'argument':argument}
class Key(str):
    __hash__=object.__hash__
    def __eq__(self,other):
        calls.append('key equality');return self is other
dup={Key('x'):1,Key('x'):2};calls.clear()
cycle=[];cycle.append(cycle)
for items in ([('a',object()),('b',dup)],[('a',cycle),('b',object())],[('a',object()),('b',cycle)],[('a',float('inf')),('b',dup)],[('a',float('inf')),('b',cycle)]):
    expected='value.unsupported_type' if type(items[0][1]) is object else 'value.cyclic' if items[0][1] is cycle or items[1][1] is cycle else 'value.duplicate_key'
    for order in itertools.permutations(items):run('native ordering '+repr([k for k,v in order]),lambda order=order:m.validate_value(dict(order)),err(expected))
run('UTF16 first fault',lambda:m.validate_value({'\ue000':2**53,'\U00010000':float('inf')}),err('value.number_not_finite'))
run('surrogate name is stage2; bad value stage1',lambda:m.validate_value({'\ud800':object()}),err('value.unsupported_type'))
run('cycle b beats generic invalid a',lambda:m.compare_versions(float('inf'),cycle),err('value.cyclic','b'))
run('duplicate b beats typed invalid a',lambda:m.compare_versions(0,dup),err('value.duplicate_key','b'))
shared=[1]
run('shared alias nested in tuple/map',lambda:m.validate_value((shared,{'a':shared})),{'value':[[1],{'a':[1]}]})
class Text(m.JsonText):
    @property
    def _text(self):calls.append('_text property');raise RuntimeError('text hook')
    @property
    def text(self):calls.append('text property');raise RuntimeError('text hook')
run('private/public slot-name properties bypassed',lambda:m.validate_arguments({'value':Text('1')}),{'value':{'value':1}})
class Poison:
    @property
    def __class__(self):calls.append('argument inspected');raise RuntimeError('inspection')
from collections import UserDict
run('non-dict map rejected before poison argument',lambda:m.validate_arguments(UserDict({'a':Poison()})),{'host':'TypeError'})
class Dict(dict):
    def __getattribute__(self,n):calls.append('dict getattribute');raise RuntimeError(n)
run('admitted arg map with bytearray JsonText',lambda:m.validate_arguments(Dict({'a':m.JsonText(bytearray(b'1'))})),{'value':{'a':1}})
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'.tmp/work/codex/ce01-closure-matrix'/sys.platform
(OUT/'direct-regressions.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
assert all(r['pass'] for r in rows),[r for r in rows if not r['pass']]
print('Direct regressions passed:',len(rows))
```
