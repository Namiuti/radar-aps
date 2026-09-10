#!/usr/bin/env python3
"""Build a small public summary from downloaded official metadata."""
from __future__ import annotations

import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "site" / "data" / "summary.json"


def load(name):
    with (RAW / name).open(encoding="utf-8") as f:
        return json.load(f)


def rows(payload):
    if isinstance(payload, list):
        return payload
    for value in payload.values():
        if isinstance(value, list):
            return value
    return []


def main():
    regions = rows(load("health_regions.json"))
    ubs = rows(load("ubs.json"))
    municipalities = load("ibge_municipios.json")
    cnes = rows(load("cnes_estabelecimentos_sample.json"))
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {
            "ibge_municipios": {"count": len(municipalities), "status": "observed"},
            "health_regions": {"count": len(regions), "status": "observed"},
            "ubs": {"count": len(ubs), "status": "sample"},
            "cnes_estabelecimentos": {"count": len(cnes), "status": "sample"},
            "icsap": {"count": None, "status": "pending_official_sih_validation"},
        },
        "method": "Metadata territorial e assistencial coletados de APIs oficiais; ICSAP não é inferido.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
