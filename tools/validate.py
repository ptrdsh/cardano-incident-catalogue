#!/usr/bin/env python3
"""Validate incident reports against TEMPLATE.md and CLASSIFICATION.md.

    python3 tools/validate.py                    # all reports
    python3 tools/validate.py CID-202501         # selected reports
    python3 tools/validate.py --write-catalogue  # regenerate the README table and catalogue.csv, then validate

Requires PyYAML (pip install pyyaml). Exits with status 1 if any report has errors.
The catalogue table in README.md and catalogue.csv are generated from the report headers;
do not edit them by hand.

Per report it checks:
- header: required fields per completeness level, allowed values, `other` explained,
  id matches directory and year, potential_severity not lower than severity;
- body: required sections in template order, the six-row incident handling table,
  the Impact rating sentence matching the header severities;
- sources: numbered 1..n, tagged [P]/[S], every citation listed and every source cited;
- figures: every embedded figure exists and every file in figures/ is embedded;
- links: related incidents exist and link back;
- catalogue: the row in the root README table and catalogue.csv match the headers.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "catalogue.csv"
CSV_FIELDS = ["id", "title", "date_start", "date_end", "date_disclosed", "l1_at_fault", "severity",
              "potential_severity", "layer", "class", "trigger", "status", "recoverability", "disclosure",
              "impact.consensus_safety", "impact.liveness", "impact.funds_lost_usd", "impact.users_made_whole",
              "affected.projects", "root_cause_tags", "related", "completeness", "last_updated", "report"]
LIST_SEPARATOR = " | "

ENUMS = {
    "completeness": {"stub", "standard", "full"},
    "layer": {"protocol", "network", "infrastructure", "tooling", "wallet", "dapp", "organisational", "other"},
    "class": {"exploit", "near-miss", "outage", "malfunction", "governance-dispute",
              "misleading-information", "shutdown", "other"},
    "trigger": {"malicious", "accidental", "bug", "design-flaw", "decision", "disputed", "unknown", "other"},
    "severity": {f"SEV-{i}" for i in range(1, 6)},
    "potential_severity": {f"SEV-{i}" for i in range(1, 6)},
    "status": {"resolved", "contained", "unresolved", "ongoing", "other"},
    "disclosure": {"full-post-mortem", "partial-post-mortem", "statement-only", "third-party-report", "none", "other"},
    "recoverability": {"routine", "extra-resources", "escalated", "not-recoverable", "other"},
}
IMPACT_ENUMS = {
    "consensus_safety": {True, False},
    "liveness": {"none", "degraded", "halted"},
    "users_made_whole": {True, False, "partial"},
}

CORE = ["schema_version", "id", "title", "completeness", "last_updated", "date_start", "date_disclosed",
        "severity", "class", "trigger", "status", "disclosure"]
STANDARD = CORE + ["potential_severity", "layer", "l1_at_fault", "date_end", "duration", "affected", "impact",
                   "responders", "root_cause_tags", "related", "references"]
FULL = STANDARD + ["recoverability"]
REQUIRED_FIELDS = {"stub": CORE, "standard": STANDARD, "full": FULL}

NARRATIVE = ["Timeline (UTC)", "Impact", "Root cause", "Detection", "Response and resolution",
             "Remediation and follow-up"]
SECTION_ORDER = NARRATIVE + ["Incident handling assessment", "Lessons for builders", "Disputed or open points",
                             "Sources"]
REQUIRED_SECTIONS = {
    "stub": ["Sources"],
    "standard": NARRATIVE + ["Lessons for builders", "Sources"],
    "full": NARRATIVE + ["Incident handling assessment", "Lessons for builders", "Sources"],
}

CRITERIA = ["CC7.2 Monitoring and detection", "CC7.3 Evaluation of events", "CC7.4 Incident response",
            "CC7.5 Recovery", "CC2.3 External communication", "CC8.1 Change management"]
RESULTS = {"No exceptions noted", "Exceptions noted", "Not evidenced", "Not applicable"}
TABLE_HEADER = ("| ID | Title | Date | L1 at fault | Severity | Potential | Trigger | Class | Status | Disclosure quality |\n"
                "|---|---|---|---|---|---|---|---|---|---|\n")


def split_report(path: Path):
    """Return (header dict, body) or raise ValueError."""
    match = re.match(r"---\n(.*?)\n---\n(.*)", path.read_text(), re.S)
    if not match:
        raise ValueError("missing YAML front matter")
    try:
        header = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(header, dict):
        raise ValueError("YAML front matter is not a mapping")
    return header, match.group(2)


def catalogue_row(header: dict) -> str:
    date = str(header.get("date_start") or header.get("date_disclosed"))[:10]
    l1 = {True: "yes", False: "no"}.get(header.get("l1_at_fault"), "—")
    cid = header.get("id")
    cells = [f"[{cid}]({cid}/README.md)", header.get("title"), date, l1, header.get("severity"),
             header.get("potential_severity"), header.get("trigger"), header.get("class"), header.get("status"),
             header.get("disclosure")]
    return "| " + " | ".join(str(c) for c in cells) + " |"


def check(report: Path, catalogue: dict[str, str]) -> list[str]:
    try:
        header, body = split_report(report)
    except ValueError as exc:
        return [str(exc)]
    errors = []
    directory = report.parent.name

    level = header.get("completeness")
    if level not in REQUIRED_FIELDS:
        errors.append(f"completeness must be one of {sorted(REQUIRED_FIELDS)}")
        level = "full"
    for field in REQUIRED_FIELDS[level]:
        if field not in header:
            errors.append(f"missing field `{field}` (required for {level})")
    for field, allowed in ENUMS.items():
        if header.get(field) is not None and header[field] not in allowed:
            errors.append(f"`{field}: {header[field]}` is not an allowed value")
    if any(header.get(f) == "other" for f in ENUMS) and not header.get("classification_notes"):
        errors.append("`other` used without `classification_notes`")
    if header.get("l1_at_fault") not in (True, False, None):
        errors.append("`l1_at_fault` must be true or false")
    impact = header.get("impact") or {}
    for field, allowed in IMPACT_ENUMS.items():
        if impact.get(field) is not None and impact[field] not in allowed:
            errors.append(f"`impact.{field}: {impact[field]}` is not an allowed value")
    sev, pot = header.get("severity"), header.get("potential_severity")
    if sev in ENUMS["severity"] and pot in ENUMS["severity"] and pot > sev:
        errors.append(f"potential_severity {pot} is lower than severity {sev}")

    if header.get("id") != directory:
        errors.append(f"id {header.get('id')} does not match directory {directory}")
    if not re.fullmatch(r"CID-\d{6}", directory):
        errors.append("directory name must be CID-yyyyxx")
    start = header.get("date_start")
    if start is not None and not str(start).startswith(directory[4:8]):
        errors.append(f"date_start {start} is not in the ID year {directory[4:8]}")
    for related in header.get("related") or []:
        target = ROOT / related / "README.md"
        if not target.exists():
            errors.append(f"related incident {related} does not exist")
            continue
        try:
            other, _ = split_report(target)
        except ValueError:
            continue
        if directory not in (other.get("related") or []):
            errors.append(f"related incident {related} does not link back to {directory}")

    headings = re.findall(r"^## (.+)$", body, re.M)
    for section in REQUIRED_SECTIONS[level]:
        if section not in headings:
            errors.append(f"missing section `{section}` (required for {level})")
    known = [h for h in headings if h in SECTION_ORDER]
    if known != sorted(known, key=SECTION_ORDER.index):
        errors.append("sections are not in template order")

    impact_text = re.search(r"^## Impact\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if impact_text and level != "stub":
        rated = re.search(r"Rated \**(SEV-\d)", impact_text.group(1))
        potential = re.search(r"[Pp]otential \**(SEV-\d)", impact_text.group(1)[rated.end():]) if rated else None
        if not rated or not potential:
            errors.append("Impact must contain the rating sentence 'Rated SEV-x (...); potential SEV-y (...)'")
        elif (rated.group(1), potential.group(1)) != (sev, pot):
            errors.append(f"Impact rates {rated.group(1)}/{potential.group(1)}, header says {sev}/{pot}")

    assessment = re.search(r"## Incident handling assessment\n(.*?)(?=\n## )", body, re.S)
    if assessment:
        rows = re.findall(r"^\| (CC[^|]+?) \| ([^|]+?) \| (.+) \|$", assessment.group(1), re.M)
        if [r[0] for r in rows] != CRITERIA:
            errors.append("incident handling table must list the six criteria in order")
        for criterion, result, _ in rows:
            if result.strip("* ") not in RESULTS:
                errors.append(f"{criterion}: invalid result `{result}`")

    narrative, _, sources = body.partition("\n## Sources")
    numbers = [int(n) for n in re.findall(r"^(\d+)\. \[[PS]\]", sources, re.M)]
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append("sources must be numbered 1..n and tagged [P] or [S]")
    cited = {int(n) for n in re.findall(r"\[(\d+)\]", narrative)}
    if cited - set(numbers):
        errors.append(f"cited but not listed: {sorted(cited - set(numbers))}")
    if set(numbers) - cited:
        errors.append(f"listed but never cited: {sorted(set(numbers) - cited)}")

    embedded = set(re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", body))
    for image in sorted(embedded):
        if not image.startswith("http") and not (report.parent / image).exists():
            errors.append(f"embedded figure not found: {image}")
    for file in sorted((report.parent / "figures").glob("*")):
        if f"figures/{file.name}" not in embedded:
            errors.append(f"figure file not embedded in the report: figures/{file.name}")

    expected = catalogue_row(header)
    actual = catalogue.get(directory)
    hint = "run `python3 tools/validate.py --write-catalogue`"
    if actual is None:
        errors.append(f"missing from the README catalogue table ({hint})")
    elif actual != expected:
        errors.append(f"README catalogue row is out of date ({hint}); expected:\n    {expected}")
    return errors


def load_headers() -> tuple[list[tuple[str, dict]], str | None]:
    """Return [(directory, header)] for all reports, or an error message if any header cannot be read."""
    headers = []
    for report in sorted(ROOT.glob("CID-*/README.md")):
        try:
            headers.append((report.parent.name, split_report(report)[0]))
        except ValueError as exc:
            return [], f"{report.parent.name}: {exc}"
    return headers, None


def field(header: dict, path: str):
    value = header
    for key in path.split("."):
        value = value.get(key) if isinstance(value, dict) else None
    return value


def csv_cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return LIST_SEPARATOR.join(str(v) for v in value)
    return str(value)


def catalogue_csv(headers: list[tuple[str, dict]]) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(CSV_FIELDS)
    for directory, header in headers:
        writer.writerow([f"{directory}/README.md" if name == "report" else csv_cell(field(header, name))
                         for name in CSV_FIELDS])
    return out.getvalue()


def write_catalogue() -> str | None:
    """Regenerate the README catalogue table and catalogue.csv; return an error message on failure."""
    headers, error = load_headers()
    if error:
        return f"{error}; catalogue not written"
    readme = ROOT / "README.md"
    lines = readme.read_text().splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if line.startswith("| ID | Title |")), None)
    if start is None:
        return "README.md has no catalogue table (a line starting with '| ID | Title |'); catalogue not written"
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    rows = "".join(catalogue_row(header) + "\n" for _, header in headers)
    readme.write_text("".join(lines[:start]) + TABLE_HEADER + rows + "".join(lines[end:]))
    CSV_PATH.write_text(catalogue_csv(headers))
    return None


def main(args: list[str]) -> int:
    if "--write-catalogue" in args:
        args = [a for a in args if a != "--write-catalogue"]
        error = write_catalogue()
        if error:
            print(error)
            return 1
        print("README.md, catalogue.csv: catalogue regenerated")
    reports = [ROOT / a / "README.md" for a in args] if args else sorted(ROOT.glob("CID-*/README.md"))
    catalogue = {m.group(1): m.group(0).rstrip()
                 for m in re.finditer(r"^\| \[(CID-\d{6})\]\(.*$", (ROOT / "README.md").read_text(), re.M)}
    failed = 0
    for report in reports:
        errors = check(report, catalogue)
        if errors:
            failed += 1
            print(f"{report.parent.name}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{report.parent.name}: ok")
    for listed in sorted(set(catalogue) - {r.parent.name for r in sorted(ROOT.glob("CID-*/README.md"))}):
        failed += 1
        print(f"README: catalogue lists {listed}, which has no report")
    headers, error = load_headers()
    if not error and (not CSV_PATH.exists() or CSV_PATH.read_text() != catalogue_csv(headers)):
        failed += 1
        print("catalogue.csv: missing or out of date (run `python3 tools/validate.py --write-catalogue`)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
