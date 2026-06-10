from __future__ import annotations

import json
from pathlib import Path


def test_all_smoke_rdf_artifacts_have_ttl_equivalent() -> None:
    cases_dir = Path("tests/smoke/cases")
    rdf_paths = sorted(cases_dir.glob("*/artifacts/observed_*_output.rdf"))
    assert rdf_paths, "smoke suite should generate RDF artifacts before TTL audit"

    missing: list[str] = []
    empty: list[str] = []
    metric_failures: list[str] = []
    for rdf_path in rdf_paths:
        ttl_path = rdf_path.with_suffix(".ttl")
        if not ttl_path.exists():
            missing.append(str(ttl_path))
            continue
        ttl_text = ttl_path.read_text(encoding="utf-8")
        if not ttl_text.strip():
            empty.append(str(ttl_path))
        case_id = rdf_path.name.removeprefix("observed_").removesuffix("_output.rdf")
        metrics_path = rdf_path.with_name(f"observed_{case_id}_metrics.json")
        if metrics_path.exists():
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            if not metrics.get("ttl_generated") or metrics.get("ttl_bytes", 0) <= 0:
                metric_failures.append(str(metrics_path))

    assert not missing, "missing TTL artifacts: " + ", ".join(missing)
    assert not empty, "empty TTL artifacts: " + ", ".join(empty)
    assert not metric_failures, "metrics missing TTL generation flags: " + ", ".join(metric_failures)
