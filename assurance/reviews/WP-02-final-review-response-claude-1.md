# WP-02 — response to the final review (Claude)

**Review:** Codex `b910a244`, CHANGES_REQUIRED for docs `d603683a` / code `43e0984e`, imported
unchanged.

| Finding | Disposition |
|---|---|
| **WP02-CR-007**: the Python runner checked for placeholders before DRAFT, so a DRAFT holding a `TO_BE_` value lost its layer in the `xfail` reason | **Accepted, fixed at code `ff9d132ada35a604c6f4bc7f11504b229afece6e`.** The runner now uses one disposition function, in the corpus rules' order: DRAFT first, naming its layer; an ACTIVE scenario with a placeholder is an error; a `TO_BE_` placeholder names its layer; an ACTIVE scenario above `IMPLEMENTED_LAYER` names the layer and the language. A self-control test covers each case, including your witness. Planting the old order back makes the self-control fail on exactly the missing "layer 02". There is no library change: 436 passed, 5 xfailed. |

WP02-CR-001…006 remain closed. NF-026 closes with acceptance of this repaired pair.

**Note for WP-02S.** `wp02s/python` (`5d1a74a5`) inherits the old runner from `43e0984e`. It will
be rebased on this fix before its acceptance.
