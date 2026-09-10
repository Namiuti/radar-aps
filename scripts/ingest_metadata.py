#!/usr/bin/env python3
"""Download official territorial and CNES metadata for Radar APS."""
from __future__ import annotations

import argparse
import gzip
import json
import pathlib
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

UA = "RadarAPS/0.1 (+public-health-open-data)"
MS_API = "https://apidadosabertos.saude.gov.br"
IBGE_API = "https://servicodados.ibge.gov.br/api/v1"


def get_json(url: str):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urlopen(req, timeout=60) as response:
        body = response.read()
        if body[:2] == b"\x1f\x8b":
            body = gzip.decompress(body)
        return json.loads(body)


def paginated(path: str, limit: int = 100, max_pages: int = 3):
    rows = []
    for offset in range(0, limit * max_pages, limit):
        url = f"{MS_API}{path}?{urlencode({'limit': limit, 'offset': offset})}"
        payload = get_json(url)
        page = payload if isinstance(payload, list) else payload.get("data", payload.get("items", next((v for v in payload.values() if isinstance(v, list)), [])))
        if not isinstance(page, list):
            raise ValueError(f"Formato inesperado em {url}")
        rows.extend(page)
        if len(page) < limit:
            break
    return rows


def write_json(path: pathlib.Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw")
    args = parser.parse_args()
    output = pathlib.Path(args.output)
    collected_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    sources = {}

    jobs = {
        "health_regions.json": f"{MS_API}/macrorregiao-e-regiao-de-saude/municipio?limit=860&offset=0",
        "ubs.json": f"{MS_API}/assistencia-a-saude/unidade-basicas-de-saude?limit=1000&offset=0",
        "ibge_municipios.json": f"{IBGE_API}/localidades/municipios?orderBy=nome",
    }
    for filename, url in jobs.items():
        payload = get_json(url)
        write_json(output / filename, payload)
        sources[filename] = {"url": url, "collected_at": collected_at}

    # The full CNES endpoint is paginated and intentionally limited in this first ingest.
    cnes = paginated("/cnes/estabelecimentos", limit=20, max_pages=3)
    write_json(output / "cnes_estabelecimentos_sample.json", cnes)
    sources["cnes_estabelecimentos_sample.json"] = {
        "url": f"{MS_API}/cnes/estabelecimentos",
        "collected_at": collected_at,
        "note": "first 60 records only; production ingest must paginate completely",
    }
    write_json(output / "manifest.json", {"collected_at": collected_at, "sources": sources})
    print(json.dumps({"files": list(sources), "collected_at": collected_at}, ensure_ascii=False))


if __name__ == "__main__":
    main()
