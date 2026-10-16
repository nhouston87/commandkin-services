# CommandKin services

Backend repository for the CommandKin Express API. This repository is
currently a documentation and CI baseline; application implementation starts in M1.

## Baseline validation

Run `python scripts/check_repository.py` with Python 3.10 or newer and Git.
CI uses the same command on Ubuntu. It checks tracked Markdown, Python, and YAML
for UTF-8, nonempty files, final newlines, trailing whitespace, and merge markers.
Markdown must have a title and existing inline relative file links within this repo.
External URLs, heading anchors, and reference-style links are not validated.
This is not a Markdown/YAML parser or a credential scanner.

The stable required check is `Services CI`. It runs on every PR, including documentation
changes, and fails unless all baseline jobs succeed. Workflow permissions are
read-only, checkout is pinned, credentials are not retained, jobs have timeouts,
and newer runs cancel superseded runs. PR jobs use no private repositories or secrets.

## Review policy

Every change to `main` requires a PR, passing `Services CI` on an up-to-date branch,
and resolved review conversations. The owner selected zero required approving
reviews for solo maintenance; the maintainer reviews the diff and CI evidence
before explicitly merging. Protection applies to admins, with force pushes and
branch deletion disabled. Administrators can still edit repository protection;
this policy is not a defense against an administrator changing the rules.

CI and policy configuration are tracked in issue #1. Verification evidence will
be recorded on its PR. No automatic merge is enabled by this workflow.

## M1 follow-up

When the services skeleton is introduced, add a committed dependency lockfile,
locked installation, lint, typechecking, unit, mocked authorization, contract, and OpenAPI checks, and a production build to
the jobs feeding `Services CI`. None of those application checks exists in this baseline.

## Trusted integration boundary

Public PR validation receives no private checkout credentials and does not run
private migrations or database integration. It does not authorize schema-sensitive
merges. Those changes remain blocked by maintainer policy until the separate
trusted integration gate is implemented and proven. That gate must bind sanitized
evidence from reviewed, pinned revisions to the exact services head SHA; a new
push requires fresh evidence. No technically enforced integration check exists yet.
Public workflows must never execute untrusted PR code with privileged secrets.

[Deliberate gate proof](missing-gate-proof.md)
