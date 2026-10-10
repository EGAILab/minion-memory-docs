# WP-01 CE-01-01 checkpoint review — Codex

**Verdict: CHANGES_REQUIRED**

Reviewed classification: `assurance/convergence/CE-01-01-classification.md` at
`d46dfa1ca378d1e2c97ea0137053f8b86f5afc9b` (not a later mutable head).
Handoff/state base: `4c2ec74ffb07f105cdb0aea181b88f9930a09d23`.
Frozen implementation: `eb47635c6ea997f030d04b8099366044a2f702aa`.
Review branch: `review/wp01-ce1-checkpoint`; only this record is added.

This checkpoint is not AGREED FOR IMPLEMENTATION. Production remains frozen for Codex. No
production files, shared contract, authoring worktrees, registers, remotes or main branches were
changed. Findings below concern this proposed checkpoint, not reopening unrelated WP-01 findings.

## Findings

### CE01-CP-001 — Prescribed real-MRO lookup dispatches and can be spoofed

- Classification: `CONTRACT_ASSURANCE_DEFECT`; severity: high; path A.
- `owner_decision_required: false`; blocking: CE-01-01 checkpoint; status: OPEN.
- Evidence: classification §2 vs §4.1, especially line 63 at the reviewed SHA; G-037/G-041 and
  SER-008 Native subclasses / Native binding completion.

§2 correctly proposes `issubclass(type(x), built_in_base)` to reject __class__ spoofs. §4.1 instead
requires classification by `type(x).__mro__`. These are not equivalent. An admitted int subclass can
have a metaclass whose __getattribute__ raises on __mro__: the prescribed lookup invokes the hook
and raises RuntimeError, while `issubclass(type(x), int)` returns True with no hook and base
extraction returns exact 1. Conversely, a non-int class with a metaclass __mro__ property returning
`(int, object)` makes `int in type(x).__mro__` True, with a user hook. Even
`type.__getattribute__(type(x), "__mro__")` invokes that property. The genuine built-in subtype
check returns False without a hook.

Executed controls M01/M02 below demonstrate both the unreasonable refusal of a genuine admitted
subclass and the false admission of a non-subclass. Checking that the *built-in base* metaclass is
not overridable does not address attribute dispatch through the *input type's* metaclass.

Required checkpoint correction: require genuine built-in ancestry without invoking user metaclass
attributes/descriptors, reconcile §2 and §4.1, and add both controls with the ordinary admitted and
unsupported-type/no-hook oracles. Do not substitute rejection of all custom-metaclass subclasses.
This is an authority reading of the existing admission/no-hook rule, not an Owner choice or code patch.

### CE01-CP-002 — Stored JsonText descriptors are an uncovered dispatch neighborhood

- Classification: `CONTRACT_ASSURANCE_DEFECT`; severity: high; path A.
- `owner_decision_required: false`; blocking: CE-01-01 checkpoint; status: OPEN.
- Evidence: classification §2 completeness claim and §4.3, B066, G-041, SER-008 completion;
  frozen `core/values.py:384`.

The classification says descriptor/attribute hooks are covered by instrumented __getattribute__
rows. They are not. A genuine JsonText subclass can store `text="1"` in its instance storage while
defining a text property whose getter raises. The frozen public call invokes this property and leaks
RuntimeError. B066 exercises an overridden __getattribute__, so an implementation that changes it
to `object.__getattribute__(wrapper, "text")` passes that existing neighborhood but still invokes
the text property. The new executed D01 control demonstrates exactly this distinction: ordinary
and object-base attribute reads both call the descriptor; the stored text remains "1".

G-041 already decides the oracle: validate_arguments on this wrapper must return `{value: 1}` with
no user hook. This is not permission to treat the wrapper as unsupported or to use a property result
as its stored text. Add an independently executed descriptor control and constrain reads to genuine
stored framework state, including bypass of subclass descriptors. Preserve the existing overridden
__getattribute__ controls. No new observable semantic choice is needed.

### CE01-CP-003 — Decision-adjusted row oracles and negative-control accounting are inconsistent

- Classification: `CONTRACT_ASSURANCE_DEFECT`; severity: high; path A.
- `owner_decision_required: false`; blocking: CE-01-01 checkpoint; status: OPEN.
- Evidence: classification §§5–6 and rows N01323, N01821, N03201, B003/B004/B032, B070–B075;
  G-042 and the unchanged characterization's observation method.

Three concrete problems:

1. **False pass under G-042.** N01821 (`int/added-attributes`, validate_value) and N03201
   (`float/added-attributes`, validate_value) are KEEP with only “required cell, zero user hooks.”
   The original required cells compare portable values after stripping runtime type/state for
   observation; they deliberately deferred exact return representation to C05. Frozen native scalar
   subclasses are still returned unchanged, including added state. Executed R01 returns the original
   subclass and retains extra=99 while satisfying that old value/no-hook oracle. G-042 now requires
   exact normalized built-ins. The new oracle must check exact types recursively on returned native
   portable values, and dispositions must be recomputed under it. A separate B070/B071 assertion
   cannot make the other rows' written oracles correct. Preserve tuple→list normalization; do not
   demand a tuple return just because a fixture's original base family was tuple.
2. **Already-correct boundary rows marked FIX.** B003/B004/B032 already produce their decided
   results with no hooks. B072/B073/B074/B075 already return exact str/list/list/dict respectively
   with no added state. They are all FIX. B074's original `exact_base_type:false` is expected because
   a tuple normalizes to a list, not evidence of a G-042 defect. These rows should be regression
   controls if they satisfy the decision-adjusted oracle; if FIX means contract work rather than
   executable failure, distinguish that disposition and its evidence explicitly. Do not count them
   as killed frozen witnesses.
3. **Impossible blanket negative-control obligation.** §5 requires every raising-hook class to
   fail on frozen code. N01323, an int with __iter__ that raises, canonicalizes to bytes hex 31 with
   no hook on frozen code. Executed K01 reproduces this. The hook is correctly uncalled. The old
   matrix has 14,955 raising-hook operation rows that already pass its old oracle; that number is
   not a recalculated G-042 closure count. Require before/after kills only for actual failing
   controls, and preserve already-passing controls. Deliberately making a correct frozen control
   fail or rejecting admitted subclasses would contradict the checkpoint.

Required correction: state full literal oracles for the now-decided boundary rows (outcome/code,
stage/argument where relevant, zero hooks, exact normalized types where applicable), recompute
dispositions/counts against those oracles, and separate kill witnesses from KEEP controls. Carry
the updated return-type assertion into all applicable normative rows rather than treating the
pre-decision observer's portable-value equality as the entire G-042 test.

## Decisions, challenge results and reviewed scope

G-039's duplicate code/native stage, G-040's active-path cycle rejection with legal shared aliases,
G-041's base-protocol extension and G-042's exact normalized outputs are recorded verbatim. Their
principal completion bullets are faithful. CH01–CH05's oracle is a sound authority reading: an
object merely spoofing __class__ is not an admitted built-in subclass. Reject it at native stage 1
as value.unsupported_type without any hook.

The transcription should also remove the obsolete SER-008 sentence “Representation defects such
as duplicate keys exist only there” and scope the source-text ordering sentence to JSON text,
explicitly carrying G-039's earlier-native-unsupported-kind precedence. Native duplicates now exist
by Owner decision; the old sentence cannot remain an unqualified description. This is a direct
authority correction, not a requested new Owner decision. The review does not invent an alternative
cycle/duplicate policy or select new error codes.

I independently re-executed CH01–CH05 against the frozen public validate_value API. CH01/CH02/CH04
leak TypeError; CH03 returns "a" and CH05 returns {"a":1}, both with hooks. All five invoke the spoofed
__class__ property. Genuine ancestry tests reject all five with no hooks. The additional metaclass,
descriptor, return-state and uncalled-hook controls were also executed. Windows and WSL Ubuntu,
both project-local managed CPython 3.12.8, produce identical full JSON observations, including ordered
hook logs. Scratch/cache/child paths remain in the project; damaged system Python was not used.

Mechanical checks: all 25,554 classification IDs are unique and exactly cover 25,470 normative,
75 boundary, 4 construction and 5 challenge rows. Current table counts are 3,625 FIX / 21,925 KEEP /
4 N/A. Every normative disposition mechanically matches the **old** characterization OK/WRONG
flag; this confirms accounting, not fidelity to the newly decided G-042 oracle. The characterization
is unchanged: blob 4a00bd7ddeff3f23b0e053f7dd5728c76dcbd24f at both 2cf2b21b and d46dfa1c.

No production suite was run: this is the frozen checkpoint's proposed semantics/controls review,
not implementation closure. The executable evidence below is sufficient to reject the checkpoint
as written. Please revise the checkpoint and controls before the single implementation pass.

## Executed observations

The following complete observations match on both hosts. Outcome inspection happens after hook
capture stops; no production imports are patched. Byte outputs are recorded in hex.

```json
{
  "CH01": {
    "outcome": {
      "host": "TypeError",
      "message": "'<=' not supported between instances of 'int' and 'Spoof'"
    },
    "hooks": [
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__"
    ]
  },
  "CH01-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "CH02": {
    "outcome": {
      "host": "TypeError",
      "message": "must be real number, not Spoof"
    },
    "hooks": [
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__"
    ]
  },
  "CH02-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "CH03": {
    "outcome": {
      "value": "a"
    },
    "hooks": [
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__iter__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__str__"
    ]
  },
  "CH03-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "CH04": {
    "outcome": {
      "host": "TypeError",
      "message": "'Spoof' object is not reversible"
    },
    "hooks": [
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__"
    ]
  },
  "CH04-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "CH05": {
    "outcome": {
      "value": {
        "a": 1
      }
    },
    "hooks": [
      "__class__",
      "__iter__",
      "__class__",
      "__class__",
      "__class__",
      "__iter__",
      "items",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "items",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "__class__",
      "items"
    ]
  },
  "CH05-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "M01-prescribed-kind": {
    "outcome": {
      "host": "RuntimeError",
      "message": "metaclass MRO hook"
    },
    "hooks": [
      "metaclass.__getattribute__(__mro__)"
    ]
  },
  "M01-safe-kind": {
    "outcome": {
      "value": true
    },
    "hooks": []
  },
  "M01-base-extraction": {
    "outcome": {
      "value": 1
    },
    "hooks": []
  },
  "M02-prescribed-kind": {
    "outcome": {
      "value": true
    },
    "hooks": [
      "metaclass.__mro__ descriptor"
    ]
  },
  "M02-type-getattribute": {
    "outcome": {
      "value": true
    },
    "hooks": [
      "metaclass.__mro__ descriptor"
    ]
  },
  "M02-safe-kind": {
    "outcome": {
      "value": false
    },
    "hooks": []
  },
  "D01-frozen-JsonText": {
    "outcome": {
      "host": "RuntimeError",
      "message": "text descriptor hook"
    },
    "hooks": [
      "text descriptor"
    ]
  },
  "D01-object-getattribute": {
    "outcome": {
      "host": "RuntimeError",
      "message": "text descriptor hook"
    },
    "hooks": [
      "text descriptor"
    ]
  },
  "D01-storage": {
    "outcome": {
      "value": "1"
    },
    "hooks": []
  },
  "K01-uncalled-raising-hook": {
    "outcome": {
      "bytes_hex": "31"
    },
    "hooks": []
  },
  "R01-returned-subtype": {
    "same_object": true,
    "exact_int": false,
    "added_state": {
      "extra": 99
    }
  },
  "S01-stages-across-arguments": {
    "outcome": {
      "code": "value.unsupported_type"
    },
    "hooks": []
  }
}
```

## Reproduction driver

Extract below to `.tmp/work/codex/ce01-checkpoint-probes.py`. In every shell first dot-source the
project environment, use a project-local managed CPython 3.12.8, and set PYTHONPATH to frozen
checkout `review-worktrees/code-wp01-python-candidate-2/minion-memory-python/src`. Run the script.
It writes only project-local scratch observations. Its small kind/storage experiments demonstrate
dispatch mechanics and proposed oracles, not production changes.

```python
import json,pathlib,sys,collections
from minion_memory import core as m
ROOT=pathlib.Path(__file__).resolve().parents[3]
calls=[]
def observe(fn):
    calls.clear()
    try:
        out=fn();result={'bytes_hex':out.hex()} if type(out) is bytes else {'value':out}
    except m.MnemeValidationError as e: result={'code':e.code}
    except Exception as e: result={'host':type(e).__name__,'message':str(e)}
    return {'outcome':result,'hooks':list(calls)}

def spoof(kind,payload):
    class Spoof:
        @property
        def __class__(self): calls.append('__class__');return kind
        def __repr__(self):calls.append('__repr__');return repr(payload)
        def __str__(self):calls.append('__str__');return str(payload)
        def __iter__(self):calls.append('__iter__');return iter(payload)
        def items(self):calls.append('items');return payload.items()
    return Spoof()
results={}
for i,(kind,payload) in enumerate(((int,1),(float,1.5),(str,'a'),(list,[1]),(dict,{'a':1})),1):
    obj=spoof(kind,payload)
    results[f'CH{i:02}']=observe(lambda:m.validate_value(obj))
    results[f'CH{i:02}-safe-kind']=observe(lambda:issubclass(type(obj),kind))

class Meta(type):
    def __getattribute__(cls,name):
        if name=='__mro__':calls.append('metaclass.__getattribute__(__mro__)');raise RuntimeError('metaclass MRO hook')
        return type.__getattribute__(cls,name)
class RealInt(int,metaclass=Meta):pass
x=RealInt(1)
results['M01-prescribed-kind']=observe(lambda:type(x).__mro__)
results['M01-safe-kind']=observe(lambda:issubclass(type(x),int))
results['M01-base-extraction']=observe(lambda:int.__int__(x))

class FalseMRO(type):
    @property
    def __mro__(cls):calls.append('metaclass.__mro__ descriptor');return (int,object)
class NotInt(metaclass=FalseMRO):pass
x=NotInt()
results['M02-prescribed-kind']=observe(lambda:int in type(x).__mro__)
results['M02-type-getattribute']=observe(lambda:int in type.__getattribute__(type(x),'__mro__'))
results['M02-safe-kind']=observe(lambda:issubclass(type(x),int))

class TextDescriptor(m.JsonText):
    @property
    def text(self):calls.append('text descriptor');raise RuntimeError('text descriptor hook')
    @text.setter
    def text(self,v):object.__getattribute__(self,'__dict__')['text']=v
text=TextDescriptor('1')
results['D01-frozen-JsonText']=observe(lambda:m.validate_arguments({'value':text}))
results['D01-object-getattribute']=observe(lambda:object.__getattribute__(text,'text'))
results['D01-storage']=observe(lambda:object.__getattribute__(text,'__dict__')['text'])

# Concrete KEEP/kill-accounting witnesses already present in the input matrix.
class Uncalled(int):
    def __iter__(self):calls.append('__iter__');raise RuntimeError('unused hook')
results['K01-uncalled-raising-hook']=observe(lambda:m.canonical_bytes(Uncalled(1)))
class Retained(int):pass
x=Retained(1);x.extra=99
out=m.validate_value(x)
results['R01-returned-subtype']={'same_object':out is x,'exact_int':type(out) is int,'added_state':object.__getattribute__(out,'__dict__')}

# Stage 1 must finish across arguments before stage 2 numeric normalization.
results['S01-stages-across-arguments']=observe(lambda:m.compare_versions(float('inf'),object()))
OUT=ROOT/'.tmp/work/codex/ce01-checkpoint'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/(sys.platform+'-probes.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
```
