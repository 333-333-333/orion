from __future__ import annotations

import json
import os
import re
import select
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_RUNNER_LOG = Path("tests/smoke/artifacts/infosec_smoke_runner.jsonl")
_TEST_LINE = re.compile(r"^(?P<test>tests/[^\s]+)(?:\s+(?P<progress>.*))?$")
_DEFAULT_TIMEOUT_SECONDS = 300.0
_HEARTBEAT_SECONDS = 15.0
_SMOKE_TESTS = (
    "tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_canonical_claims_red_smoke.py",
    "tests/smoke/cases/infosec_p001_p002/test_infosec_p001_p002_modular_contract_smoke.py",
    "tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_semantic_claims_smoke.py",
    "tests/smoke/cases/infosec_p003_p004/test_infosec_p003_p004_canonical_rdf_smoke.py",
    "tests/smoke/cases/infosec_p005_p006/test_infosec_p005_p006_observational_smoke.py",
    "tests/smoke/cases/infosec_p007_p008/test_infosec_p007_p008_observational_smoke.py",
    "tests/smoke/cases/infosec_p009_p010/test_infosec_p009_p010_observational_smoke.py",
    "tests/smoke/cases/infosec_p011_p012/test_infosec_p011_p012_observational_smoke.py",
    "tests/smoke/cases/infosec_p013_p014/test_infosec_p013_p014_observational_smoke.py",
    "tests/smoke/cases/infosec_p015_p016/test_infosec_p015_p016_observational_smoke.py",
    "tests/smoke/cases/infosec_p017_p018/test_infosec_p017_p018_observational_smoke.py",
    "tests/smoke/cases/infosec_p019_p020/test_infosec_p019_p020_observational_smoke.py",
    "tests/smoke/cases/infosec_p021_p022/test_infosec_p021_p022_observational_smoke.py",
    "tests/smoke/cases/infosec_p023_p024/test_infosec_p023_p024_observational_smoke.py",
    "tests/smoke/cases/infosec_p025_p026/test_infosec_p025_p026_observational_smoke.py",
    "tests/smoke/cases/infosec_p027_p028/test_infosec_p027_p028_observational_smoke.py",
    "tests/smoke/cases/infosec_p029_p030/test_infosec_p029_p030_observational_smoke.py",
    "tests/smoke/cases/infosec_p031_p032/test_infosec_p031_p032_observational_smoke.py",
    "tests/smoke/cases/infosec_p033_p034/test_infosec_p033_p034_observational_smoke.py",
    "tests/smoke/cases/infosec_p035_p036/test_infosec_p035_p036_observational_smoke.py",
    "tests/smoke/cases/infosec_p037_p038/test_infosec_p037_p038_observational_smoke.py",
    "tests/smoke/cases/infosec_p039_p040/test_infosec_p039_p040_observational_smoke.py",
    "tests/smoke/cases/infosec_p041_p042/test_infosec_p041_p042_observational_smoke.py",
    "tests/smoke/cases/infosec_p043/test_infosec_p043_observational_smoke.py",
    "tests/smoke/cases/infosec_full_text/test_infosec_full_text_observational_smoke.py",
)
_DISABLED_INFOSEC_3K_SMOKE_TESTS = (
    "tests/smoke/test_infosec_3k_pipeline_smoke.py",
    "tests/smoke/test_infosec_3k_paragraphs_smoke.py",
    "tests/smoke/test_infosec_paragraph_semantics_smoke.py",
)
_INFOSEC_3K_DENYLIST = ("infosec_3k", "3k_pipeline", "3k_paragraphs")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _json_event(
    *,
    event: str,
    status: str,
    message: str,
    phase: str = "smoke_runner",
    test: str | None = None,
    duration: float | None = None,
    error: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "timestamp": _timestamp(),
        "event": event,
        "status": status,
        "message": message,
        "phase": phase,
    }
    if test:
        payload["test"] = test
    if duration is not None:
        payload["duration"] = round(duration, 3)
    if error is not None:
        payload["error"] = error
    if metadata is not None:
        payload["metadata"] = metadata
    return payload


def _emit(payload: dict[str, Any]) -> None:
    line = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    print(line, flush=True)
    _RUNNER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with _RUNNER_LOG.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def _line_event(line: str) -> dict[str, Any]:
    stripped = line.rstrip("\n")
    match = _TEST_LINE.match(stripped)
    test = match.group("test") if match else None
    progress = match.group("progress") if match else None
    lower = stripped.lower()
    status = "info"
    pytest_status = None
    if " failures " in lower or stripped.startswith("FAILED ") or " failed " in lower:
        status = "failed"
        pytest_status = "failed"
    elif " passed" in lower or " passed " in lower or stripped.endswith(" PASSED"):
        status = "passed"
        pytest_status = "passed"
    elif " skipped" in lower:
        status = "skipped"
        pytest_status = "skipped"
    elif " short test summary " in lower:
        status = "summary"
        pytest_status = "summary"
    metadata = {"progress": progress} if progress else None
    if pytest_status:
        metadata = metadata or {}
        metadata["pytest_status"] = pytest_status
    return _json_event(
        event="pytest_output",
        status=status,
        message=stripped,
        phase="pytest",
        test=test,
        metadata=metadata,
    )


def _timeout_seconds() -> float:
    raw = os.environ.get("ORION_SMOKE_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return _DEFAULT_TIMEOUT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return _DEFAULT_TIMEOUT_SECONDS
    return max(1.0, value)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    log_path = repo_root / _RUNNER_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("", encoding="utf-8")

    selected_tests = list(_SMOKE_TESTS)
    blocked_tests = [
        test
        for test in selected_tests
        if any(blocked in test for blocked in _INFOSEC_3K_DENYLIST)
    ]
    if blocked_tests:
        _emit(_json_event(
            event="runner_blocked",
            status="failed",
            message="infosec 3k smoke scope is disabled and must not execute",
            error={"blocked_tests": blocked_tests},
            metadata={"selected_tests": selected_tests},
        ))
        return 125

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-vv",
        "-ra",
        *selected_tests,
    ]
    if os.environ.get("ORION_SMOKE_FAILFAST", "").strip().lower() in {"1", "true", "yes", "on"}:
        cmd.insert(3, "-x")

    timeout_seconds = _timeout_seconds()
    started = time.monotonic()
    last_output = started
    last_heartbeat = started
    last_test: str | None = None
    _emit(_json_event(
        event="runner_started",
        status="started",
        message="starting smoke suite with infosec 3k disabled",
        duration=0.0,
        metadata={
            "command": cmd,
            "timeout_seconds": timeout_seconds,
            "selected_tests": selected_tests,
            "disabled_infosec_3k_tests": list(_DISABLED_INFOSEC_3K_SMOKE_TESTS),
        },
    ))

    process = subprocess.Popen(
        cmd,
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    assert process.stdout is not None
    while True:
        ready, _, _ = select.select([process.stdout], [], [], 0.2)
        now = time.monotonic()
        if ready:
            line = process.stdout.readline()
            if line:
                event = _line_event(line)
                if event.get("test"):
                    last_test = str(event["test"])
                last_output = now
                _emit(event)
                continue

        returncode = process.poll()
        if returncode is not None:
            for line in process.stdout:
                event = _line_event(line)
                if event.get("test"):
                    last_test = str(event["test"])
                _emit(event)
            break

        duration = now - started
        if duration >= timeout_seconds:
            process.kill()
            returncode = process.wait()
            _emit(_json_event(
                event="runner_timeout",
                status="failed",
                message="smoke suite exceeded timeout",
                duration=duration,
                error={"returncode": returncode, "timeout_seconds": timeout_seconds},
                metadata={"last_test": last_test, "seconds_since_output": round(now - last_output, 3)},
            ))
            _emit(_json_event(
                event="runner_completed",
                status="failed",
                message="smoke suite completed after timeout",
                duration=time.monotonic() - started,
                error={"returncode": returncode, "timeout_seconds": timeout_seconds},
            ))
            return 124

        if now - last_heartbeat >= _HEARTBEAT_SECONDS:
            last_heartbeat = now
            _emit(_json_event(
                event="runner_heartbeat",
                status="running",
                message="smoke suite still running",
                duration=duration,
                metadata={"last_test": last_test, "seconds_since_output": round(now - last_output, 3)},
            ))

        time.sleep(0.2)

    duration = time.monotonic() - started
    status = "passed" if returncode == 0 else "failed"
    error = None if returncode == 0 else {"returncode": returncode}
    _emit(
        _json_event(
            event="runner_completed",
            status=status,
            message="smoke suite completed",
            duration=duration,
            error=error,
        )
    )
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
