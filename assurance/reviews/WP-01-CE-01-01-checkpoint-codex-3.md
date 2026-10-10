# WP-01 CE-01-01 checkpoint revision 3 — Codex targeted re-review

**Verdict: APPROVED**

Approved exact artifact: `assurance/convergence/CE-01-01-classification.md` at
`8e8d30a824dee743782db6b5a5179515bcd36819`.
Handoff/state base: `38f126cb0631d39e934ea33da87cde073a365a2e`.
Frozen executable reference: `eb47635c6ea997f030d04b8099366044a2f702aa`.
Review branch: `review/wp01-ce1-checkpoint-3`; only this record is added.

This makes the exact revision-3 checkpoint **AGREED FOR IMPLEMENTATION**. It does not approve an
implementation, close WP01-CR-007/008, accept a candidate onto main, or authorize Codex production
edits. The agreed single implementation pass belongs to Claude; targeted implementation closure
still follows. No production modules, shared contract, authoring worktrees, registers or remotes
were modified by this review.

## CE01-CP-004 disposition

**RESOLVED by Owner G-043.** The prior path-C issue is now decided, not selected by an agent.
The verbatim source at the reviewed SHA requires a documented dict/dict-subclass public precondition;
anything else raises TypeError immediately, before any argument inspection, with no hooks, outside
the Mneme value-error vocabulary.

SER-008 “Argument maps” and classification §0/§3/§4.3 preserve that policy. Read the public
precondition as covering every non-dict input, as G-043 says “anything else”; it is not permission
to inspect a non-Mapping object before refusal. The earlier no-hook/base-dict rule remains intact.
No new error-code choice or exception-message promise is introduced.

CM01 and CM02 have the correct literal oracles: caller TypeError before any supplied argument is
inspected, with zero user hooks. Their FIX dispositions are justified by independent executions:

| Control | Frozen public validate_arguments result | Required by G-043 |
|---|---|---|
| CM01: UserDict containing a=1, b=2 | Returns {a:1,b:2}; no instrumented hook | TypeError immediately; zero hooks |
| CM02: custom Mapping containing a=1 | Returns {a:1}; invokes len, iter and getitem | TypeError immediately; zero hooks |

I also executed poison-value companions: the same rejected call-frame types containing a value
whose __class__ property raises. Frozen code inspects the argument and leaks RuntimeError;
G-043 requires the same immediate TypeError with no hook. These companions substantiate the
already-agreed “before any argument” requirement; they introduce no new semantics or finding and
do not alter the approved checkpoint row set.

CE01-CP-001–003 retain the resolved checkpoint dispositions from revision 2. No new blocker found.

## Scope and unchanged-content verification

Compared exact docs commits `3d4e83398a4cd0cc3f96b61d0967b9b1cdf63853` and
`8e8d30a824dee743782db6b5a5179515bcd36819`:

- All **25,558** previous classification row entries are byte-for-byte equal at the line-content
  level, including disposition, finding/decision, oracle and evidence columns. The only new IDs
  are CM01 and CM02, both FIX.
- The original characterization is unchanged. The independent G-042 re-derivation from revision 2
  remains applicable; no need to repeat the unchanged full matrix.
- Classification prose changes only the revision/response text, G-043 argument-map policy and
  corresponding counts. SER-008 adds only the argument-map bullet; governance adds only G-043.
  Prior semantic rules and implementation constraints otherwise remain unchanged.
- The other docs-tree changes are the landed revision-2 review and its handoff/state coordination
  records. Thus “nothing else changed” holds for checkpoint semantics, not a claim that the whole
  docs tree has no metadata or review additions.
- State head `38f126cb` differs from the reviewed artifact commit only by the new handoff and state
  record. The review is pinned to the artifact SHA above.

Revised accounting is correct: **25,560 unique IDs; 4,116 FIX / 21,440 KEEP / 4 N/A.** CM01/CM02
are the only additions to the previous counts. Kill witnesses remain separate from regressions.

Both Windows and WSL Ubuntu used project-local managed CPython 3.12.8 against the clean frozen
checkout. Complete observations, including ordered hook logs, match across hosts. Every shell
first sourced the project environment. Scratch/cache/output paths stayed inside the project;
the damaged system Python was not used. No implementation suite was run: this is the narrowly
scoped checkpoint review, not implementation closure.

## Executed observations

```json
{
  "controls": {
    "CM01": {
      "current": {
        "value": {
          "a": 1,
          "b": 2
        }
      },
      "hooks": [],
      "required": {
        "host": "TypeError",
        "hooks": [],
        "before_argument_inspection": true
      }
    },
    "CM02": {
      "current": {
        "value": {
          "a": 1
        }
      },
      "hooks": [
        "mapping.__len__",
        "mapping.__iter__",
        "mapping.__getitem__"
      ],
      "required": {
        "host": "TypeError",
        "hooks": [],
        "before_argument_inspection": true
      }
    },
    "CM01-poison": {
      "current": {
        "host": "RuntimeError",
        "message": "argument inspected"
      },
      "hooks": [
        "argument.__class__"
      ],
      "required": {
        "host": "TypeError",
        "hooks": [],
        "before_argument_inspection": true
      }
    },
    "CM02-poison": {
      "current": {
        "host": "RuntimeError",
        "message": "argument inspected"
      },
      "hooks": [
        "mapping.__len__",
        "mapping.__iter__",
        "mapping.__getitem__",
        "argument.__class__"
      ],
      "required": {
        "host": "TypeError",
        "hooks": [],
        "before_argument_inspection": true
      }
    }
  },
  "rows_unchanged": 25558,
  "new_rows": [
    "CM01",
    "CM02"
  ],
  "counts": {
    "KEEP": 21440,
    "FIX": 4116,
    "N/A": 4
  },
  "characterization_unchanged": true
}
```

## Independent reproduction driver

Save under `.tmp/work/codex/ce01-checkpoint3.py`, source the project environment, use project-local
managed Python 3.12.8, and set PYTHONPATH to the frozen checkout's minion-memory-python/src.
The driver reads pinned docs objects and writes only project-local scratch evidence.

```python
import collections,collections.abc,json,pathlib,re,subprocess,sys
from minion_memory import core as m
ROOT=pathlib.Path(__file__).resolve().parents[3]
calls=[]
class CallMap(collections.abc.Mapping):
    def __init__(self,value=1):self.data={'a':value}
    def __len__(self):calls.append('mapping.__len__');return len(self.data)
    def __iter__(self):calls.append('mapping.__iter__');return iter(self.data)
    def __getitem__(self,k):calls.append('mapping.__getitem__');return self.data[k]
class Poison:
    @property
    def __class__(self):calls.append('argument.__class__');raise RuntimeError('argument inspected')
def run(value):
    calls.clear()
    try:out={'value':m.validate_arguments(value)}
    except m.MnemeValidationError as e:out={'code':e.code}
    except Exception as e:out={'host':type(e).__name__,'message':str(e)}
    return {'current':out,'hooks':list(calls),'required':{'host':'TypeError','hooks':[],'before_argument_inspection':True}}
results={'CM01':run(collections.UserDict({'a':1,'b':2})),'CM02':run(CallMap()),
         'CM01-poison':run(collections.UserDict({'a':Poison()})),
         'CM02-poison':run(CallMap(Poison()))}
DOC=ROOT/'review-worktrees/docs-wp01-ce1-checkpoint-3'
def gittext(commit,path):return subprocess.check_output(['git','--git-dir',str(ROOT/'minion-memory-docs/.git'),'show',commit+':'+path]).decode('utf-8')
def table(text):
    pairs={}
    for line in text.splitlines():
        if re.match(r'^\| (N\d+|B\d+|F\d+|CH\d+|M\d+|D\d+|CM\d+) \|',line):
            f=[v.strip() for v in line.split('|')[1:-1]]
            assert f[0] not in pairs
            pairs[f[0]]=f[1:]
    return pairs
artifact='assurance/convergence/CE-01-01-classification.md'
old=table(gittext('3d4e8339',artifact));new=table(gittext('8e8d30a8',artifact))
assert all(new[k]==v for k,v in old.items())
assert set(new)-set(old)=={'CM01','CM02'}
assert new['CM01'][0]==new['CM02'][0]=='FIX'
counts=collections.Counter(v[0] for v in new.values())
assert dict(counts)=={'KEEP':21440,'FIX':4116,'N/A':4}
characterization='assurance/convergence/CE-01-01-characterization.md'
assert gittext('3d4e8339',characterization)==gittext('8e8d30a8',characterization)
OUT=ROOT/'.tmp/work/codex/ce01-checkpoint3'/sys.platform
OUT.mkdir(parents=True,exist_ok=True)
data={'controls':results,'rows_unchanged':len(old),'new_rows':['CM01','CM02'],'counts':dict(counts),'characterization_unchanged':True}
(OUT/'evidence.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2))
```
