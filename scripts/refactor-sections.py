#!/usr/bin/env python3
"""
Refactor events.json: add sections (BCE Option A + CE centuries), assign each event
to a section, move duplicate timeline_sources to sections, keep per-event sources when different.
Then run build-hierarchy to generate recursive hierarchy from source headers.
"""
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
EVENTS_JSON = os.path.join(REPO_DIR, "data", "events.json")

BCE_SOURCES = [
    "Saturnian",
    "Jno Cook",
    "N. A. Morozov",
    "Immanuel Velikovsky",
    "David Talbott",
]
CE_CHRONOLOGY_SOURCES = ["Saturnian", "Fomenko"]

SECTIONS = [
    # BCE Option A
    {"id": "before-creation", "name": "Before Creation", "era": "BCE", "start": -5000, "end": -4078, "timeline_sources": BCE_SOURCES},
    {"id": "golden-age", "name": "The Golden Age", "era": "BCE", "start": -4077, "end": -3148, "timeline_sources": BCE_SOURCES},
    {"id": "dark-ages", "name": "The Dark Ages", "era": "BCE", "start": -3147, "end": -687, "timeline_sources": BCE_SOURCES},
    {"id": "iron-age-blip", "name": "Iron Age / The Blip", "era": "BCE", "start": -686, "end": -1, "timeline_sources": BCE_SOURCES},
    # CE centuries (chronology page)
    {"id": "11th-century", "name": "11th Century C.E. Common Era Begins", "era": "CE", "start": 1000, "end": 1099, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "12th-century", "name": "12th Century C.E. Birth of Christianity", "era": "CE", "start": 1100, "end": 1199, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "13th-century", "name": "13th Century C.E. Russian Horde Tartarian Empire", "era": "CE", "start": 1200, "end": 1299, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "14th-century", "name": "14th Century C.E. Mongol Slavic Rus-Horde Expansion", "era": "CE", "start": 1300, "end": 1399, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "15th-century", "name": "15th Century C.E. Ottoman Conquest of Europe", "era": "CE", "start": 1400, "end": 1499, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "16th-century", "name": "16th Century C.E. Reformation and Inquisition", "era": "CE", "start": 1500, "end": 1599, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "17th-century", "name": "17th Century C.E. Romanovs Rise to Power", "era": "CE", "start": 1600, "end": 1699, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "18th-century", "name": "18th Century C.E. MudFlood and Pugachev", "era": "CE", "start": 1700, "end": 1799, "timeline_sources": CE_CHRONOLOGY_SOURCES},
    {"id": "19th-century", "name": "19th Century C.E.", "era": "CE", "start": 1800, "end": 1999, "timeline_sources": CE_CHRONOLOGY_SOURCES},
]


def section_for_year(year):
    """Return section id for a given year (negative = BCE)."""
    for s in SECTIONS:
        if s["era"] == "BCE" and year < 0:
            if s["start"] <= year <= s["end"]:
                return s["id"]
        elif s["era"] == "CE" and year >= 0:
            if s["start"] <= year <= s["end"]:
                return s["id"]
    return SECTIONS[0]["id"]


def main():
    with open(EVENTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = data["events"]
    section_sources = {s["id"]: s["timeline_sources"] for s in SECTIONS}

    section_by_id = {s["id"]: s for s in SECTIONS}

    for evt in events:
        if not evt.get("dates"):
            continue
        d = evt["dates"][0]
        year = d.get("start", d.get("value", 0))
        if "value" in d:
            d["start"] = d.pop("value")
        section_id = section_for_year(year)
        evt["section"] = section_id
        sec = section_by_id.get(section_id)
        for d in evt["dates"]:
            if "value" in d:
                d["start"] = d.pop("value")
            if "end" not in d and sec:
                d["end"] = sec["end"]

        sources = evt.get("timeline_sources")
        default_sources = section_sources.get(section_id, CE_CHRONOLOGY_SOURCES)
        if sources is None or sources == default_sources or sources == []:
            if "timeline_sources" in evt:
                del evt["timeline_sources"]
        else:
            evt["timeline_sources"] = sources

    data["sections"] = SECTIONS
    data["meta"] = data.get("meta", {})
    data["meta"]["source"] = "refactor-sections.py"

    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Refactored {len(events)} events into {len(SECTIONS)} sections")
    for s in SECTIONS:
        count = sum(1 for e in events if e.get("section") == s["id"])
        overrides = sum(1 for e in events if e.get("section") == s["id"] and "timeline_sources" in e)
        print(f"  {s['id']}: {count} events, {overrides} with per-event sources")

    subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "build-hierarchy.py")],
        check=True,
    )


if __name__ == "__main__":
    main()
