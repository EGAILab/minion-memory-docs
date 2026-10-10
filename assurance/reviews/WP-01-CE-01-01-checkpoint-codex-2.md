# WP-01 CE-01-01 checkpoint revision 2 — Codex targeted re-review

**Verdict: CHANGES_REQUIRED**

Exact artifact: `assurance/convergence/CE-01-01-classification.md` at
`3d4e83398a4cd0cc3f96b61d0967b9b1cdf63853`.
Handoff/state base: `4c31dbbf4021e469ed4f3029fcf5bccc72a7d69c`.
Frozen code: `eb47635c6ea997f030d04b8099366044a2f702aa`.
Review branch: `review/wp01-ce1-checkpoint-2`; only this record is added.

CE01-CP-001–003 are resolved at the checkpoint level. One newly explicit semantic reading needs an
Owner decision before this exact checkpoint can become AGREED FOR IMPLEMENTATION. This is not a
reopening of unrelated rows and does not close the implementation findings WP01-CR-007/008.
Production stays frozen. No production, contract, authoring-worktree, register or remote changes
were made; project-local managed Python and project-local scratch/cache paths were used throughout.

## Per-finding dispositions

| Finding | Disposition | Evidence and limits |
|---|---|---|
| CE01-CP-001 | RESOLVED | §4.1 requires `issubclass(type(x), built-in base)`, prohibits all three unsafe lookup forms, and agrees with §2. Genuine custom-metaclass subclasses remain admitted. Independent M01/M02 executions confirm the frozen observations: M01 returns a subtype, so FIX under G-042; M02 rejects with unsupported_type and no hook, so KEEP. |
| CE01-CP-002 | RESOLVED | §4.3 explicitly bypasses text, __dict__ and __getattribute__ descriptors through genuine storage. D01 is a failing descriptor witness; D02 guards against replacing it with an obj.__dict__ read. Both were independently executed and their FIX/KEEP dispositions match. B066 remains a FIX control. |
| CE01-CP-003 | RESOLVED | Independent re-execution of the committed driver with an independently written iterative exact-return observer reproduces every original ID/case/outcome/hook/status, promotes exactly the same 537 IDs, and agrees with every normative disposition. Literal boundary oracles give 25 FIX / 50 KEEP. Kill accounting now distinguishes failures from regression controls; N01323 is not forced to fail. G-042 checks apply to applicable portable outputs, including recursive elements and names; tuple becomes list. |

The SER-008 correction removes the text-only duplicate claim, separates native/text stage-1
ordering, and carries earlier unsupported-kind precedence and the active-path cycle point. It is
faithful to G-039/G-040. No regression was found in the unchanged rejection/normalization oracles.

## CE01-CP-004 — Non-dict argument-map failure policy is not decided by G-041

- Classification: `REQUIREMENT_UNCERTAIN`.
- Path: **C — observable semantic choice**.
- `owner_decision_required: true`.
- Status: OPEN; blocking: CE-01-01 checkpoint's non-dict control-map failure policy.
- Sources: reviewed artifact §3 C03 and §4.3; SER-008 completion; verbatim G-041 in
  `reference/governance/2026-10-10-owner-layer01-decisions.md` at the reviewed artifact SHA;
  frozen public `core/values.py:384` and exported `validate_arguments`.

G-041 requires argument maps to be read as **base dict entries** without hooks. That supports the
dict-family input restriction by authority reading. It does **not** say how a non-dict call-frame
input is rejected, or that such a failure is a caller programming error outside the stable Mneme
error vocabulary. The proposed checkpoint explicitly chooses `TypeError` in §3, while the public
frozen signature accepts Mapping and currently accepts UserDict and a custom Mapping.

Executed witnesses on both hosts:
- `validate_arguments(UserDict({"a":1,"b":2}))` returns those values on frozen code.
- A custom Mapping containing a=1 is accepted and invokes its len/iter/getitem hooks on frozen code.
- An ordinary dict call-frame already returns the values with no hooks.

The new restriction is supported; the proposed **failure category** is not thereby fixed. At
least two observable policies preserve the already-decided no-hook/base-dict rule:

| Option | Observable response |
|---|---|
| Caller misuse | Reject non-dict call-frame input as TypeError, before inspecting any supplied arguments; explicitly state this public binding precondition. |
| Validation rejection | Reject it with a MnemeValidationError (for example value.unsupported_type), with a declared stage/argument policy; explicitly include the framework control seam in that vocabulary. |

These differ in exception class, code and the boundary between caller misuse and validation. That
is not merely choosing an internal representation or naming an already-decided fault. G-041 fixes
extraction but does not resolve those observables. Recommendation: route this narrow options packet
to the Owner, record the chosen failure/precondition policy, then make the checkpoint and a literal
non-dict negative control agree with it. Either policy must preserve zero hooks; do not silently
resume arbitrary Mapping hook dispatch. No agent-selected TypeError policy is approved here.

## The other flagged G-041 reading

**decode_json bytearray acceptance: path A, no Owner decision required.** G-041's question explicitly
names “bytes/bytearray subclasses at the raw-hash and JSON-bytes seams,” and its selected answer
requires reading those buffers as their underlying bytes. Interpreting a bytearray containing b'1'
as the same JSON byte text as bytes b'1' follows that authority. Exact bytearray and genuine subclasses
must have the same underlying-buffer semantics; hooks are bypassed. The B016–B028 even-row oracle
of decoded exact integer 1 is sound. Frozen TypeError on these inputs is a fix witness under this
new decision, rather than a reason to preserve the former narrower implementation annotation.

This reading does not admit bytearray as a generic native JSON payload value or silently widen
other buffer types. It governs only the explicitly decided byte-text/raw-hash seams.

## Independent execution and row audit

Both Windows and WSL Ubuntu used project-local managed CPython 3.12.8 against the clean detached
frozen checkout. Full re-executed matrices compare equal across hosts, including the exact-return
observer, current outcomes and ordered hooks. Independent controls also compare equal.

The original committed witness driver was extracted from the unchanged characterization. I added
only an independent exact-return observer and changed its scratch output path. No implementation
function was patched. The observer runs after hook capture stops and checks exact runtime types
iteratively; it does not invoke subclass methods. Exact bytes are allowed for canonical-byte APIs;
the explicit library-owned OperationIdentity adapter is checked through its exact string fields,
not mislabeled a caller-supplied portable subclass. In prose, “exact returned values” must be read
in this portable-value/binding scope rather than as removing declared framework return adapters.

Every old row field, including ID/case and old OK/WRONG status, matches the original evidence.
The exact-return observer promotes **537** previously OK rows, and every promoted ID equals the
revision's FIX classification. All other normative dispositions match as well.

| Check | Independent result |
|---|---:|
| Original normative rows | 25,470 |
| Original OK / WRONG | 21,925 / 3,545 |
| Additional G-042 FIX rows | 537 |
| Revised normative FIX / KEEP | 4,082 / 21,388 |
| Literal boundary FIX / KEEP | 25 / 50 |
| Challenge rows | 5 FIX |
| Added controls | M01/D01 FIX; M02/D02 KEEP |
| Unique classified IDs | 25,558 |
| Total FIX / KEEP / N/A | 4,114 / 21,440 / 4 |

All 75 boundary dispositions were independently recomputed from their executed values/hooks and
literal decided oracles. In particular, B072–B075 are KEEP and a normalized tuple's exact list output
is not mistaken for a defect. For cycles the original bounded observation is a failure to return,
not an invented frozen error code; the proposed value.cyclic oracle comes from G-040.

No production suite was run: this is targeted checkpoint re-review, not implementation closure.
The three prior assurance findings can remain resolved. Resolve only CE01-CP-004 before approval;
then the revised checkpoint can be reconsidered without reopening unrelated rows.

## Executed additional controls and seam witnesses

The complete observations below match on both hosts. Hook capture excludes caller construction
and result inspection. M01 exact_int=false is the frozen G-042 failure, not a claim of hook dispatch.

```json
{
  "M01": {
    "outcome": {
      "value": 1,
      "exact_int": false
    },
    "hooks": []
  },
  "M02": {
    "outcome": {
      "code": "value.unsupported_type"
    },
    "hooks": []
  },
  "D01": {
    "outcome": {
      "host": "RuntimeError",
      "message": "text hook"
    },
    "hooks": [
      "text property"
    ]
  },
  "D02": {
    "outcome": {
      "value": {
        "value": 1
      }
    },
    "hooks": []
  },
  "dict-map": {
    "outcome": {
      "value": {
        "a": 1,
        "b": 2
      }
    },
    "hooks": []
  },
  "UserDict-map": {
    "outcome": {
      "value": {
        "a": 1,
        "b": 2
      }
    },
    "hooks": []
  },
  "bytearray-text": {
    "outcome": {
      "host": "TypeError",
      "message": "'<=' not supported between instances of 'str' and 'int'"
    },
    "hooks": []
  },
  "custom-map": {
    "outcome": {
      "value": {
        "a": 1
      }
    },
    "hooks": [
      "map len",
      "map iter",
      "map getitem"
    ]
  }
}
```

## Reproduction recipe

First dot-source the project environment in every shell. Use project-local managed Python 3.12.8;
set PYTHONPATH to the frozen checkout's minion-memory-python/src (and the local rfc8785==0.1.4 dev
oracle for the full matrix). The scripts below reside under `.tmp/work/codex/`; the matrix
preparer extracts the committed original driver, adds the independent observer, and writes a
scratch driver. Run that generated driver, then the controls. Both scripts are embedded for review;
they are probes, not production changes. All output stays under the project.

### Independent matrix observer preparation

```python
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
text=(ROOT/'review-worktrees/docs-wp01-ce1-checkpoint-2/assurance/convergence/CE-01-01-characterization.md').read_text(encoding='utf-8')
driver=text.split('```python\n',1)[1].rsplit('\n```',1)[0]+'\n'
def replace(a,b):
    global driver
    assert driver.count(a)==1,(a,driver.count(a))
    driver=driver.replace(a,b)
replace("OUT = ROOT / '.tmp/work/codex/ce01-native' / sys.platform","OUT = ROOT / '.tmp/work/codex/ce01-checkpoint2-matrix' / sys.platform")
replace('ROWS = []','''RETURN_EXACT = None
def exact_return(value):
    pending=[value]
    while pending:
        x=pending.pop(); t=type(x)
        if x is None or any(t is b for b in (bool,int,float,str,bytes)): continue
        if t is list: pending.extend(list.__iter__(x));continue
        if t is dict:
            for k,v in dict.items(x):
                if type(k) is not str:return False
                pending.append(v)
            continue
        # Explicit library-owned typed adapter; its portable fields must be exact strings.
        if t is m.OperationIdentity:
            if type(x.source_namespace) is str and type(x.source_operation_id) is str:continue
        return False
    return True
class MeasuredRows(list):
    def append(self,row):
        row['return_exact']=RETURN_EXACT
        list.append(self,row)
ROWS = MeasuredRows()''')
replace('    global ACTIVE\n    LOG.clear()','    global ACTIVE, RETURN_EXACT\n    RETURN_EXACT = None\n    LOG.clear()')
replace("        result = {'value': plain(result)}","        RETURN_EXACT = exact_return(result)\n        result = {'value': plain(result)}")
(ROOT/'.tmp/work/codex/ce01-checkpoint2-matrix.py').write_text(driver,encoding='utf-8')
print('Original committed driver extracted; independent iterative exact-return observer added')
```

### Independent control driver

```python
import collections,collections.abc,json,pathlib,sys
from minion_memory import core as m
calls=[]
def obs(fn):
    calls.clear()
    try:
        out=fn()
        kind=type(out)
        result={'value':out,'exact_int':kind is int} if kind is int or issubclass(kind,int) else {'value':out}
    except m.MnemeValidationError as e:result={'code':e.code}
    except Exception as e:result={'host':type(e).__name__,'message':str(e)}
    return {'outcome':result,'hooks':list(calls)}
class Meta(type):
    def __getattribute__(cls,name):
        if name=='__mro__':calls.append('metaclass.__getattribute__');raise RuntimeError('MRO hook')
        return type.__getattribute__(cls,name)
class Real(int,metaclass=Meta):pass
class FakeMeta(type):
    @property
    def __mro__(cls):calls.append('MRO descriptor');return (int,object)
class Fake(metaclass=FakeMeta):pass
class TextProperty(m.JsonText):
    @property
    def text(self):calls.append('text property');raise RuntimeError('text hook')
    @text.setter
    def text(self,value):object.__getattribute__(self,'__dict__')['text']=value
class DictProperty(m.JsonText):
    @property
    def __dict__(self):calls.append('dict property');raise RuntimeError('dict hook')
results={
 'M01':obs(lambda:m.validate_value(Real(1))),
 'M02':obs(lambda:m.validate_value(Fake())),
 'D01':obs(lambda:m.validate_arguments({'value':TextProperty('1')})),
 'D02':obs(lambda:m.validate_arguments({'value':DictProperty('1')})),
 'dict-map':obs(lambda:m.validate_arguments({'a':1,'b':2})),
 'UserDict-map':obs(lambda:m.validate_arguments(collections.UserDict({'a':1,'b':2}))),
 'bytearray-text':obs(lambda:m.decode_json(bytearray(b'1'))),
}
# Instrument a genuine Mapping that is not a dict; its data are stored by the caller.
class Map(collections.abc.Mapping):
    def __init__(self):self.data={'a':1}
    def __iter__(self):calls.append('map iter');return iter(self.data)
    def __len__(self):calls.append('map len');return len(self.data)
    def __getitem__(self,k):calls.append('map getitem');return self.data[k]
results['custom-map']=obs(lambda:m.validate_arguments(Map()))
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'.tmp/work/codex/ce01-checkpoint2-matrix'/sys.platform
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'controls.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
```
