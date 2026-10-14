# Instructions for agents

This repository is a public catalogue of incidents on Cardano and in the dApps, wallets and organisations built on it. Readers use it for due diligence and to learn from past failures, so accuracy matters more than coverage: an unsourced or overstated claim does more harm than a missing one.

## Where things are

| Path | Purpose |
|---|---|
| `README.md` | Scope, what each header field means (*Reading a report*), the catalogue table, contribution rules |
| `CLASSIFICATION.md` | Authoritative definitions and rating rules; wins over any summary elsewhere |
| `TEMPLATE.md` | Header fields and section order for a report |
| `CID-yyyyxx/README.md` | One incident per directory; images in `figures/` |
| `tools/validate.py` | Structural checks; run before finishing any change |

## Answering questions from the catalogue

- Filter, count and compare on the YAML headers, not the prose. All headers in one line (needs PyYAML):
  `[next(yaml.safe_load_all(p.read_text())) for p in Path(".").glob("CID-*/README.md")]`
- Do not call an incident a Cardano failure unless `l1_at_fault` is `true`. A SEV-1 in a dApp says nothing about the protocol.
- `null` is unknown, not zero. When summing losses, say how many incidents have no figure. Losses are gross; do not net out reimbursements.
- Status and figures are as of the report's `last_updated` date. Say so when it matters.
- Cite the incident ID and the report's source numbers. Carry over the report's caveats (*Disputed or open points*), and flag claims that rest only on **[S]** sources.
- If you add knowledge from outside the catalogue, say that it is not from the catalogue.

## Adding a report

1. Check the incident fits the README *Scope* and is not already covered: search titles, `affected.projects` and the reports' text for the project name.
2. Use the year the incident started and the next free number for that year as the ID (`CID-yyyyxx`).
3. Gather primary sources first: the affected party's statements and post-mortems, repositories, release notes, on-chain data. Use secondary sources to fill gaps, and say where only secondary sources exist.
4. Copy `TEMPLATE.md`. File a `stub` if the facts are thin; do not pad a report to reach `full`.
5. Classify strictly by `CLASSIFICATION.md` and record every judgement call in `classification_notes`.
6. Add the catalogue row to `README.md`. The validator prints the expected row.

## Editing an existing report

- Read the whole report, and the parts of `CLASSIFICATION.md` you rely on, before changing anything.
- A changed classification value needs a rule from `CLASSIFICATION.md`; name it in `classification_notes`. Keep the header, the closing rating sentence of *Impact* and the catalogue row in step.
- When shortening, keep every sourced fact; state it fully once and refer to it elsewhere.
- `related` links need a shared root cause, the same project or a causal link (`CLASSIFICATION.md`, section 9), and must be added or removed on both reports.
- Touch other reports only for those back-links. Set `last_updated` on every report you change.

## Evidence rules

- Cite only sources you have opened and read. Never cite from memory or from search-result snippets. If a page blocks access, use an archived copy (web.archive.org) and give both URLs.
- Recompute every number you write: USD conversions with the price, its source and date; durations between timeline entries; block, slot and transaction counts; totals.
- Use `null` for what is not established, and label inferences ("which suggests", "the catalogue infers").
- Stay neutral. Present conflicting accounts side by side under *Disputed or open points*; do not settle them silently.
- Never publish details of a vulnerability that is not yet fixed.

## Useful techniques

- Times are UTC. The posting time of an X post can be decoded from its ID: `(id >> 22) + 1288834974657` milliseconds since the Unix epoch.
- On-chain facts (transactions, blocks, epochs, pool data, protocol parameters) can be checked against the Koios API (`https://api.koios.rest/api/v1/`) and cited as primary sources with the retrieval date.
- GitHub timestamps for issues, pull requests and releases are available from the GitHub API and are more precise than page renderings.

## Before you finish

- `python3 tools/validate.py` passes for every report. It checks structure only; the facts still have to stand up against the sources.
- Report what you changed, every classification value you changed and why, and anything you could not verify.
