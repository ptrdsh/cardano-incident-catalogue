# Incident Report Template

Copy this file to `CID-yyyyxx/README.md` (see [README.md](README.md) for numbering) and fill in the fields required for the chosen `completeness` level ([CLASSIFICATION.md](CLASSIFICATION.md), section 11). Field values are defined in the same document. Use `null` for unknown values rather than guessing, and explain the gap in the report. Every list field also accepts `other`; explain it in `classification_notes`.

Figures go into the incident directory under `figures/`. Prefer images already published in the sources (charts, screenshots, diagrams); embed each with an italic caption that credits the author with a link and the source number, e.g. `![Node upgrades during the partition](figures/node-upgrades.png)` and `*Figure 1: ... Source: Intersect, "Incident report ..." [2].*` Only where no source image covers something relevant, add your own chart from verifiable data; the caption names the data source and says "chart by the catalogue". Mechanisms can also be drawn inline as Mermaid diagrams.

```markdown
---
schema_version: "1.0"
completeness: full                   # stub | standard | full
id: CID-yyyyxx
title: Short descriptive title
date_start: YYYY-MM-DDTHH:MMZ        # UTC; date only (YYYY-MM-DD) if time unknown; null if never established
date_end: YYYY-MM-DDTHH:MMZ          # when impact ended; null if ongoing
date_disclosed: YYYY-MM-DD           # first public acknowledgement by the responsible party
duration: "~14h"                     # human readable impact window
layer: protocol                      # protocol | network | infrastructure | tooling | wallet | dapp | organisational | other
class: exploit                       # exploit | near-miss | outage | malfunction | governance-dispute | misleading-information | shutdown | other
trigger: malicious                   # malicious | accidental | bug | design-flaw | decision | disputed | unknown | other
severity: SEV-1                      # actual impact, SEV-1 (critical) .. SEV-5 (informational)
potential_severity: SEV-1            # worst credible impact if unmitigated
status: resolved                     # resolved | contained | unresolved | ongoing | other
recoverability: routine              # routine | extra-resources | escalated | not-recoverable | other (NIST SP 800-61r2 categories)
l1_at_fault: false                   # true if the root cause is in the Cardano protocol or node software
affected:
  projects: []                       # e.g. [cardano-node, Minswap]
  components: []                     # e.g. [ledger CBOR decoder, LP minting policy]
  versions: []                       # affected software versions, if applicable
impact:
  consensus_safety: false            # Cardano L1: did honest nodes diverge?
  liveness: none                     # Cardano L1: none | degraded | halted; describe dApp/service availability in the report
  funds_lost_usd: null               # gross, at time of incident
  funds_lost_native: null            # e.g. "2,434,648 ADA"
  funds_recovered: null              # free text
  users_made_whole: null             # true | false | partial | null
  users_affected: null               # free text, e.g. "374 addresses"
disclosure: full-post-mortem         # full-post-mortem | partial-post-mortem | statement-only | third-party-report | none | other
responders: []                       # organisations that handled the incident
root_cause_tags: []                  # short free-form tags, e.g. [deserialisation, input-validation]
related: []                          # catalogue IDs with shared root cause, same project or causal link, e.g. [CID-202406]
classification_notes: null           # free text: judgement calls and any use of `other`
references:                          # the most authoritative 1-3 sources (also listed under Sources)
  - https://...
last_updated: YYYY-MM-DD
---

# CID-yyyyxx: Title

> One-paragraph executive summary: what happened, impact, whether funds were lost,
> whether the Cardano L1 was at fault, and how it ended. Written for a non-technical
> decision maker.

## Timeline (UTC)

| Time | Event |
|---|---|
| YYYY-MM-DD HH:MM | ... [1] |

## Impact

What was affected, for how long, how much value, which users. Quantified where sources allow.

End with the rating justification: "Rated SEV-x (dimension: ...); potential SEV-y (dimension: ...). Recoverability: <value> (...)."

## Root cause

Technical or organisational explanation, as precise as the sources allow.

## Detection

How and by whom the incident was detected; time to detection if known.

## Response and resolution

Who did what to contain and resolve the incident.

## Remediation and follow-up

What changed afterwards (code fixes, process changes, audits, compensation) so that the incident does not repeat.

## Incident handling assessment

Assessment of the responsible party's handling against SOC 2 Trust Services Criteria, based on public sources only (see CLASSIFICATION.md, section 10).

| Criterion | Result | Observation |
|---|---|---|
| CC7.2 Monitoring and detection | No exceptions noted / Exceptions noted / Not evidenced / Not applicable | ... [n] |
| CC7.3 Evaluation of events | ... | ... |
| CC7.4 Incident response | ... | ... |
| CC7.5 Recovery | ... | ... |
| CC2.3 External communication | ... | ... |
| CC8.1 Change management | ... | ... |

## Lessons for builders

Concrete, transferable takeaways for teams building on Cardano.

## Disputed or open points

Conflicting accounts, missing data, unanswered questions. Omit the section if there are none.

## Sources

1. [P] Publisher, "Title", YYYY-MM-DD. URL
2. [S] Publisher, "Title", YYYY-MM-DD. URL
```
