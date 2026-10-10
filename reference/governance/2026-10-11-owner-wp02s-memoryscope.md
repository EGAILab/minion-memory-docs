# Owner decisions — WP-02S MemoryScope (2026-10-11)

Recorded verbatim by Claude. These are the Owner's answers to the consolidated packet
`assurance/layers/02s-owner-decision-packet.md` (D1–D8, NF-018). Each answer is the selected option
with the Owner's own text.

## G-056 — D1 — MemoryScope value and equality

> **Q:** WP-02S D1 — What is a MemoryScope value, and when are two equal? (Sources fix: typed, structured, extensible, faceted, namespaced per profile.)
>
> **A:** "Choose 1 — an immutable single-valued facet map.A resolved MemoryScope is a JSON object mapping canonical namespaced facet names to one canonical portable-token value each. Facet names use the <profile>.<facet> form, but Core infers no hierarchy from the dotted spelling. Equality is exact map equality: member order is irrelevant, while absent and present facets are distinct.The empty resolved map denotes explicitly global scope; unknown scope is represented separately as unresolved and is hidden from ordinary reads. Scope is part of a record’s immutable canonical content. Changing it requires a new artifact revision or an explicit append-only superseding interpretation with lineage.Multi-valued facets and separately identified Scope artifacts are not part of the initial Core contract."

## G-057 — D2 — No hierarchy in Core

> **Q:** WP-02S D2 — Is there a hierarchy between facets (e.g. principal ⊃ workspace ⊃ conversation ⊃ session ⊃ task)? Sources call them 'dimensions' and list them flat.
>
> **A:** "Choose 1 — facets are flat and independent in Core.Core infers no parent, containment, inheritance, or widening relationship between facets or their values. Namespaced dotted facet names are lexical identifiers only. Records and queries must state every constraint they rely on explicitly.A profile may later introduce an explicit, versioned widening policy that expands source context into an effective query scope before invoking Core matching. Such a policy does not alter stored scopes or create implicit Core hierarchy."

## G-058 — D3 — Applicability matching, fail-closed

> **Q:** WP-02S D3 — Visibility: when does a record's scope match a query's allowed scope? (Sources: query carries 'allowed scope'; record carries facets 'applicable' to it.)
>
> **A:** "Choose 1 — applicability matching with fail-closed query omission.For resolved scopes, a record is visible exactly when every facet declared by the record is explicitly present with the same value in the query’s allowed scope. Record-omitted facets are unconstrained; query-omitted facets never widen visibility. Extra query facets are allowed and do not prevent broader records from applying.An explicitly empty resolved record scope is global; an empty query sees only global records. Unresolved records remain hidden. Non-matching records are excluded, and public ID lookup treats them as not_found."

## G-059 — D4 — Out-of-scope outcome

> **Q:** WP-02S D4 — What happens to out-of-scope records? (Sources: they 'cannot be returned' by similarity; private records may be omitted.)
>
> **A:** "Choose 1 — silently filter out-of-scope records and make scoped ID lookup indistinguishable from absence.Ordinary search, retrieval, ranking, projection, counts, and diagnostics operate as though out-of-scope records are not present. A scoped lookup of an existing but inaccessible record returns the same not_found result as a nonexistent ID and must not expose a separate denial or existence signal.Privileged audit tooling may diagnose scope exclusion through a separate authorized interface. Public responses expose no hidden-record count; internal telemetry may record only bounded, content-free aggregates under the privacy policy.Cross-scope consolidation remains deferred to Layer 14. Until that contract exists, implementations must not combine records in a way that silently widens visibility."

## G-060 — D5 — Scope at capture

> **Q:** WP-02S D5 — Scope at capture: what scope does a newly captured record get? (Sources: scope is attached at the durability barrier; capture-first durability must not lose the source.)
>
> **A:** "Choose 1 — capture with the most restrictive complete scope that can be positively established; otherwise preserve the source under explicit unresolved scope.A resolved capture includes every applicable facet known to the adapter. A facet may be omitted only when the adapter can affirm that the record is intentionally unconstrained by that facet. Missing, ambiguous, or incomplete contextual knowledge results in scope_state = unresolved, not a partially widened scope and never an empty/global scope.Unresolved captures are committed durably at the capture barrier but remain hidden from ordinary reads until an explicit resolution creates a new revision or superseding interpretation with lineage. Scope is never silently defaulted to principal/agent or global."

## G-061 — D6 — Unknown facets; canonical Agent facet registry

> **Q:** WP-02S D6 — Unknown facets and the paired names in the sources (principal/user, workspace/project, course/domain, collection/curriculum).
>
> **A:** "Choose 1 — fail closed with one canonical name per semantic facet.For the Agent MVP, the canonical facet registry is agent.principal, agent.agent, agent.workspace, agent.conversation, agent.session, and agent.task. Source terms user and project are mapped by the integration adapter to principal and workspace; aliases never enter Core.A stored record containing any facet unknown to the reader is excluded from ordinary reads without dropping that constraint. A query containing an unknown facet is rejected as scope.query_invalid. Current capture APIs reject unknown facets, while imported/future records may be preserved but remain fail-closed until a reviewed vocabulary understands them.The Learning Profile’s facet vocabulary remains deferred. course/domain and collection/curriculum must not yet be declared aliases or distinct facets without the Learning-layer decision. Any future facet addition, rename, alias change, or split is a versioned vocabulary change."

## G-062 — D7 — Learning Profile adoption deferred

> **Q:** WP-02S D7 — Does the Learning Profile have to enforce MemoryScope now? (Sources: 'Shared MemoryScope may be used by the Learning Profile'; no learning scope test exists.)
>
> **A:** "Choose 1 — defer Learning Profile adoption of MemoryScope to Layers 07–12.Core defines reusable scope semantics, and the Agent Profile adopts them now. Current Learning Profile schemas and Flashcard MVP operations do not participate in scope semantics: they carry neither a resolved empty/global scope nor an unresolved scope, and learning retrieval does not invoke the Core scope matcher.Future Learning adoption requires an explicit, versioned profile contract covering facet vocabulary, capture, visibility, legacy records, migration and tests. Existing learning records must not be retroactively interpreted as globally scoped or unresolved. Multi-learner or shared-store isolation is a trigger that must resolve this deferral before such functionality ships."

## G-063 — D8 — Agent isolation conformance covers six dimensions

> **Q:** WP-02S D8 — Agent scope-isolation conformance: sources list six dimensions, but the R04 §42 test names four (principal/agent/project/conversation). Which set must the isolation scenarios cover?
>
> **A:** "Choose 1 — isolation conformance covers all six Agent Profile dimensions: principal, agent, workspace, conversation, session, and task.R04 §42’s principal/agent/project/conversation list is a required subset, not an exhaustive cap; project maps to the canonical workspace facet. Each dimension requires match, mismatch, record-omission and query-omission evidence, plus composed cases proving that a mismatch in any one declared facet excludes the record.An exhaustive \(2^6\) cross-product is unnecessary, but session and task isolation cannot remain untested because both are normative visibility constraints."
