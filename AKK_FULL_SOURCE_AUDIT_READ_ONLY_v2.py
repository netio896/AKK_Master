# -*- coding: utf-8 -*-
"""
AKK FULL SOURCE AUDIT — READ ONLY v2
FROM SOURCE / ZERO ASSUMPTION / DO NOT USE CHAT MEMORY

Scope:
01 Root Inventory
02 Current Core Recovery Audit
03 Release Candidate Audit
04 Archive Reference Audit
05 Three-Way Hash Comparison
06 P1/P2/P3 Candidate Classification
07 Native CAD / Native Source Detection
08 Control File Detection
09 Phase Map Validation
10 Register Validation
11 Duplicate / Conflict Review
12 Legacy Contamination Scan (external registry driven)
13 ZIP Integrity
14 Empty Shell Detection
15 Multi-Gate Summary

Safety:
- SOURCE FILES ARE READ ONLY.
- NO source move / copy / rename / overwrite / delete.
- NO Builder execution.
- Script writes reports only into a timestamped audit-report folder.
- P1/P2/P3 results are SUGGESTIONS ONLY and require human approval.
- Legacy patterns are read from AKK_RETIRED_DATA_REGISTRY.csv; no legacy project
  dimensions, bed counts, room counts, or other retired project facts are hardcoded.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------
# CORE PATHS — path names only; no project geometry/capacity facts here.
# ---------------------------------------------------------------------

ROOT = Path(r"H:\Hermes-KnowledgeBase\项目\核心项目")

CURRENT_CORE_CANDIDATE_PATHS = [
    ROOT / "AKK_CURRENT_CORE_v3.1_RECOVERY",
    ROOT / "AKK_CURRENT_CORE_v3.1_RECOVERY_CLEAN",
]

RELEASE_CANDIDATE = ROOT / "AKK_Final_Client_Package_v3.1_RELEASE_CANDIDATE"

ARCHIVE_REFERENCE = (
    ROOT
    / "99_ARCHIVE_OLD"
    / "AKK_Final_Client_Package_v3.1_RELEASE_CANDIDATE"
)

CONTROL_FILENAMES = {
    "SOURCE_REGISTER": "AKK_SOURCE_REGISTER.csv",
    "PHASE_MAP": "AKK_PHASE_MAP.csv",
    "ASSET_REGISTER": "AKK_ASSET_REGISTER.csv",
    "RETIRED_DATA_REGISTRY": "AKK_RETIRED_DATA_REGISTRY.csv",
}

NATIVE_EXTENSIONS = {".dwg", ".dxf", ".obj", ".fbx", ".skp"}

TEXT_SCAN_EXTENSIONS = {
    ".md", ".txt", ".csv", ".json", ".yaml", ".yml",
    ".ini", ".cfg", ".xml", ".html", ".htm", ".ps1", ".py",
}

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_DIR = ROOT / f"AKK_AUDIT_REPORT_v2_{STAMP}"

OUT = {
    "TXT": REPORT_DIR / f"AKK_FULL_AUDIT_v2_{STAMP}.txt",
    "ROOT_INVENTORY": REPORT_DIR / f"AKK_ROOT_INVENTORY_{STAMP}.csv",
    "ROLE_SUMMARY": REPORT_DIR / f"AKK_ROLE_SUMMARY_{STAMP}.csv",
    "THREE_WAY": REPORT_DIR / f"AKK_THREE_WAY_HASH_COMPARISON_{STAMP}.csv",
    "SOURCE_CLASSIFICATION": REPORT_DIR / f"AKK_SOURCE_CLASSIFICATION_REVIEW_{STAMP}.csv",
    "NATIVE_SCAN": REPORT_DIR / f"AKK_NATIVE_SOURCE_SCAN_{STAMP}.csv",
    "CONTROL_STATUS": REPORT_DIR / f"AKK_CONTROL_FILE_STATUS_{STAMP}.csv",
    "PHASE_VALIDATION": REPORT_DIR / f"AKK_PHASE_MAPPING_VALIDATION_{STAMP}.csv",
    "REGISTER_VALIDATION": REPORT_DIR / f"AKK_REGISTER_VALIDATION_{STAMP}.csv",
    "DUPLICATES": REPORT_DIR / f"AKK_DUPLICATES_{STAMP}.csv",
    "CONFLICTS": REPORT_DIR / f"AKK_HASH_CONFLICTS_{STAMP}.csv",
    "LEGACY": REPORT_DIR / f"AKK_LEGACY_CONTAMINATION_REPORT_{STAMP}.csv",
    "ZIP": REPORT_DIR / f"AKK_ZIP_INTEGRITY_{STAMP}.csv",
    "EMPTY": REPORT_DIR / f"AKK_EMPTY_SHELL_REPORT_{STAMP}.csv",
    "GATES": REPORT_DIR / f"AKK_MULTI_GATE_SUMMARY_{STAMP}.csv",
}

# ---------------------------------------------------------------------
# GENERIC HELPERS
# ---------------------------------------------------------------------

def norm_path_text(value: str) -> str:
    return value.strip().strip('"').strip("'").replace("/", os.sep)


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest().upper()


def files_under(base: Path, exclude_report_dir: bool = True) -> list[Path]:
    if not base.exists() or not base.is_dir():
        return []
    result: list[Path] = []
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if exclude_report_dir and REPORT_DIR in p.parents:
            continue
        result.append(p)
    return sorted(result, key=lambda p: str(p).lower())


def dirs_under(base: Path, exclude_report_dir: bool = True) -> list[Path]:
    if not base.exists() or not base.is_dir():
        return []
    result: list[Path] = []
    for p in base.rglob("*"):
        if not p.is_dir():
            continue
        if exclude_report_dir and (p == REPORT_DIR or REPORT_DIR in p.parents):
            continue
        result.append(p)
    return sorted(result, key=lambda p: str(p).lower())


def bytes_total(paths: Iterable[Path]) -> int:
    total = 0
    for p in paths:
        try:
            total += p.stat().st_size
        except OSError:
            pass
    return total


def mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def safe_rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("/", "\\")
    except Exception:
        return str(path)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text_best_effort(path: Path) -> tuple[str | None, str]:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "cp1252"):
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return None, f"ERROR:{e}"
    return None, "UNREADABLE_TEXT"


def read_csv_best_effort(path: Path) -> tuple[list[dict[str, str]], list[str], str]:
    text, encoding = read_text_best_effort(path)
    if text is None:
        return [], [], encoding
    try:
        reader = csv.DictReader(text.splitlines())
        rows = []
        for row in reader:
            clean = {
                (k or "").strip(): (v or "").strip()
                for k, v in row.items()
            }
            rows.append(clean)
        return rows, list(reader.fieldnames or []), encoding
    except Exception as e:
        return [], [], f"CSV_ERROR:{e}"


def find_column(headers: list[str], candidates: list[str]) -> str | None:
    normalized = {normalize_header(h): h for h in headers}
    for c in candidates:
        key = normalize_header(c)
        if key in normalized:
            return normalized[key]
    return None


def file_hash_or_error(path: Path) -> str:
    try:
        return sha256(path)
    except Exception as e:
        return f"ERROR:{e}"


def resolve_declared_path(raw: str, control_file: Path) -> Path | None:
    raw = raw.strip()
    if not raw:
        return None
    expanded = os.path.expandvars(raw)
    p = Path(norm_path_text(expanded))
    candidates = []
    if p.is_absolute():
        candidates.append(p)
    else:
        candidates.extend([
            ROOT / p,
            control_file.parent / p,
        ])
    for c in candidates:
        if c.exists():
            return c
    return candidates[0] if candidates else p


def discover_exact_filename(filename: str) -> list[Path]:
    matches = []
    for p in ROOT.rglob(filename):
        if p.is_file() and REPORT_DIR not in p.parents:
            matches.append(p)
    return sorted(matches, key=lambda p: str(p).lower())


def dir_summary(path: Path) -> dict[str, Any]:
    fs = files_under(path)
    ds = dirs_under(path)
    return {
        "Path": str(path),
        "Exists": path.exists(),
        "Files": len(fs),
        "Folders": len(ds),
        "SizeBytes": bytes_total(fs),
        "SizeMB": mb(bytes_total(fs)),
    }


def select_current_core_candidate() -> tuple[Path | None, list[Path]]:
    existing = [p for p in CURRENT_CORE_CANDIDATE_PATHS if p.exists()]
    if len(existing) == 1:
        return existing[0], existing
    if len(existing) > 1:
        # Do not auto-promote between multiple candidates.
        return None, existing
    return None, []


# ---------------------------------------------------------------------
# ROLE / HASH HELPERS
# ---------------------------------------------------------------------

def build_role_map(base: Path | None) -> dict[str, dict[str, Any]]:
    if base is None or not base.exists():
        return {}
    result = {}
    for p in files_under(base):
        rel = safe_rel(p, base)
        result[rel] = {
            "Path": p,
            "SHA256": file_hash_or_error(p),
            "SizeBytes": p.stat().st_size if p.exists() else 0,
        }
    return result


def role_triplet_status(
    recovery: dict[str, dict[str, Any]],
    release: dict[str, dict[str, Any]],
    archive: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    all_rels = sorted(set(recovery) | set(release) | set(archive), key=str.lower)

    for rel in all_rels:
        r = recovery.get(rel)
        l = release.get(rel)
        a = archive.get(rel)

        hashes = [
            x["SHA256"] for x in (r, l, a)
            if x is not None and not str(x["SHA256"]).startswith("ERROR:")
        ]
        unique_hashes = set(hashes)

        if r and l and a:
            status = "ALL_THREE_IDENTICAL" if len(unique_hashes) == 1 else "HASH_CONFLICT"
        elif r and a and not l:
            status = "MISSING_IN_RELEASE__RECOVERY_ARCHIVE_MATCH" if r["SHA256"] == a["SHA256"] else "RECOVERY_ARCHIVE_CONFLICT"
        elif l and a and not r:
            status = "MISSING_IN_RECOVERY__RELEASE_ARCHIVE_MATCH" if l["SHA256"] == a["SHA256"] else "RELEASE_ARCHIVE_CONFLICT"
        elif r and l and not a:
            status = "MISSING_IN_ARCHIVE__RECOVERY_RELEASE_MATCH" if r["SHA256"] == l["SHA256"] else "RECOVERY_RELEASE_CONFLICT"
        elif r:
            status = "RECOVERY_ONLY"
        elif l:
            status = "RELEASE_ONLY"
        else:
            status = "ARCHIVE_ONLY"

        rows.append({
            "RelativePath": rel,
            "RecoveryPath": str(r["Path"]) if r else "",
            "RecoverySHA256": r["SHA256"] if r else "",
            "ReleasePath": str(l["Path"]) if l else "",
            "ReleaseSHA256": l["SHA256"] if l else "",
            "ArchivePath": str(a["Path"]) if a else "",
            "ArchiveSHA256": a["SHA256"] if a else "",
            "Status": status,
            "HumanReviewRequired": "YES" if status != "ALL_THREE_IDENTICAL" else "NO",
        })
    return rows


# ---------------------------------------------------------------------
# SOURCE CLASSIFICATION — suggestion only
# ---------------------------------------------------------------------

def suggest_source_level(path: Path) -> tuple[str, str, str, str]:
    """
    Returns: CandidateLevel, Reason, CurrentStatus, HumanApprovalRequired
    No project-specific retired parameter is used here.
    """
    name = path.name.upper()
    full = str(path).upper()
    ext = path.suffix.lower()

    if ext in NATIVE_EXTENSIONS:
        return (
            "P1_CANDIDATE",
            "Native design/source file extension",
            "VERIFY",
            "YES",
        )

    p1_tokens = (
        "SOURCE_OF_TRUTH",
        "MASTER_BASELINE",
        "ENGINEER_DRAWING",
        "SOURCE_REGISTER",
        "PHASE_MAP",
        "ASSET_REGISTER",
    )
    if any(t in name for t in p1_tokens):
        return (
            "P1_CANDIDATE",
            "Filename indicates controlled source / baseline / engineer / register role",
            "VERIFY",
            "YES",
        )

    p2_tokens = (
        "VISUAL",
        "MATERIAL",
        "LIGHTING",
        "COLOR_SYSTEM",
        "WAYFINDING",
        "FF&E",
        "POD_ROOM",
        "BATH_WC",
        "CORRIDOR",
        "OVERLAY",
    )
    if any(t in name for t in p2_tokens) or "DESIGN_DOCUMENTATION" in full:
        return (
            "P2_CANDIDATE",
            "Visual/design-development naming or location",
            "VERIFY",
            "YES",
        )

    p3_tokens = (
        "PROPOSAL",
        "CONCEPT",
        "WORKING",
        "REFERENCE",
        "README",
    )
    if any(t in name for t in p3_tokens):
        return (
            "P3_CANDIDATE",
            "Proposal / concept / working / reference naming",
            "VERIFY",
            "YES",
        )

    return (
        "UNCLASSIFIED",
        "No conservative filename/location rule matched",
        "VERIFY",
        "YES",
    )


# ---------------------------------------------------------------------
# PHASE MAP VALIDATION
# ---------------------------------------------------------------------

def parse_phase_number(value: str) -> int | None:
    if not value:
        return None
    m = re.search(r"(?:PHASE\s*)?0*([1-9]|1[0-5])\b", value, re.IGNORECASE)
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 15 else None


def validate_phase_map(path: Path) -> tuple[list[dict[str, Any]], str]:
    rows, headers, enc = read_csv_best_effort(path)
    if not headers:
        return [{
            "Phase": "",
            "SourceDeclared": "",
            "SourceExists": "",
            "SourceHashDeclared": "",
            "SourceHashActual": "",
            "HashStatus": "",
            "OutputDeclared": "",
            "OutputExists": "",
            "StatusDeclared": "",
            "RowGate": "BLOCKED_UNREADABLE_PHASE_MAP",
            "Notes": enc,
        }], "BLOCKED_UNREADABLE_PHASE_MAP"

    phase_col = find_column(headers, ["Phase", "PhaseID", "PhaseNumber", "PhaseNo"])
    source_col = find_column(headers, ["Source", "SourcePath", "SourceFile", "SourceAsset", "InputPath"])
    hash_col = find_column(headers, ["SHA256", "SourceSHA256", "SourceHash", "Hash"])
    output_col = find_column(headers, ["Output", "OutputPath", "OutputFile", "DeliverablePath", "TargetPath"])
    status_col = find_column(headers, ["Status", "PhaseStatus", "CurrentStatus"])

    missing_required_columns = []
    if phase_col is None:
        missing_required_columns.append("Phase")
    if source_col is None:
        missing_required_columns.append("Source")
    if status_col is None:
        missing_required_columns.append("Status")

    if missing_required_columns:
        gate = "BLOCKED_PHASE_MAP_COLUMNS_MISSING"
        return [{
            "Phase": "",
            "SourceDeclared": "",
            "SourceExists": "",
            "SourceHashDeclared": "",
            "SourceHashActual": "",
            "HashStatus": "",
            "OutputDeclared": "",
            "OutputExists": "",
            "StatusDeclared": "",
            "RowGate": gate,
            "Notes": "Missing columns: " + ", ".join(missing_required_columns),
        }], gate

    result_rows: list[dict[str, Any]] = []
    phase_seen: dict[int, int] = defaultdict(int)
    blocked = False

    for row in rows:
        raw_phase = row.get(phase_col, "")
        phase_num = parse_phase_number(raw_phase)
        if phase_num is not None:
            phase_seen[phase_num] += 1

        source_decl = row.get(source_col, "")
        source_path = resolve_declared_path(source_decl, path) if source_decl else None
        source_exists = bool(source_path and source_path.exists())

        declared_hash = row.get(hash_col, "") if hash_col else ""
        actual_hash = ""
        hash_status = "NOT_DECLARED"
        if source_exists and source_path and source_path.is_file():
            actual_hash = file_hash_or_error(source_path)
            if declared_hash:
                hash_status = "MATCH" if declared_hash.upper() == actual_hash.upper() else "MISMATCH"
            else:
                hash_status = "NOT_DECLARED"
        elif source_decl:
            hash_status = "SOURCE_NOT_FOUND"

        output_decl = row.get(output_col, "") if output_col else ""
        output_path = resolve_declared_path(output_decl, path) if output_decl else None
        output_exists = bool(output_path and output_path.exists()) if output_decl else ""

        status_decl = row.get(status_col, "")
        row_gate = "PASS"
        notes = []

        if phase_num is None:
            row_gate = "BLOCKED"
            notes.append("Phase could not be parsed as 01–15")
        if not source_decl:
            row_gate = "BLOCKED"
            notes.append("Source is empty")
        elif not source_exists:
            row_gate = "BLOCKED"
            notes.append("Source path not found")
        if hash_status == "MISMATCH":
            row_gate = "BLOCKED"
            notes.append("Declared source hash mismatch")
        if output_col and output_decl and output_exists is False:
            row_gate = "BLOCKED"
            notes.append("Declared output path not found")
        if not status_decl.strip():
            row_gate = "BLOCKED"
            notes.append("Status is empty")

        if row_gate != "PASS":
            blocked = True

        result_rows.append({
            "Phase": f"{phase_num:02d}" if phase_num else raw_phase,
            "SourceDeclared": source_decl,
            "SourceExists": source_exists,
            "SourceHashDeclared": declared_hash,
            "SourceHashActual": actual_hash,
            "HashStatus": hash_status,
            "OutputDeclared": output_decl,
            "OutputExists": output_exists,
            "StatusDeclared": status_decl,
            "RowGate": row_gate,
            "Notes": "; ".join(notes),
        })

    missing_phases = [n for n in range(1, 16) if phase_seen.get(n, 0) == 0]
    duplicate_phases = [n for n, count in phase_seen.items() if count > 1]

    if missing_phases:
        blocked = True
        result_rows.append({
            "Phase": "SUMMARY",
            "SourceDeclared": "",
            "SourceExists": "",
            "SourceHashDeclared": "",
            "SourceHashActual": "",
            "HashStatus": "",
            "OutputDeclared": "",
            "OutputExists": "",
            "StatusDeclared": "",
            "RowGate": "BLOCKED",
            "Notes": "Missing phases: " + ", ".join(f"{n:02d}" for n in missing_phases),
        })
    if duplicate_phases:
        blocked = True
        result_rows.append({
            "Phase": "SUMMARY",
            "SourceDeclared": "",
            "SourceExists": "",
            "SourceHashDeclared": "",
            "SourceHashActual": "",
            "HashStatus": "",
            "OutputDeclared": "",
            "OutputExists": "",
            "StatusDeclared": "",
            "RowGate": "BLOCKED",
            "Notes": "Duplicate phase entries: " + ", ".join(f"{n:02d}" for n in duplicate_phases),
        })

    gate = "BLOCKED_PHASE_MAPPING" if blocked else "PASS_PHASE_MAPPING"
    return result_rows, gate


# ---------------------------------------------------------------------
# REGISTER VALIDATION
# ---------------------------------------------------------------------

def validate_generic_register(role: str, path: Path | None, matches: list[Path]) -> dict[str, Any]:
    if not matches:
        return {
            "Register": role,
            "ExpectedFilename": CONTROL_FILENAMES[role],
            "Matches": 0,
            "SelectedPath": "",
            "Rows": "",
            "Columns": "",
            "Encoding": "",
            "Gate": "MISSING_CONTROL_FILE",
            "Notes": "",
        }

    if len(matches) > 1:
        hashes = {file_hash_or_error(p) for p in matches}
        return {
            "Register": role,
            "ExpectedFilename": CONTROL_FILENAMES[role],
            "Matches": len(matches),
            "SelectedPath": "",
            "Rows": "",
            "Columns": "",
            "Encoding": "",
            "Gate": "BLOCKED_MULTIPLE_CONTROL_FILES" if len(hashes) > 1 else "VERIFY_DUPLICATE_CONTROL_FILES",
            "Notes": "Multiple exact-name files found",
        }

    assert path is not None
    rows, headers, enc = read_csv_best_effort(path)
    if not headers:
        gate = "BLOCKED_UNREADABLE_CONTROL_FILE"
    elif not rows:
        gate = "BLOCKED_EMPTY_CONTROL_FILE"
    else:
        gate = "PASS_CONTROL_FILE_PRESENT"

    return {
        "Register": role,
        "ExpectedFilename": CONTROL_FILENAMES[role],
        "Matches": 1,
        "SelectedPath": str(path),
        "Rows": len(rows),
        "Columns": len(headers),
        "Encoding": enc,
        "Gate": gate,
        "Notes": "",
    }


# ---------------------------------------------------------------------
# LEGACY REGISTRY / CONTAMINATION SCAN
# ---------------------------------------------------------------------

def boolish(value: str, default: bool = False) -> bool:
    v = value.strip().lower()
    if not v:
        return default
    return v in {"1", "true", "yes", "y", "on", "enabled"}


def compile_legacy_patterns(path: Path) -> tuple[list[dict[str, Any]], str]:
    rows, headers, enc = read_csv_best_effort(path)
    if not headers:
        return [], "BLOCKED_UNREADABLE_RETIRED_DATA_REGISTRY"

    pattern_col = find_column(headers, [
        "Pattern", "RetiredValue", "LegacyToken", "SearchText", "Value"
    ])
    regex_col = find_column(headers, ["Regex", "IsRegex", "UseRegex"])
    enabled_col = find_column(headers, ["Enabled", "Active", "Use"])
    id_col = find_column(headers, ["ID", "LegacyID", "RetiredID", "Name"])
    reason_col = find_column(headers, ["Reason", "Description", "Notes"])

    if pattern_col is None:
        return [], "BLOCKED_RETIRED_REGISTRY_PATTERN_COLUMN_MISSING"

    patterns = []
    for idx, row in enumerate(rows, start=1):
        pattern = row.get(pattern_col, "").strip()
        if not pattern:
            continue
        enabled = boolish(row.get(enabled_col, ""), True) if enabled_col else True
        if not enabled:
            continue
        is_regex = boolish(row.get(regex_col, ""), False) if regex_col else False
        patterns.append({
            "RegistryRow": idx,
            "LegacyID": row.get(id_col, "") if id_col else f"ROW_{idx}",
            "Pattern": pattern,
            "IsRegex": is_regex,
            "Reason": row.get(reason_col, "") if reason_col else "",
        })

    if not patterns:
        return [], "BLOCKED_RETIRED_REGISTRY_NO_ACTIVE_PATTERNS"
    return patterns, "PASS_RETIRED_REGISTRY_LOADED"


def discover_legacy_scan_zones(current_core: Path | None) -> list[tuple[str, Path]]:
    zones: list[tuple[str, Path]] = []

    if current_core and current_core.exists():
        zones.append(("CURRENT_CORE", current_core))

    if RELEASE_CANDIDATE.exists():
        zones.append(("RELEASE_CANDIDATE", RELEASE_CANDIDATE))

    # Optional discovered production/final zones. Absence is reported, not treated
    # as a hard project-fact assumption.
    for p in ROOT.iterdir():
        if not p.is_dir():
            continue
        u = p.name.upper()
        if "PRODUCTION" in u and p != REPORT_DIR:
            zones.append(("PRODUCTION_DISCOVERED", p))
        elif "FINAL_RELEASE" in u and p != REPORT_DIR:
            zones.append(("FINAL_RELEASE_DISCOVERED", p))

    dedup = []
    seen = set()
    for label, p in zones:
        key = str(p).lower()
        if key not in seen:
            seen.add(key)
            dedup.append((label, p))
    return dedup


def scan_legacy_contamination(
    registry_path: Path | None,
    current_core: Path | None,
) -> tuple[list[dict[str, Any]], str, list[tuple[str, Path]]]:
    if registry_path is None or not registry_path.exists():
        return [], "BLOCKED_LEGACY_REGISTRY_MISSING", discover_legacy_scan_zones(current_core)

    patterns, registry_gate = compile_legacy_patterns(registry_path)
    zones = discover_legacy_scan_zones(current_core)
    if not registry_gate.startswith("PASS"):
        return [], registry_gate, zones

    rows = []
    for zone_label, zone_path in zones:
        for p in files_under(zone_path):
            if p.suffix.lower() not in TEXT_SCAN_EXTENSIONS:
                continue
            text, enc = read_text_best_effort(p)
            if text is None:
                rows.append({
                    "Zone": zone_label,
                    "Path": str(p),
                    "LegacyID": "",
                    "Pattern": "",
                    "MatchType": "",
                    "Line": "",
                    "Excerpt": "",
                    "Encoding": enc,
                    "Status": "UNREADABLE_TEXT_VERIFY",
                })
                continue

            for pat in patterns:
                pattern = pat["Pattern"]
                if pat["IsRegex"]:
                    try:
                        rx = re.compile(pattern, re.IGNORECASE)
                    except re.error as e:
                        rows.append({
                            "Zone": zone_label,
                            "Path": str(registry_path),
                            "LegacyID": pat["LegacyID"],
                            "Pattern": pattern,
                            "MatchType": "REGEX_ERROR",
                            "Line": "",
                            "Excerpt": str(e),
                            "Encoding": "",
                            "Status": "REGISTRY_PATTERN_ERROR",
                        })
                        continue

                    for line_no, line in enumerate(text.splitlines(), start=1):
                        if rx.search(line):
                            rows.append({
                                "Zone": zone_label,
                                "Path": str(p),
                                "LegacyID": pat["LegacyID"],
                                "Pattern": pattern,
                                "MatchType": "REGEX",
                                "Line": line_no,
                                "Excerpt": line.strip()[:500],
                                "Encoding": enc,
                                "Status": "LEGACY_PATTERN_FOUND",
                            })
                else:
                    needle = pattern.casefold()
                    for line_no, line in enumerate(text.splitlines(), start=1):
                        if needle in line.casefold():
                            rows.append({
                                "Zone": zone_label,
                                "Path": str(p),
                                "LegacyID": pat["LegacyID"],
                                "Pattern": pattern,
                                "MatchType": "LITERAL",
                                "Line": line_no,
                                "Excerpt": line.strip()[:500],
                                "Encoding": enc,
                                "Status": "LEGACY_PATTERN_FOUND",
                            })

    actual_findings = [r for r in rows if r["Status"] == "LEGACY_PATTERN_FOUND"]
    pattern_errors = [r for r in rows if r["Status"] == "REGISTRY_PATTERN_ERROR"]

    if pattern_errors:
        gate = "BLOCKED_LEGACY_REGISTRY_PATTERN_ERROR"
    elif actual_findings:
        gate = "BLOCKED_LEGACY_CONTAMINATION"
    else:
        gate = "PASS_LEGACY_SCAN_NO_MATCHES"

    return rows, gate, zones


# ---------------------------------------------------------------------
# ZIP / EMPTY SHELL
# ---------------------------------------------------------------------

def zip_status(path: Path) -> dict[str, Any]:
    result = {
        "Path": str(path),
        "Exists": path.exists(),
        "SizeBytes": path.stat().st_size if path.exists() else 0,
        "Open": False,
        "FileCount": "",
        "Status": "NOT_FOUND",
        "SHA256": "",
    }
    if not path.exists():
        return result
    result["SHA256"] = file_hash_or_error(path)
    try:
        with zipfile.ZipFile(path, "r") as zf:
            bad = zf.testzip()
            file_count = len([i for i in zf.infolist() if not i.is_dir()])
            result["Open"] = True
            result["FileCount"] = file_count
            if bad is not None:
                result["Status"] = f"CORRUPT_ENTRY:{bad}"
            elif file_count == 0:
                result["Status"] = "EMPTY_ZIP"
            else:
                result["Status"] = "PASS"
    except Exception as e:
        result["Status"] = f"FAIL:{e}"
    return result


# ---------------------------------------------------------------------
# GATE LOGIC
# ---------------------------------------------------------------------

def choose_system_gate(gates: dict[str, str]) -> str:
    # Highest-risk blocking conditions first.
    hash_gate = gates.get("HASH_GATE", "")
    source_gate = gates.get("SOURCE_GATE", "")
    core_gate = gates.get("CORE_GATE", "")
    phase_gate = gates.get("PHASE_GATE", "")
    register_gate = gates.get("REGISTER_GATE", "")
    legacy_gate = gates.get("LEGACY_GATE", "")
    release_gate = gates.get("RELEASE_GATE", "")

    if "CONFLICT" in hash_gate or "CONFLICT" in source_gate:
        return "BLOCKED_SOURCE_CONFLICT"
    if phase_gate.startswith("BLOCKED"):
        return "BLOCKED_PHASE_MAPPING"
    if register_gate.startswith("BLOCKED") or register_gate.startswith("MISSING"):
        return "BLOCKED_REGISTER"
    if legacy_gate.startswith("BLOCKED"):
        return legacy_gate
    if core_gate.startswith("BLOCKED"):
        return "BLOCKED_CURRENT_CORE"
    if release_gate.startswith("BLOCKED"):
        return "BLOCKED_RELEASE"
    return "READY_FOR_HUMAN_SOURCE_APPROVAL"


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

def main() -> int:
    if not ROOT.exists():
        print(f"STOP: ROOT NOT FOUND: {ROOT}")
        return 2

    REPORT_DIR.mkdir(parents=False, exist_ok=False)

    lines: list[str] = []
    def log(s: str = "") -> None:
        lines.append(s)
        print(s)

    log("AKK FULL SOURCE AUDIT — READ ONLY v2")
    log("FROM SOURCE / ZERO ASSUMPTION / DO NOT USE CHAT MEMORY")
    log(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    log("SOURCE MODE: READ ONLY")
    log("REPORT MODE: WRITE REPORTS ONLY")
    log("NO MOVE / NO COPY / NO RENAME / NO DELETE / NO BUILDER")
    log("")

    # ================================================================
    # 01 ROOT INVENTORY
    # ================================================================
    log("=== 01 ROOT INVENTORY ===")
    inventory_rows = []
    for p in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
        if p == REPORT_DIR:
            continue
        try:
            if p.is_dir():
                fs = files_under(p)
                ds = dirs_under(p)
                size = bytes_total(fs)
                row = {
                    "Type": "DIR",
                    "Name": p.name,
                    "Path": str(p),
                    "Files": len(fs),
                    "Folders": len(ds),
                    "SizeBytes": size,
                    "SizeMB": mb(size),
                    "SHA256": "",
                }
                log(f"DIR  | {p.name} | files={len(fs)} | folders={len(ds)} | sizeMB={mb(size)}")
            else:
                size = p.stat().st_size
                row = {
                    "Type": "FILE",
                    "Name": p.name,
                    "Path": str(p),
                    "Files": "",
                    "Folders": "",
                    "SizeBytes": size,
                    "SizeMB": mb(size),
                    "SHA256": file_hash_or_error(p),
                }
                log(f"FILE | {p.name} | size={size} bytes")
            inventory_rows.append(row)
        except Exception as e:
            log(f"INVENTORY ERROR | {p} | {e}")

    write_csv(
        OUT["ROOT_INVENTORY"],
        ["Type", "Name", "Path", "Files", "Folders", "SizeBytes", "SizeMB", "SHA256"],
        inventory_rows,
    )

    # ================================================================
    # 02 / 03 / 04 ROLE AUDITS
    # ================================================================
    log("")
    log("=== 02 CURRENT CORE RECOVERY AUDIT ===")
    current_core, current_core_existing = select_current_core_candidate()
    if current_core is None and len(current_core_existing) == 0:
        log("CURRENT CORE CANDIDATE: NOT FOUND")
    elif current_core is None:
        log("CURRENT CORE CANDIDATE: MULTIPLE CANDIDATES FOUND — HUMAN SELECTION REQUIRED")
        for p in current_core_existing:
            log(f"CANDIDATE | {p}")
    else:
        log(f"CURRENT CORE CANDIDATE: {current_core}")

    log("")
    log("=== 03 RELEASE CANDIDATE AUDIT ===")
    log(f"RELEASE CANDIDATE: {RELEASE_CANDIDATE}")

    log("")
    log("=== 04 ARCHIVE REFERENCE AUDIT ===")
    log(f"ARCHIVE REFERENCE: {ARCHIVE_REFERENCE}")

    role_rows = []
    role_specs = [
        ("CURRENT_CORE_CANDIDATE", current_core),
        ("RELEASE_CANDIDATE", RELEASE_CANDIDATE),
        ("ARCHIVE_REFERENCE", ARCHIVE_REFERENCE),
    ]
    for role, path in role_specs:
        if path is None:
            row = {
                "Role": role,
                "Path": "",
                "Exists": False,
                "Files": 0,
                "Folders": 0,
                "SizeBytes": 0,
                "SizeMB": 0,
                "Status": "NOT_SELECTED_OR_NOT_FOUND",
            }
        else:
            s = dir_summary(path)
            if not s["Exists"]:
                status = "NOT_FOUND"
            elif s["Files"] == 0:
                status = "EMPTY_SHELL"
            else:
                status = "NON_EMPTY"
            row = {"Role": role, **s, "Status": status}
        role_rows.append(row)
        log(
            f"{role} | exists={row['Exists']} | files={row['Files']} | "
            f"folders={row['Folders']} | sizeMB={row['SizeMB']} | status={row['Status']}"
        )

    write_csv(
        OUT["ROLE_SUMMARY"],
        ["Role", "Path", "Exists", "Files", "Folders", "SizeBytes", "SizeMB", "Status"],
        role_rows,
    )

    # ================================================================
    # 05 THREE-WAY HASH COMPARISON
    # ================================================================
    log("")
    log("=== 05 THREE-WAY HASH COMPARISON ===")
    recovery_map = build_role_map(current_core)
    release_map = build_role_map(RELEASE_CANDIDATE)
    archive_map = build_role_map(ARCHIVE_REFERENCE)

    three_way_rows = role_triplet_status(recovery_map, release_map, archive_map)
    write_csv(
        OUT["THREE_WAY"],
        [
            "RelativePath",
            "RecoveryPath", "RecoverySHA256",
            "ReleasePath", "ReleaseSHA256",
            "ArchivePath", "ArchiveSHA256",
            "Status", "HumanReviewRequired",
        ],
        three_way_rows,
    )

    three_way_conflicts = [
        r for r in three_way_rows
        if "CONFLICT" in r["Status"]
    ]
    log(f"THREE-WAY ROWS     : {len(three_way_rows)}")
    log(f"HASH CONFLICT ROWS : {len(three_way_conflicts)}")

    # ================================================================
    # GLOBAL FILE INDEX / DUPLICATES
    # ================================================================
    all_files = [
        p for p in ROOT.rglob("*")
        if p.is_file() and REPORT_DIR not in p.parents
    ]
    all_files = sorted(all_files, key=lambda p: str(p).lower())

    hash_to_paths: dict[str, list[Path]] = defaultdict(list)
    for p in all_files:
        h = file_hash_or_error(p)
        hash_to_paths[h].append(p)

    duplicate_rows = []
    duplicate_group_count = 0
    for h, paths in sorted(hash_to_paths.items()):
        if h.startswith("ERROR:"):
            continue
        if len(paths) > 1:
            duplicate_group_count += 1
            for p in paths:
                duplicate_rows.append({
                    "SHA256": h,
                    "Copies": len(paths),
                    "Path": str(p),
                    "RelativeToRoot": safe_rel(p, ROOT),
                })

    write_csv(
        OUT["DUPLICATES"],
        ["SHA256", "Copies", "Path", "RelativeToRoot"],
        duplicate_rows,
    )

    # Detailed relative-path conflicts across the three roles.
    conflict_rows = []
    for row in three_way_conflicts:
        conflict_rows.append({
            "RelativePath": row["RelativePath"],
            "RecoverySHA256": row["RecoverySHA256"],
            "ReleaseSHA256": row["ReleaseSHA256"],
            "ArchiveSHA256": row["ArchiveSHA256"],
            "Status": row["Status"],
            "Action": "VERIFY__DO_NOT_PROMOTE_AUTOMATICALLY",
        })

    write_csv(
        OUT["CONFLICTS"],
        ["RelativePath", "RecoverySHA256", "ReleaseSHA256", "ArchiveSHA256", "Status", "Action"],
        conflict_rows,
    )

    # ================================================================
    # 06 P1/P2/P3 CANDIDATE CLASSIFICATION
    # ================================================================
    log("")
    log("=== 06 P1/P2/P3 CANDIDATE CLASSIFICATION ===")
    classification_rows = []
    classification_scope: list[tuple[str, Path]] = []
    if current_core and current_core.exists():
        classification_scope.append(("CURRENT_CORE", current_core))
    if RELEASE_CANDIDATE.exists():
        classification_scope.append(("RELEASE_CANDIDATE", RELEASE_CANDIDATE))
    if ARCHIVE_REFERENCE.exists():
        classification_scope.append(("ARCHIVE_REFERENCE", ARCHIVE_REFERENCE))

    seen_class_paths = set()
    for role, base in classification_scope:
        for p in files_under(base):
            key = str(p).lower()
            if key in seen_class_paths:
                continue
            seen_class_paths.add(key)
            level, reason, status, human = suggest_source_level(p)
            classification_rows.append({
                "Role": role,
                "Path": str(p),
                "RelativePath": safe_rel(p, base),
                "CandidateLevel": level,
                "Reason": reason,
                "CurrentStatus": status,
                "HumanApprovalRequired": human,
                "SHA256": file_hash_or_error(p),
            })

    write_csv(
        OUT["SOURCE_CLASSIFICATION"],
        [
            "Role", "Path", "RelativePath", "CandidateLevel", "Reason",
            "CurrentStatus", "HumanApprovalRequired", "SHA256"
        ],
        classification_rows,
    )
    p1_candidates = [r for r in classification_rows if r["CandidateLevel"] == "P1_CANDIDATE"]
    log(f"P1 CANDIDATES: {len(p1_candidates)}")
    log("NOTE: P1 classification is suggestion only; no automatic approval.")

    # ================================================================
    # 07 NATIVE SOURCE DETECTION
    # ================================================================
    log("")
    log("=== 07 NATIVE CAD / NATIVE SOURCE DETECTION ===")
    native_rows = []
    for p in all_files:
        if p.suffix.lower() in NATIVE_EXTENSIONS:
            native_rows.append({
                "Extension": p.suffix.lower(),
                "Path": str(p),
                "SizeBytes": p.stat().st_size,
                "SHA256": file_hash_or_error(p),
                "Status": "FOUND_VERIFY_AUTHORITY",
            })

    if not native_rows:
        native_rows.append({
            "Extension": "",
            "Path": "",
            "SizeBytes": "",
            "SHA256": "",
            "Status": "NOT_FOUND / VERIFY",
        })
        log("NATIVE SOURCE: NOT_FOUND / VERIFY")
    else:
        log(f"NATIVE SOURCE FILES FOUND: {len(native_rows)}")

    write_csv(
        OUT["NATIVE_SCAN"],
        ["Extension", "Path", "SizeBytes", "SHA256", "Status"],
        native_rows,
    )

    # ================================================================
    # 08 CONTROL FILE DETECTION
    # ================================================================
    log("")
    log("=== 08 CONTROL FILE DETECTION ===")
    control_matches: dict[str, list[Path]] = {}
    selected_control: dict[str, Path | None] = {}
    control_status_rows = []

    for role, filename in CONTROL_FILENAMES.items():
        matches = discover_exact_filename(filename)
        control_matches[role] = matches
        selected_control[role] = matches[0] if len(matches) == 1 else None
        hashes = sorted({file_hash_or_error(p) for p in matches}) if matches else []
        if not matches:
            status = "MISSING CONTROL FILE"
        elif len(matches) == 1:
            status = "FOUND"
        elif len(hashes) == 1:
            status = "MULTIPLE BYTE-IDENTICAL COPIES / VERIFY"
        else:
            status = "MULTIPLE DIFFERENT COPIES / BLOCKED"
        control_status_rows.append({
            "ControlRole": role,
            "ExpectedFilename": filename,
            "Matches": len(matches),
            "SelectedPath": str(selected_control[role]) if selected_control[role] else "",
            "UniqueHashes": len(hashes),
            "Status": status,
            "MatchPaths": " | ".join(str(p) for p in matches),
        })
        log(f"{role} | matches={len(matches)} | status={status}")

    write_csv(
        OUT["CONTROL_STATUS"],
        ["ControlRole", "ExpectedFilename", "Matches", "SelectedPath", "UniqueHashes", "Status", "MatchPaths"],
        control_status_rows,
    )

    # ================================================================
    # 09 PHASE MAP VALIDATION
    # ================================================================
    log("")
    log("=== 09 PHASE MAP VALIDATION ===")
    phase_map_path = selected_control["PHASE_MAP"]
    if phase_map_path is None:
        phase_rows = [{
            "Phase": "",
            "SourceDeclared": "",
            "SourceExists": "",
            "SourceHashDeclared": "",
            "SourceHashActual": "",
            "HashStatus": "",
            "OutputDeclared": "",
            "OutputExists": "",
            "StatusDeclared": "",
            "RowGate": "MISSING_CONTROL_FILE",
            "Notes": CONTROL_FILENAMES["PHASE_MAP"],
        }]
        phase_gate = "BLOCKED_PHASE_MAPPING"
    else:
        phase_rows, phase_gate = validate_phase_map(phase_map_path)

    write_csv(
        OUT["PHASE_VALIDATION"],
        [
            "Phase", "SourceDeclared", "SourceExists",
            "SourceHashDeclared", "SourceHashActual", "HashStatus",
            "OutputDeclared", "OutputExists", "StatusDeclared",
            "RowGate", "Notes",
        ],
        phase_rows,
    )
    log(f"PHASE_MAPPING_GATE = {phase_gate}")

    # ================================================================
    # 10 REGISTER VALIDATION
    # ================================================================
    log("")
    log("=== 10 REGISTER VALIDATION ===")
    register_rows = []
    register_gates = []

    for role in ("SOURCE_REGISTER", "PHASE_MAP", "ASSET_REGISTER"):
        matches = control_matches[role]
        selected = selected_control[role]
        row = validate_generic_register(role, selected, matches)
        register_rows.append(row)
        register_gates.append(row["Gate"])
        log(f"{role} | gate={row['Gate']}")

    write_csv(
        OUT["REGISTER_VALIDATION"],
        ["Register", "ExpectedFilename", "Matches", "SelectedPath", "Rows", "Columns", "Encoding", "Gate", "Notes"],
        register_rows,
    )

    if any(g == "MISSING_CONTROL_FILE" for g in register_gates):
        register_gate = "BLOCKED_MISSING_CONTROL_FILE"
    elif any(g.startswith("BLOCKED") for g in register_gates):
        register_gate = "BLOCKED_REGISTER_VALIDATION"
    elif any(g.startswith("VERIFY") for g in register_gates):
        register_gate = "BLOCKED_REGISTER_DUPLICATE_REVIEW"
    else:
        register_gate = "PASS_REGISTERS_PRESENT_AND_READABLE"

    # ================================================================
    # 11 DUPLICATE / CONFLICT
    # ================================================================
    log("")
    log("=== 11 DUPLICATE / CONFLICT REVIEW ===")
    log(f"FILES HASHED          : {len(all_files)}")
    log(f"DUPLICATE GROUPS      : {duplicate_group_count}")
    log(f"THREE-WAY CONFLICTS   : {len(three_way_conflicts)}")

    # ================================================================
    # 12 LEGACY CONTAMINATION SCAN
    # ================================================================
    log("")
    log("=== 12 LEGACY CONTAMINATION SCAN ===")
    retired_registry = selected_control["RETIRED_DATA_REGISTRY"]
    legacy_rows, legacy_gate, legacy_zones = scan_legacy_contamination(
        retired_registry,
        current_core,
    )

    if not legacy_rows:
        # Still write one status row so the CSV is self-explanatory.
        legacy_rows = [{
            "Zone": "",
            "Path": "",
            "LegacyID": "",
            "Pattern": "",
            "MatchType": "",
            "Line": "",
            "Excerpt": "",
            "Encoding": "",
            "Status": legacy_gate,
        }]

    write_csv(
        OUT["LEGACY"],
        ["Zone", "Path", "LegacyID", "Pattern", "MatchType", "Line", "Excerpt", "Encoding", "Status"],
        legacy_rows,
    )

    log(f"LEGACY_GATE = {legacy_gate}")
    for label, p in legacy_zones:
        log(f"LEGACY SCAN ZONE | {label} | {p}")

    # ================================================================
    # 13 ZIP INTEGRITY
    # ================================================================
    log("")
    log("=== 13 ZIP INTEGRITY ===")
    zip_rows = []
    for p in all_files:
        if p.suffix.lower() == ".zip":
            z = zip_status(p)
            zip_rows.append(z)
            log(
                f"ZIP | {p} | files={z['FileCount']} | status={z['Status']} | "
                f"size={z['SizeBytes']}"
            )

    if not zip_rows:
        zip_rows.append({
            "Path": "",
            "Exists": False,
            "SizeBytes": 0,
            "Open": False,
            "FileCount": "",
            "Status": "NO_ZIP_FOUND",
            "SHA256": "",
        })

    write_csv(
        OUT["ZIP"],
        ["Path", "Exists", "SizeBytes", "Open", "FileCount", "Status", "SHA256"],
        zip_rows,
    )

    # ================================================================
    # 14 EMPTY SHELL DETECTION
    # ================================================================
    log("")
    log("=== 14 EMPTY SHELL DETECTION ===")
    empty_rows = []
    for d in dirs_under(ROOT):
        try:
            children = list(d.iterdir())
            if not children:
                empty_rows.append({
                    "Path": str(d),
                    "Type": "EMPTY_DIRECTORY",
                    "Files": 0,
                    "Folders": 0,
                    "Status": "VERIFY",
                })
                continue

            # Empty shell = may contain folders but zero files recursively.
            fs = files_under(d)
            ds = dirs_under(d)
            if len(fs) == 0 and len(ds) > 0:
                empty_rows.append({
                    "Path": str(d),
                    "Type": "EMPTY_SHELL_TREE",
                    "Files": 0,
                    "Folders": len(ds),
                    "Status": "VERIFY",
                })
        except Exception:
            continue

    if not empty_rows:
        empty_rows.append({
            "Path": "",
            "Type": "",
            "Files": "",
            "Folders": "",
            "Status": "NO_EMPTY_SHELL_FOUND",
        })

    write_csv(
        OUT["EMPTY"],
        ["Path", "Type", "Files", "Folders", "Status"],
        empty_rows,
    )
    log(f"EMPTY/SHELL ROWS: {len([r for r in empty_rows if r['Path']])}")

    # ================================================================
    # 15 MULTI-GATE SUMMARY
    # ================================================================
    log("")
    log("=== 15 MULTI-GATE SUMMARY ===")

    # SOURCE_GATE
    if not p1_candidates:
        source_gate = "BLOCKED_NO_P1_SOURCE_CANDIDATES"
    elif control_matches["SOURCE_REGISTER"] and len(control_matches["SOURCE_REGISTER"]) > 1:
        source_gate = "BLOCKED_SOURCE_REGISTER_CONFLICT_OR_DUPLICATE"
    else:
        source_gate = "READY_FOR_HUMAN_SOURCE_APPROVAL"

    # CORE_GATE
    if len(current_core_existing) == 0:
        core_gate = "BLOCKED_CURRENT_CORE_CANDIDATE_NOT_FOUND"
    elif len(current_core_existing) > 1:
        core_gate = "BLOCKED_MULTIPLE_CURRENT_CORE_CANDIDATES"
    elif current_core and len(recovery_map) == 0:
        core_gate = "BLOCKED_CURRENT_CORE_EMPTY"
    else:
        recovery_archive_rows = [
            r for r in three_way_rows
            if r["RecoveryPath"] or r["ArchivePath"]
        ]
        ra_conflicts = [
            r for r in recovery_archive_rows
            if r["RecoveryPath"] and r["ArchivePath"]
            and r["RecoverySHA256"] != r["ArchiveSHA256"]
        ]
        archive_missing_in_recovery = [
            r for r in recovery_archive_rows
            if r["ArchivePath"] and not r["RecoveryPath"]
        ]
        recovery_extra_vs_archive = [
            r for r in recovery_archive_rows
            if r["RecoveryPath"] and not r["ArchivePath"]
        ]
        if ra_conflicts:
            core_gate = "BLOCKED_CURRENT_CORE_ARCHIVE_HASH_CONFLICT"
        elif archive_missing_in_recovery or recovery_extra_vs_archive:
            core_gate = "BLOCKED_CURRENT_CORE_ARCHIVE_STRUCTURE_MISMATCH"
        else:
            core_gate = "PASS_CURRENT_CORE_MATCHES_ARCHIVE_REFERENCE"

    # HASH_GATE
    hash_gate = (
        "BLOCKED_HASH_CONFLICT"
        if three_way_conflicts
        else "PASS_NO_THREE_WAY_HASH_CONFLICT"
    )

    # RELEASE_GATE
    release_summary = dir_summary(RELEASE_CANDIDATE)
    if not release_summary["Exists"]:
        release_gate = "BLOCKED_RELEASE_CANDIDATE_NOT_FOUND"
    elif release_summary["Files"] == 0:
        release_gate = "BLOCKED_RELEASE_CANDIDATE_EMPTY"
    elif current_core is None:
        release_gate = "BLOCKED_RELEASE_REQUIRES_CURRENT_CORE_SELECTION"
    else:
        rl_rows = [r for r in three_way_rows if r["RecoveryPath"] or r["ReleasePath"]]
        rl_conflicts = [
            r for r in rl_rows
            if r["RecoveryPath"] and r["ReleasePath"]
            and r["RecoverySHA256"] != r["ReleaseSHA256"]
        ]
        rl_missing = [
            r for r in rl_rows
            if bool(r["RecoveryPath"]) != bool(r["ReleasePath"])
        ]
        if rl_conflicts:
            release_gate = "BLOCKED_RELEASE_HASH_CONFLICT"
        elif rl_missing:
            release_gate = "BLOCKED_RELEASE_STRUCTURE_MISMATCH"
        else:
            release_gate = "PASS_RELEASE_MATCHES_CURRENT_CORE"

    gates = {
        "SOURCE_GATE": source_gate,
        "CORE_GATE": core_gate,
        "PHASE_GATE": phase_gate,
        "REGISTER_GATE": register_gate,
        "HASH_GATE": hash_gate,
        "LEGACY_GATE": legacy_gate,
        "RELEASE_GATE": release_gate,
    }
    system_gate = choose_system_gate(gates)
    gates["AKK_SYSTEM_GATE"] = system_gate

    gate_rows = []
    for name, value in gates.items():
        gate_rows.append({
            "Gate": name,
            "Result": value,
            "HumanApprovalRequired": "YES",
        })
        log(f"{name} = {value}")

    write_csv(
        OUT["GATES"],
        ["Gate", "Result", "HumanApprovalRequired"],
        gate_rows,
    )

    log("")
    log("FINAL:")
    log(f"AKK_SYSTEM_GATE = {system_gate}")
    log("")
    log("IMPORTANT:")
    log("- This audit does not approve P1.")
    log("- This audit does not authorize MOVE / DELETE / BUILDER.")
    log("- Native source NOT_FOUND is reported as NOT_FOUND / VERIFY, not auto-MISSING.")
    log("- Legacy scan is driven only by AKK_RETIRED_DATA_REGISTRY.csv.")
    log("- Source Ready remains a human-governed gate.")

    # Write final TXT last.
    OUT["TXT"].write_text("\n".join(lines), encoding="utf-8-sig")

    print("")
    print("REPORT DIRECTORY:")
    print(REPORT_DIR)
    print("")
    print("PRIMARY REPORT:")
    print(OUT["TXT"])
    print("")
    print("ALL REPORTS:")
    for key, path in OUT.items():
        print(f"{key}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
