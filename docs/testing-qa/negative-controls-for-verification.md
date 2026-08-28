---
title: "Negative Controls for Verification"
description: "A green check proves nothing until it has been shown able to go red. Hide-the-subject protocol, must-fail fixtures, mutation testing as residual-risk measurement, and the self-certifying-proof anti-pattern."
---

# Negative Controls for Verification

Every instrument needs a case that **must** come back red. Without one, a green result
carries no information: it is equally consistent with "the system is correct" and "the
instrument cannot detect anything". A test with no assertion cannot fail; a gate that
reads the wrong file cannot fail; a proof that never touches its subject cannot fail.

## The measurement: hide the subject, demand red

The protocol is one line long and settles the question mechanically.

1. Declare what the check is about (the *subject*) and pin it by digest.
2. Remove, corrupt, or replace the subject.
3. Run the check. It **must** return non-zero.
4. If it stays green, the instrument is broken - not the system.

```python
import hashlib, json, shutil, subprocess, tempfile
from pathlib import Path

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def gate(manifest_path: Path) -> int:
    """Refuse to accept a proof that cannot go red when its subject disappears."""
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    subject, check = Path(m["subject"]), m["check"]

    if digest(subject) != m["subject_sha256"]:
        print("subject changed since the manifest was written")
        return 1

    green = subprocess.run(check, capture_output=True).returncode
    if green != 0:
        print("check fails on the intact subject")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        stash = Path(tmp) / subject.name
        shutil.move(subject, stash)                 # hide the subject
        try:
            red = subprocess.run(check, capture_output=True).returncode
        finally:
            shutil.move(stash, subject)             # always restore

    if red == 0:
        print("NEGATIVE CONTROL FAILED: check is green without its subject")
        return 1
    return 0
```

**Measured baseline from one audit of 18 proof scripts:** 16 stayed green in a world
containing nothing but the script itself - 6 asserted nothing, 10 verified artifacts they
had just written, 1 reached outside its own scope, 1 did not reproduce. Their exit codes
were unchanged by deleting the thing they claimed to prove.

## Must-fail fixtures in the self-test

An instrument ships with its own suite, and that suite needs cases that are red by
construction. The most valuable fixture is the one that **prints success and exits
non-zero**, because it separates "reads the text" from "reads the status".

```python
FIXTURES = [
    ("intact",        0),   # subject present, check correct
    ("no_manifest",   1),   # nothing declares what is being proved
    ("empty_check",   1),   # check asserts nothing
    ("prints_pass",   1),   # prints "PASS", exits 1 - status wins over prose
    ("wrong_digest",  1),   # subject differs from the pinned digest
    ("unknown_flag",  2),   # cannot run -> UNKNOWN, never green
]

def self_test() -> int:
    bad = [name for name, want in FIXTURES if run_fixture(name) != want]
    if bad:
        print("self-test failed on:", ", ".join(bad))
        return 1
    return 0
```

Run the self-test in CI on every change to the instrument. An instrument without a
self-test is an unverified claim about verification.

## Mutation testing: the general form

Negative controls scale up to mutation testing. Inject a small semantic change into the
code under test and re-run the suite:

- **Killed mutant** - some test failed. The suite detects that class of defect.
- **Surviving mutant** - every test passed on wrong code. That is **residual risk**,
  measured rather than assumed.

```bash
# Python: mutmut / cosmic-ray. JS/TS: Stryker. Java: PIT.
mutmut run --paths-to-mutate src/pricing.py
mutmut results          # survivors are the report; coverage percentage is not
```

Line coverage cannot substitute for this. Code executed by a test with no assertion is
100% covered and 0% verified - it is exactly the shape that makes all mutants survive.

Apply the same idea to any gate, not only unit tests: change the check's own logic in a
way that should break it (read the wrong field, compare against a constant, swap the
comparison) and confirm the verdict changes. Mutations that provably cannot change
behaviour are *equivalent mutants*; record them as such rather than counting them as
detection failures.

## The self-certifying proof

The recurring anti-pattern: a script that writes an artifact, then verifies the artifact it
just wrote.

```python
# WRONG - proves the script can write a file, nothing about the system
out = run_pipeline()
Path("evidence.json").write_text(json.dumps(out))
assert json.loads(Path("evidence.json").read_text())["status"] == "ok"
```

It is green on a machine where the subject does not exist at all. The fix is to make the
proof depend on something it did not produce: a pinned input digest, a response from the
real service, an artifact built by a different step, a file whose absence it cannot paper
over.

```python
# RIGHT - the proof is bound to an external subject it cannot fabricate
manifest = json.loads(Path("proof.manifest.json").read_text(encoding="utf-8"))
subject = Path(manifest["subject"])                      # produced elsewhere
assert digest(subject) == manifest["subject_sha256"]     # cannot pass if it is missing
assert probe_real_endpoint(manifest["endpoint"]).status_code == 200
```

## Where green suites go blind

A passing suite is evidence about the shapes somebody thought of. It says nothing about
shapes nobody enumerated.

- A guard written against a list of spellings covers that list. One measured case: a fix
  closed one escape path, its own probe confirmed it, 32 tests passed - and an independent
  reviewer found 18 further variants of the same construct, 15 of them live.
- The author of a finding is the worst reviewer of its fix: the probe shares the blind spot
  that produced the defect. Whoever writes the fix should not certify the class closed.
- Prefer a check that is *causal* (one property that all variants must violate) over a
  check that enumerates spellings.

## Gotchas

- **Issue:** a gate is added, goes green immediately, and is trusted from then on - but it
  was green before the feature existed. -> **Fix:** before merging any gate, run it against
  a deliberately broken input and require red. A gate whose first result is green has not
  been demonstrated to work.
- **Issue:** the check greps its own log for a success word, so rewording the message
  silently flips the verdict. -> **Fix:** judge on exit status or structured output; see
  [[three-state-check-aggregation]].
- **Issue:** high line coverage is used as the quality metric while assertions are thin.
  All mutants survive and nobody notices. -> **Fix:** report surviving mutants, not
  coverage percentage; treat survivors as a work list.
- **Issue:** the negative-control run leaves the subject moved away because the check
  crashed mid-run. -> **Fix:** restore in a `finally` block (or operate on a copy), and
  assert the subject is back before exiting.
- **Issue:** a "verification" step reruns the generator and compares it with itself, so
  both sides move together and disagreement is impossible. -> **Fix:** pin one side by
  digest, or compare against an artifact from an independent producer.
- **Issue:** the fixture suite contains only must-pass cases, so a broken instrument that
  always exits 0 passes its own self-test. -> **Fix:** at least one fixture that prints a
  success word and must still be judged red.

## See Also

- [[three-state-check-aggregation]] - PASS / FAIL / UNKNOWN and fail-closed rollup
- [[test-architecture]] - where gates live in the suite
- [[ci-cd-test-automation]] - running self-tests and mutation runs in the pipeline
- [[pytest-fundamentals]] - assertion styles that actually fail
- [[chaos-engineering-and-testing]] - fault injection as a negative control at system scale
- [[agent-evaluation]] - the same problem for agent output graders
