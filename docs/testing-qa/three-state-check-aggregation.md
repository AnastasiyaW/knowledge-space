---
title: "Three-State Check Aggregation"
description: "PASS / FAIL / UNKNOWN instead of pass-fail: exit-code contracts, fail-closed aggregation, absence-of-signal alarms, and why grepping prose for a verdict eventually reports green on a red system."
---

# Three-State Check Aggregation

A checking mechanism must distinguish three outcomes, not two. Collapsing the third into
the first is the defect: **absence of signal becomes indistinguishable from health**, and
the error always lands on the dangerous side, because an unrun check looks exactly like an
absent failure.

| State | Meaning | Consumer action |
|---|---|---|
| `PASS` | Ran, matched expectation | Proceed |
| `FAIL` | Ran, did not match | Fix the system |
| `UNKNOWN` | **Did not run, or could not decide** | Not green. Find out why it did not run |

## Exit-code contract

The machine channel is the exit status. Printed text is for humans and drifts the moment
somebody rewords a message.

```python
# Convention, declared in a manifest - never guessed by the consumer.
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_UNKNOWN = 2   # could not run: missing dependency, no credentials, target unreachable
```

```python
import sys

def main() -> int:
    if not tool_available():
        print("check NOT performed (this is not a success): tool missing")
        return EXIT_UNKNOWN
    return EXIT_PASS if probe_matches() else EXIT_FAIL

if __name__ == "__main__":
    sys.exit(main())   # never `main()` alone - a falling-off-the-end return of None exits 0
```

The `UNKNOWN` code must be **declared**, not sniffed. A consumer that infers "2 probably
means skipped" is doing prose-grepping with extra steps. Put it in the manifest the
aggregator reads:

```json
{
  "checks": [
    {"id": "schema", "cmd": ["python", "checks/schema.py"], "timeout_sec": 120},
    {"id": "smoke",  "cmd": ["python", "checks/smoke.py"],  "timeout_sec": 300}
  ],
  "unknown_exit_codes": [2]
}
```

## Fail-closed aggregation

Green is emitted only when **every** expected check ran and passed. One `UNKNOWN` is enough
to withhold green. A result that never arrived is `UNKNOWN`, not "nothing to report".

```python
import json, subprocess

def run_check(spec, unknown_codes):
    try:
        proc = subprocess.run(spec["cmd"], capture_output=True, text=True,
                              timeout=spec.get("timeout_sec", 300), encoding="utf-8")
    except FileNotFoundError:
        return "UNKNOWN", "executable not found"
    except subprocess.TimeoutExpired:
        return "UNKNOWN", "timeout"
    rc = proc.returncode
    if rc in unknown_codes:
        return "UNKNOWN", f"declared unknown exit {rc}"
    if rc < 0:
        return "UNKNOWN", f"killed by signal {-rc}"     # not a failed assertion
    return ("PASS", "") if rc == 0 else ("FAIL", f"exit {rc}")

def aggregate(manifest_path):
    m = json.loads(open(manifest_path, encoding="utf-8").read())
    unknown_codes = set(m.get("unknown_exit_codes", [2]))
    results = {}
    for spec in m["checks"]:
        results[spec["id"]] = run_check(spec, unknown_codes)

    # every declared check must have produced a result
    for spec in m["checks"]:
        results.setdefault(spec["id"], ("UNKNOWN", "no result recorded"))

    if any(v[0] == "FAIL" for v in results.values()):
        return 1, results
    if any(v[0] == "UNKNOWN" for v in results.values()):
        return 2, results          # fail closed: not green
    return 0, results
```

Three properties do the work: the verdict comes from the return code, a crash or timeout
lands in `UNKNOWN` rather than being lost, and a missing result is materialized as
`UNKNOWN` instead of being skipped in the report.

## Absence of signal is an alarm

A monitor that stops reporting looks, from the outside, exactly like a calm system.

- **Always-firing watchdog.** A rule that fires unconditionally (`vector(1)` in Prometheus)
  proves the whole pipeline - rule engine, alertmanager, receiver - is alive. When it goes
  quiet, the silence *is* the alarm.
- **Missing series.** `absent()` / `absent_over_time(metric[15m])` turns "no data" into a
  firing condition. Without it, a crashed exporter is a flat, quiet dashboard.
- **Reporter silence.** A supervisor that has not checked in within `SILENCE_MINUTES`
  raises its own alarm. A dead watchdog must not be able to look healthy.

```yaml
# Prometheus: the two rules that make silence visible
groups:
  - name: meta
    rules:
      - alert: Watchdog                 # must always fire; its absence is the signal
        expr: vector(1)
        labels: {severity: none}
      - alert: ExporterGone
        expr: absent_over_time(up{job="worker"}[15m])
        for: 5m
        labels: {severity: page}
```

## Suppressed repeat is not health

Deduplication and repeat-suppression are correct behaviour and a common source of lying
logs: an alert already delivered is not re-sent, and the reporter prints "all green"
because it saw no *new* alert this cycle.

Log the two situations differently:

```text
all green: 0 findings
suppressed: 16 findings still open, alarms already delivered (no new alerts this cycle)
```

A supervisor that printed "all green" for 72 consecutive cycles while 16 findings stood
open was not lying about the findings - it was lying about the *shape of its own silence*.

## Structured results, not prose

CI report formats (JUnit XML, TAP, CTRF) exist because prose is not a contract. A summary
step reads the structured result or the return code; it never greps for a word.

```bash
# WRONG - the verdict depends on which word this month's author chose
python run_checks.py | grep -c "FAIL" && echo "red" || echo "green"

# RIGHT - the pipeline preserves the failing status, the verdict is the code
set -o pipefail
python run_checks.py --junit-xml results.xml | tee run.log
rc=$?
case "$rc" in
  0) echo "PASS" ;;
  2) echo "UNKNOWN - not green" ; exit 2 ;;
  *) echo "FAIL" ; exit 1 ;;
esac
```

Without `set -o pipefail` the pipeline reports the exit code of `tee`, so every failure
downstream of a pipe reads as success.

## Gotchas

- **Issue:** the aggregator greps stdout for `FAIL`, and a check written later prints
  "MISMATCH" or a localized word. The suite goes green with real defects inside. ->
  **Fix:** judge by exit code or a structured report; treat printed text as human-facing
  only. Unifying the wording fixes one round and breaks on the next author.
- **Issue:** `sys.exit(main())` where `main()` can fall off the end and return `None`.
  `None` exits 0, so every failure path reports success. -> **Fix:** every branch returns
  an explicit code; assert the return type in a test.
- **Issue:** a check that could not run (missing binary, no credentials, unreachable
  target) is silently omitted from the report, so the summary shows only passes. ->
  **Fix:** materialize every declared check; a missing result is `UNKNOWN` and blocks green.
- **Issue:** a probe answers about the wrong target - the queue is read on one port while
  the container being restarted listens on another - and the wrong answer has the same
  shape as the right one. -> **Fix:** the probe echoes the identity of what it measured
  (endpoint, container id, revision) and the consumer asserts on that identity.
- **Issue:** timeouts and signals are folded into `FAIL`, so a flaky infrastructure problem
  is indistinguishable from a genuine assertion failure and gets "fixed" by retrying. ->
  **Fix:** timeout, signal kill, and launch failure are `UNKNOWN`; only a completed run
  that disagreed with expectation is `FAIL`.
- **Issue:** an alert repeats forever on a known blocked condition, so the channel gets
  muted by its readers - a channel people learn to ignore is worse than no channel. ->
  **Fix:** suppress the repeat but keep the standing count visible in the periodic report.

## See Also

- [[negative-controls-for-verification]] - proving a check is able to go red at all
- [[ci-cd-test-automation]] - where the exit-code contract is consumed
- [[monitoring-and-observability]] - watchdog and absence alerting in practice
- [[observability-query-languages]] - `absent_over_time` and friends
- [[sre-incident-management]] - alert fatigue and suppression policy
- [[test-architecture]] - reporting layers and result formats
- [[winhttp-async-client]] - timeout as a third outcome in client code
