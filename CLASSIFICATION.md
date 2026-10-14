# Incident Classification Standard

Every incident in this catalogue carries a machine-readable header (YAML front matter) and is classified with the scheme below. The goal is that a reader doing due diligence can compare incidents across years, layers and projects without reading every report, and that tools (including AI assistants) can filter the catalogue reliably.

Header fields are specified in [TEMPLATE.md](TEMPLATE.md). This document defines what the values mean.

**Standard version: 1.0.** Each report records the version it follows in `schema_version`. Changes are listed in the [Changelog](#changelog). Section 11 sets out which fields are required, and section 12 covers incidents that do not fit a predefined value.

## 0. Basis and relation to established frameworks

This scheme is not a regulatory classification and the reports are not audits. Every rating is derived from public sources only. The scheme borrows its structure from established frameworks so that readers used to them can map it quickly:

| Element | Inspired by | How it is used here |
|---|---|---|
| Severity (section 1) | EU DORA, Commission Delegated Regulation (EU) 2024/1772, criteria for major ICT-related incidents [1] | Economic impact is counted without deducting recoveries (Art. 7(1)); duration and downtime are explicit criteria (Art. 9(3)). **This catalogue is deliberately stricter**: network-wide degradation counts from 1 hour (DORA: 2 hours of downtime of critical functions), and it uses five levels instead of DORA's binary "major / not major". |
| Network availability (section 1) | CIP-135, *Disaster Recovery Plan for Cardano networks* [2] | The thresholds use Cardano's own recovery limits: the rollback limit *k* and the block-production window 3*k*/*f*. Any incident that requires CIP-135 disaster-recovery procedures is SEV-1. |
| Recoverability (section 7) | NIST SP 800-61 Rev. 2, Table 3-4, *Recoverability Effort Categories* [3] | Same four categories with plain-language names, mapped one to one, with Cardano examples. |
| Related incidents (section 9) | DORA RTS Art. 8(2), recurring incidents with the same apparent root cause [1] | Incidents with a shared root cause or a direct causal link are linked, so recurring weaknesses are visible. |
| Incident handling assessment (section 10) | AICPA Trust Services Criteria (SOC 2), CC2.3, CC7.2–CC7.5 and CC8.1 [4] | Each report assesses, criterion by criterion, how the responsible party handled the incident, using SOC 2 test-result language. |

Where this scheme is stricter than a framework, the stricter rule applies. A financial entity subject to DORA still has to make its own classification from its own perspective; this catalogue gives it the provider-side facts to do so.

## 1. Severity

Each incident gets two severity ratings:

- **`severity`**: the impact that actually materialised.
- **`potential_severity`**: the worst credible impact had the issue been fully exploited or left unmitigated, given the conditions at the time (value locked, share of nodes running the affected version, etc.). For near-misses, this is the number that matters most to a risk assessor.

Severity is assessed per impact dimension; **the overall rating is the highest level reached on any dimension**. The rating is about the incident, not about blame: a SEV-1 caused by a third-party dApp says nothing about the Cardano protocol (see `l1_at_fault`).

| Level | Label | Consensus safety | Availability / liveness | Financial loss (gross, USD at time of incident) | Trust and integrity |
|---|---|---|---|---|---|
| **SEV-1** | Critical | Honest nodes follow diverging chains (chain split / partition), a rollback deeper than the security parameter *k*, or an invalid state is accepted by the network | Network-wide halt of block production, or the chain is unusable for settlement for more than 1 hour; or **any incident that requires CIP-135 disaster-recovery procedures** (defined below) | ≥ 1,000,000 | Compromise of keys with protocol-level authority (genesis, governance, hard-fork, major stablecoin mint authority) or of the private keys of a large user population |
| **SEV-2** | High | Honest nodes disagree on validity without a lasting fork | **Network-wide degradation** (defined below) lasting more than 1 hour; or major exchanges/bridges suspend Cardano deposits or withdrawals because of the incident | 100,000 – 999,999 | Compromise of infrastructure or keys of a major ecosystem entity with demonstrated user harm |
| **SEV-3** | Medium | — | Network-wide degradation shorter than 1 hour that self-heals; or a widely used dApp, wallet or service is unavailable or unusable for more than 24 hours | 10,000 – 99,999 | Compromise of an official communication channel used to defraud users; a service operating materially differently from what users were told, to their detriment |
| **SEV-4** | Low | — | Localised or short (< 24 h) unavailability of a single dApp, wallet or service; degraded user experience | 1 – 9,999 | Contained compromise or misinformation without demonstrated user harm |
| **SEV-5** | Informational | — | No user-visible impact | None | None — e.g. a vulnerability found and fixed before any exploitation, a process failure caught internally |

The header fields `impact.consensus_safety` and `impact.liveness` describe Cardano L1 mainnet only. A dApp or wallet outage can therefore have `impact.liveness: none` while still receiving SEV-3 or SEV-4 on the availability dimension. Describe application and service availability in `impact.users_affected` and the report.

### Network availability definitions

The network rows use measurable quantities taken from the protocol itself rather than from service-level agreements.

**Network-wide degradation** means at least one of:

- **Chain density below 90% of expected** over the affected window. On mainnet the expected rate is one block per 20 seconds (active slot coefficient *f* = 0.05), about 180 blocks per hour or 21,600 per epoch. Full mainnet epochs 560 to 660 averaged 97.8% of expected, with the lowest full epoch at 90.1% (epoch 596, which contains the CID-202501 chain split) [5]. A 90% threshold is therefore roughly three times the normal shortfall.
- **Valid, correctly priced transactions routinely waiting more than 5 minutes** (about 15 expected blocks) for inclusion.

**CIP-135 disaster recovery** is required when the network cannot heal itself through normal Ouroboros chain selection [2]:

| CIP-135 scenario | Protocol limit (mainnet) | Triggers the SEV-1 clause when |
|---|---|---|
| 1. Long-lived network partition | Rollback limit *k* = 2,160 blocks, about 12 hours | A partition persists beyond *k*, so operators must truncate their node databases and resynchronise manually |
| 2. Failure to make blocks | At least one block every 3*k*/*f* slots, about 36 hours | Block production has to be restarted by a coordinated recovery group. Any halt longer than 1 hour is already SEV-1, long before this limit. |
| 3. Bad block on chain (3.1–3.4) | — | A block on the chain cannot be processed by some or all node versions and recovery needs coordinated node-version changes (3.1), a rollback (3.2, 3.4) or a hot-fix node that accepts the block (3.3) |

A short fork that resolves itself within *k*, with no bad block on the winning chain, does not trigger this clause. It is still rated on the consensus-safety dimension.

### Rules of thumb

- **Testnets.** Severity describes mainnet impact. An incident confined to a testnet is rated by its effect on mainnet (usually SEV-5), with `potential_severity` describing what would have happened on mainnet.
- **Emergency upgrades.** If mainnet operators had to perform an unscheduled, mandatory upgrade or follow restrictive operating instructions (e.g. "do not restart your node") but no user-visible impact occurred, rate SEV-4.
- **Gross, not net.** Financial loss is the value drained, stolen or lost before any reimbursement, in line with DORA's rule of assessing economic impact "without accounting for financial recoveries" [1]. Reimbursements are recorded separately (`impact.users_made_whole`). A fully reimbursed loss keeps its severity; the response quality shows in the report, not in the rating.
- **Funds frozen are not funds lost.** Value that is temporarily locked but later released counts toward availability, not financial loss.
- **Near-misses.** A vulnerability that was disclosed and fixed with no exploitation is `severity: SEV-5`, or SEV-4 if users had to act (delist, withdraw, migrate) or the service was briefly paused, with a `potential_severity` reflecting the value that was at risk. A pause of a widely used service lasting more than 24 hours is rated on the availability dimension (SEV-3), as the highest dimension wins.
- **When data is uncertain** (e.g. no official loss figure), rate on the best-sourced figure, state the uncertainty in the report, and prefer the lower level unless a primary source supports the higher one.

## 2. Layer

Where in the stack the root cause sits. Pick exactly one.

There is no separate technical/organisational field. Layer `organisational`, the classes `governance-dispute`, `misleading-information` and `shutdown`, and root-cause tags such as `social-engineering` already identify incidents whose root cause lies in people, processes or decisions rather than in software.

| Value | Meaning | Examples |
|---|---|---|
| `protocol` | Ledger rules, consensus, Plutus evaluation, node implementations (`cardano-node`, `cardano-ledger`, `ouroboros-consensus`, Amaru, Dingo, …) | Deserialisation bug causing a chain split |
| `network` | Peer-to-peer layer, mempool, propagation, resource exhaustion, stake pool operations at network scale | Spam / DDoS against the network, mass node disconnection |
| `infrastructure` | Indexers, chain followers, APIs, explorers, oracle feeds, exchange integrations, Mithril, db-sync, individual stake pool or relay hosts | Indexer misreporting leading to wrong balances; a compromised block-producer host |
| `tooling` | Libraries, SDKs, compilers, languages, standard libraries used by builders | Compiler bug producing an unsafe validator |
| `wallet` | Wallet software, hardware wallet apps, key derivation and signing | Faulty signature nonce leaking private keys |
| `dapp` | On-chain validators and off-chain components (batchers, matchmakers, front-ends) of applications: DEXes, lending, marketplaces, bridges, stablecoins | Validator missing a check, drained pool |
| `organisational` | Governance processes, legal entities, operations, communications, people | Hijacked official social media account |

## 3. Incident class

What kind of event the incident was, independent of where it happened (layer) and why (trigger). Class answers the first question a risk assessor asks: was something abused, was it caught in time, did something stop working, or did something go wrong in how the system was run or governed?

| Value | Meaning |
|---|---|
| `exploit` | An attacker actively abused a weakness against users, a protocol, the network or an organisation. The weakness can be in software, configuration, credentials or people's trust (e.g. a drained contract, a hijacked official account, a phishing campaign). |
| `near-miss` | A weakness was found and fixed (or contained) before anyone abused it |
| `outage` | Loss or degradation of availability without abuse of a weakness |
| `malfunction` | The system kept running but produced wrong results (wrong prices, valuations, liquidations or balances) without anyone abusing a weakness. Includes wrong results caused by operator mistakes such as faulty configuration data or a faulty transaction. |
| `governance-dispute` | Dispute, failure or controversy in decision-making, treasury or accountability processes |
| `misleading-information` | Users were harmed or misled by missing, incorrect or late information about how a system behaves |
| `shutdown` | A project or service shut down or paused, leaving users with stranded funds, frozen assets, forced migrations or undelivered products |

## 4. Trigger

| Value | Meaning |
|---|---|
| `malicious` | Deliberately caused by an attacker |
| `accidental` | Caused unintentionally (testing, operator error, unexpected load) |
| `bug` | A software defect surfaced under normal use |
| `design-flaw` | The system behaved as designed, but the design itself caused harm |
| `decision` | A deliberate choice by the responsible party (shutting down a service, a governance or treasury action) rather than an attack, an accident or a defect |
| `disputed` | Sources disagree on intent |
| `unknown` | Not established |

## 5. Status

| Value | Meaning |
|---|---|
| `resolved` | Root cause fixed and incident closed |
| `contained` | Immediate impact stopped; a permanent fix, recovery or reimbursement is still pending but in progress |
| `unresolved` | Immediate impact stopped, but the root cause has not been fixed or losses have not been recovered, and no fix or recovery is in prospect |
| `ongoing` | Incident still developing at time of writing |

## 6. Disclosure quality

How well the responsible party disclosed the incident. This is often the most telling signal for due diligence.

| Value | Meaning |
|---|---|
| `full-post-mortem` | Published root cause, timeline, impact and remediation |
| `partial-post-mortem` | Published some of the above (e.g. root cause without timeline) |
| `statement-only` | Acknowledged the incident without technical detail |
| `third-party-report` | Only reported by press, researchers or community; the responsible party said nothing |
| `none` | Not publicly acknowledged |

## 7. Recoverability

The effort needed to recover, using the four categories of NIST SP 800-61 Rev. 2, Table 3-4 [3], with plain-language names. NIST withdrew Rev. 2 in April 2025 in favour of Rev. 3, which is organised around the NIST Cybersecurity Framework 2.0 and no longer contains these category tables; the Rev. 2 definitions are kept here because they remain widely used and map cleanly onto blockchain incidents.

Assess recoverability for the affected system **and** the affected users at the time of writing. When the two differ, record the worse of the two and explain in the report.

| Value | NIST category | NIST definition | Typical Cardano examples |
|---|---|---|---|
| `routine` | Regular | Time to recovery is predictable with existing resources | Nodes restart automatically and Ouroboros chain selection resolves a short fork; a team fixes an issue with its own staff and normal releases |
| `extra-resources` | Supplemented | Time to recovery is predictable with additional resources | An emergency node release or coordinated operator upgrade; a dApp migrates to patched contracts; users are reimbursed from a treasury |
| `escalated` | Extended | Time to recovery is unpredictable; additional resources and outside help are needed | A cross-organisation incident room; recovery depends on third parties (exchanges, platform operators, custodians, independent reviewers); CIP-135 disaster recovery |
| `not-recoverable` | Not Recoverable | Recovery from the incident is not possible | Stolen funds not returned; private keys exposed on-chain; a product abandoned with raised funds unaccounted for. The incident can only be contained. |

## 8. Sources

Every factual claim in a report must be traceable to a numbered source. Sources are tagged:

- **[P] Primary**: the affected party, the responders, official repositories, on-chain data, audit reports.
- **[S] Secondary**: press, analysts, community write-ups.

Where primary and secondary sources disagree, the report says so in *Disputed or open points* instead of picking a side silently.

## 9. Related incidents

The `related` header field lists catalogue IDs that share the same or a closely similar root cause, affect the same project, or are causally linked (for example, one incident's fix introducing the next). This follows the idea behind DORA's treatment of recurring incidents [1]: repeated incidents with the same apparent root cause point to a systemic weakness even when each one is minor on its own. Unlike DORA, related incidents are not merged into one rating; each keeps its own severity.

## 10. Incident handling assessment (SOC 2-adjacent)

Each report contains an *Incident handling assessment* table, organised like the testing section of a SOC 2 Type 2 report. It assesses how the **responsible party** (the entity that operates or maintains the affected system) handled the incident, against the AICPA Trust Services Criteria most relevant to incident handling [4]. The criteria below are paraphrased; the authoritative text is the AICPA publication.

| Criterion | Focus | What is assessed in the report |
|---|---|---|
| CC7.2 | Monitoring and detection | Did the responsible party's own monitoring detect the anomaly, or was it found by users, researchers or the press? How fast? |
| CC7.3 | Evaluation of events | Was the event triaged and its impact and severity assessed promptly and correctly? |
| CC7.4 | Incident response | Was the incident contained, mitigated and communicated during the response, with clear roles? |
| CC7.5 | Recovery | Was service restored, the root cause determined, and were changes made to prevent recurrence? |
| CC2.3 | External communication | Were users and the ecosystem informed in a timely, accurate and complete way (see `disclosure`)? |
| CC8.1 | Change management | If the root cause was introduced by a change (code, configuration, deployment), was that change designed, tested and approved adequately? |

Each row receives one result:

| Result | Meaning |
|---|---|
| **No exceptions noted** | Public sources show the criterion was met |
| **Exceptions noted** | Public sources show a gap or failure; the exception is described |
| **Not evidenced** | Public sources are insufficient to judge. This is not a finding of failure. |
| **Not applicable** | The criterion does not apply (e.g. CC8.1 when no change caused the incident) |

This is an assessment based on public information, not an audit opinion. A SOC 2 auditor tests controls with access to internal evidence; the catalogue can only report what the responsible party and third parties have made public.

## 11. Required fields and report completeness

Not every incident is fully understood when it is first added. The `completeness` field states how far a report has been developed, and each level defines the fields and sections that must be present. Anything not required may be omitted or set to `null`.

| Field or section | `stub` | `standard` | `full` |
|---|---|---|---|
| `schema_version`, `id`, `title`, `completeness`, `last_updated` | required | required | required |
| `date_start`, `date_disclosed` | required (may be `null` with a note) | required | required |
| `severity`, `class`, `trigger`, `status`, `disclosure` | required | required | required |
| `potential_severity`, `layer`, `l1_at_fault`, `date_end`, `duration` | optional | required | required |
| `affected`, `impact`, `responders`, `root_cause_tags`, `related`, `references` | optional | required | required |
| `recoverability` | optional | optional | required |
| `classification_notes` | optional | optional | optional |
| Summary and *Sources* sections | required | required | required |
| *Timeline*, *Impact*, *Root cause*, *Detection*, *Response and resolution*, *Remediation and follow-up*, *Lessons for builders* | optional | required | required |
| *Incident handling assessment* | optional | optional | required |

A stub is enough to put an incident on record. Contributors and maintainers can raise its completeness later. Whatever the level, every factual claim still needs a source.

## 12. Values that do not fit

Every field with a fixed list of values (`layer`, `class`, `trigger`, `status`, `disclosure`, `recoverability`) also accepts `other`. Use it when no value describes the incident without distortion, and explain the choice in the free-text `classification_notes` field. Also use `classification_notes` for any judgement call a reader would want to know about, such as why one value was preferred over a close alternative.

Maintainers review uses of `other` and the notes from time to time. A situation that keeps recurring is a candidate for a new value in the next version of this standard.

## Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-10-13 | First published version. |

## References

1. European Commission, Commission Delegated Regulation (EU) 2024/1772 of 13 March 2024 supplementing Regulation (EU) 2022/2554 (DORA) with regard to regulatory technical standards specifying the criteria for the classification of ICT-related incidents and cyber threats. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1772
2. Cardano Improvement Proposals, CIP-0135, "Disaster Recovery Plan for Cardano networks", created 2024-06-17. https://github.com/cardano-foundation/CIPs/blob/master/CIP-0135/README.md
3. NIST, Special Publication 800-61 Revision 2, "Computer Security Incident Handling Guide", August 2012 (withdrawn 2025-04-03, superseded by SP 800-61r3), Table 3-4. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf
4. AICPA, "2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy (with Revised Points of Focus – 2022)", TSP Section 100. https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022
5. Koios API, mainnet `epoch_info` (block count per epoch, epochs 560–660), retrieved 2026-10-13. https://api.koios.rest/api/v1/epoch_info?select=epoch_no,blk_count&epoch_no=gte.560
