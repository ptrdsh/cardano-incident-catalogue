# Cardano Incident Catalogue

A public record of incidents on Cardano and in the dApps, wallets and organisations built on it, technical and organisational, written for companies doing due diligence before building on Cardano and for the teams that build there.

The catalogue is meant to be read by people and by AI agents alike. Every report starts with a machine-readable header, so incidents can be filtered and compared by tools, and knowing how Cardano broke in the past helps AI-assisted development avoid repeating it. Agents working with this repository should start with [AGENTS.md](AGENTS.md).

## Scope

Include an event when it affected, or credibly threatened, the Cardano protocol, network, developer tooling, infrastructure, a Cardano dApp or wallet, or an organisation acting in an official ecosystem role. An entry needs enough public evidence to establish the event and explain why it matters to builders or due-diligence readers. Near-misses, project shutdowns, governance failures and impersonation campaigns qualify when they expose a concrete technical, operational or trust risk.

Do not include ordinary defects with no material impact or credible security consequence, general cryptocurrency scams that merely mention ADA, market-price movements without a system failure, or allegations that cannot be separated from speculation. A dispute may itself be an incident when the documented governance or disclosure failure—not the unproven allegation—is what the report assesses.

## Structure

Each incident has its own directory, `CID-yyyyxx` (Cardano Incident Disclosure), where `yyyy` is the year the incident started and `xx` is a two-digit sequence number (01–99) assigned in the order incidents were added to the catalogue. The sequence does not imply chronology within a year: there is no complete list of incidents, contributions arrive out of order, and some incidents are only disclosed months after they were resolved, for security reasons.

Each directory contains a `README.md` with:

- a machine-readable **YAML header** with the fields listed in [TEMPLATE.md](TEMPLATE.md) and explained under [Reading a report](#reading-a-report);
- a report with a fixed set of sections: executive summary, timeline (UTC), impact, root cause, detection, response and resolution, remediation and follow-up, incident handling assessment, lessons for builders, disputed or open points, and numbered sources;
- where useful, a `figures/` folder with images from the sources (credited and linked in the caption) or, where nothing suitable exists, a chart drawn by the catalogue from cited data.

Third-party images remain the property of their authors and are credited in each caption. Rights holders who want an image removed can open a pull request removing it.

## Reading a report

The header classifies each incident along a fixed set of dimensions. The values are defined in [CLASSIFICATION.md](CLASSIFICATION.md). The scheme borrows from established frameworks and is deliberately stricter where they differ: severity follows the EU DORA incident-classification standard (Delegated Regulation 2024/1772), network availability is anchored to Cardano's disaster recovery plan (CIP-135), recoverability uses the NIST SP 800-61 categories, and incident handling is assessed against SOC 2 criteria (CC2.3, CC7.2–CC7.5, CC8.1). The catalogue rests on public sources only; it is neither a regulatory classification nor an audit.

### Severity

| Level | Label | Typical example |
|---|---|---|
| SEV-1 | Critical | Chain split, network halt, CIP-135 disaster recovery required, or ≥ USD 1M lost |
| SEV-2 | High | Network-wide degradation > 1 h, honest nodes disagreeing on validity, or USD 100k – 1M lost |
| SEV-3 | Medium | Self-healing network degradation < 1 h, a major dApp unusable > 24 h, hijacked official channel, or USD 10k – 100k lost |
| SEV-4 | Low | Short single-service outage, emergency upgrade without user impact, contained compromise |
| SEV-5 | Informational | No user-visible impact, e.g. a vulnerability fixed before exploitation or confined to a testnet |

Each incident is rated twice. `severity` is the impact that actually happened; `potential_severity` is the worst credible outcome had the issue not been caught or contained, which for near-misses is the number that matters most. Both are rated on four dimensions (consensus safety, availability, financial loss, trust and integrity), and the highest level on any dimension is the rating.

### Other classifiers

| Field | Question it answers | Values |
|---|---|---|
| `l1_at_fault` | Was the root cause in the Cardano protocol or node software? A SEV-1 in a dApp says nothing about the L1. | `true`, `false` |
| `layer` | Where in the stack did the root cause sit? | `protocol`, `network`, `infrastructure`, `tooling`, `wallet`, `dapp`, `organisational` |
| `class` | What kind of event was it? | `exploit` (a weakness was abused), `near-miss` (found and fixed before abuse), `outage`, `malfunction` (kept running with wrong results), `governance-dispute`, `misleading-information`, `shutdown` |
| `trigger` | What set it off? | `malicious`, `accidental`, `bug`, `design-flaw` (worked as designed, the design caused harm), `decision`, `disputed`, `unknown` |
| `status` | Where does it stand today? | `resolved`, `contained` (recovery under way), `unresolved` (no fix or recovery in prospect), `ongoing` |
| `recoverability` | How much effort did recovery take, for the system or its users, whichever is worse? | `routine`, `extra-resources`, `escalated` (outside help, unpredictable timing), `not-recoverable` |
| `disclosure` | How well did the responsible party disclose it? | `full-post-mortem`, `partial-post-mortem`, `statement-only`, `third-party-report` (only others reported it), `none` |
| `related` | Which incidents share its root cause or project, or are causally linked to it? | catalogue IDs |
| `completeness` | How far has the report been developed? | `stub`, `standard`, `full` |

Fields with a fixed list of values also accept `other` when nothing fits; the reason goes in `classification_notes`, which records every judgement call behind the ratings.

The `impact` block quantifies the damage. `consensus_safety` and `liveness` describe the Cardano L1 only, so a dApp outage appears in `severity`, not in `liveness`. `funds_lost_usd` is gross and valued at the time of the incident, before any reimbursement; whether users were reimbursed is recorded separately in `users_made_whole`. Throughout the header, `null` means unknown, never zero, and a date without a time means the time was not established. Times are UTC.

Each full report also contains an *Incident handling assessment*: how the responsible party detected, evaluated, contained, recovered from and communicated the incident, with one SOC 2 result per criterion (*No exceptions noted*, *Exceptions noted*, *Not evidenced*, *Not applicable*). Sources are tagged **[P]** (primary: the affected party, responders, repositories, on-chain data) or **[S]** (secondary: press, analysts, community).

## Catalogue

| ID | Title | Date | Severity | Potential | Trigger | Class | Status | Disclosure quality |
|---|---|---|---|---|---|---|---|---|
| [CID-202001](CID-202001/README.md) | HAPPY Stake Pool Host Compromise via Exposed Docker Socket | 2020-08-06 | SEV-2 | SEV-2 | malicious | exploit | unresolved | partial-post-mortem |
| [CID-202101](CID-202101/README.md) | Marketplace Double-Satisfaction Vulnerability (jpg.store) | 2021-11-22 | SEV-4 | SEV-4 | bug | near-miss | resolved | statement-only |
| [CID-202201](CID-202201/README.md) | SundaeSwap Launch Congestion and Failed Orders | 2022-01-20 | SEV-3 | SEV-2 | design-flaw | outage | resolved | partial-post-mortem |
| [CID-202202](CID-202202/README.md) | Minswap LP Token Minting Vulnerability | 2022-03-21 | SEV-3 | SEV-1 | bug | near-miss | resolved | partial-post-mortem |
| [CID-202203](CID-202203/README.md) | SECP256k1 Binding Flaw and Legacy Testnet Incompatibility | 2022-07-15 | SEV-5 | SEV-1 | accidental | near-miss | resolved | partial-post-mortem |
| [CID-202204](CID-202204/README.md) | Node 1.35.x Minimum-Fee Bug, Mainnet Forks and Rollback to 1.34.1 | 2022-07-22 | SEV-2 | SEV-1 | bug | outage | resolved | partial-post-mortem |
| [CID-202205](CID-202205/README.md) | Ardana Stablecoin Project Halts Development | 2022-11-24 | SEV-3 | SEV-1 | disputed | shutdown | unresolved | statement-only |
| [CID-202301](CID-202301/README.md) | Mass Node Disconnection and Restart | 2023-01-22 | SEV-3 | SEV-2 | bug | outage | resolved | partial-post-mortem |
| [CID-202302](CID-202302/README.md) | Djed Reserve Ratio Breach and Depeg | 2023-06-10 | SEV-3 | SEV-3 | design-flaw | outage | unresolved | partial-post-mortem |
| [CID-202303](CID-202303/README.md) | MuesliSwap Matchmaker Slippage Retention and Refunds | 2023-08-07 | SEV-3 | SEV-3 | design-flaw | misleading-information | unresolved | partial-post-mortem |
| [CID-202401](CID-202401/README.md) | Liqwid Faulty Oracle Transaction | 2024-01-10 | SEV-3 | SEV-1 | bug | malfunction | resolved | full-post-mortem |
| [CID-202402](CID-202402/README.md) | Lenfi BTN Liquidations Incident | 2024-05-11 | SEV-2 | SEV-2 | design-flaw | malfunction | resolved | full-post-mortem |
| [CID-202403](CID-202403/README.md) | Reference Script Spam (DDoS) Attack on Mainnet | 2024-06-24 | SEV-2 | SEV-2 | malicious | exploit | resolved | partial-post-mortem |
| [CID-202404](CID-202404/README.md) | Conway Ledger State Replay Bug after Chang Hard Fork | 2024-09-01 | SEV-4 | SEV-2 | bug | outage | resolved | partial-post-mortem |
| [CID-202405](CID-202405/README.md) | Cardano Foundation X Account Compromise (ADAsol scam) | 2024-12-08 | SEV-3 | SEV-2 | malicious | exploit | unresolved | statement-only |
| [CID-202406](CID-202406/README.md) | Lenfi V2 Smart Contract Vulnerability | 2024-12-11 | SEV-3 | SEV-1 | bug | near-miss | resolved | partial-post-mortem |
| [CID-202407](CID-202407/README.md) | Plomin Hard Fork DoS Vector and Mandatory Hotfix 10.1.4 | 2024-12-30 | SEV-4 | SEV-2 | bug | near-miss | resolved | partial-post-mortem |
| [CID-202501](CID-202501/README.md) | Pig vs Chicken Chainsplit | 2025-11-21 | SEV-1 | SEV-1 | disputed | exploit | resolved | full-post-mortem |
| [CID-202502](CID-202502/README.md) | Milkomeda C1 Sidechain Sunset and Frozen Residual Funds | 2025-04-22 | SEV-3 | SEV-1 | decision | shutdown | unresolved | statement-only |
| [CID-202503](CID-202503/README.md) | 318M ADA Unredeemed-Voucher Funds, Disclosure Gap and Independent Review | 2025-05-06 | SEV-4 | SEV-1 | decision | governance-dispute | resolved | full-post-mortem |
| [CID-202504](CID-202504/README.md) | Fake Eternl Desktop Phishing Campaign | 2025-12-21 | SEV-4 | SEV-2 | malicious | exploit | unresolved | third-party-report |
| [CID-202601](CID-202601/README.md) | SecondFi Wallet Signing Nonce Flaw | 2026-06-21 | SEV-1 | SEV-1 | malicious | exploit | contained | partial-post-mortem |
| [CID-202602](CID-202602/README.md) | DeltaDeFi Hydra DEX Operational Pause | 2026-07-15 | SEV-3 | SEV-3 | decision | shutdown | unresolved | statement-only |
| [CID-202603](CID-202603/README.md) | Wanchain Cardano Bridge Exploit (NIGHT) | 2026-07-20 | SEV-1 | SEV-1 | malicious | exploit | unresolved | partial-post-mortem |
| [CID-202604](CID-202604/README.md) | Splash StableSwap Pool Exploit (ADA/OADA) | 2026-09-13 | SEV-2 | SEV-1 | malicious | exploit | contained | full-post-mortem |
| [CID-202605](CID-202605/README.md) | Deeply Nested Native Script Crashes Tooling on Preprod | 2026-09-16 | SEV-4 | SEV-3 | accidental | outage | contained | partial-post-mortem |

## Contributing

- Copy [TEMPLATE.md](TEMPLATE.md) into a new `CID-yyyyxx/README.md`, using the next free number for the year the incident started, and add the incident to the catalogue table above.
- You don't need the full picture to start. A report can be filed as a `stub` with only the core fields and sources, and raised to `standard` or `full` later ([CLASSIFICATION.md](CLASSIFICATION.md), section 11).
- If no predefined value fits, use `other` and explain in `classification_notes` rather than forcing the incident into the wrong category (section 12).
- Every factual claim needs a numbered source. Prefer primary sources (post-mortems, official statements, repositories, on-chain data) and say so where only secondary sources exist.
- Figures go in the incident's `figures/` folder. Prefer images already published in the sources, credit the author and link the original in the caption. Add your own chart only where no such image exists, and name the data source in the caption.
- Stay neutral. Where accounts conflict, present each side with its source under *Disputed or open points*.
- Do not publish details of vulnerabilities that are not yet fixed. Report those to the affected project (for the Cardano core, security@intersectmbo.org) and add the incident once it is resolved.
- Run `python3 tools/validate.py` (needs PyYAML) and fix every error before opening a pull request. It checks structure and internal consistency, not facts: required fields and values, section order, source numbering and citations, figures, `related` links in both directions, and that the report's rating sentence and its row in the catalogue table match the header.

## Why publish incidents at all? Aren't incidents bad?

**No.**

Cardano is a technology platform, in the same sense that AWS is one. Decision makers choosing the technology behind their product do not need a perfect history. They need to know what happened in the past, how it was handled, and what changed so that it does not happen again. In Web2, technology providers answer this at scale with ISAE 3000 / SOC 2 audits, which examine how a company identifies, controls and responds to the risks of its technology. Once a provider passes its annual audit, its clients can tick off pages of their own due-diligence checklists in one go, which saves cost, reduces risk and makes the audited provider more attractive. The point of these audits is not to have no risks; it is to handle issues well when, not if, they occur.

In Web3 there is no equivalent audit for decentralised technology providers (attempts have been made), so the risk of building on a chain is still assessed through the manual due-diligence questionnaires of large institutions. The questions about incidents in those questionnaires aim to learn how the risks of the chain are managed, as a SOC 2 audit would, not to learn the technical details of a single incident. Sweeping incidents under the carpet, or confining them to closed councils, does not help: a chain with no incidents is either too young to have had one, which means it is untested for the day an issue inevitably arises, or is not being used. An open incident catalogue is not an admission of defeat. It is the evidence that Cardano is battle-tested and will survive the next, unavoidable incident.
