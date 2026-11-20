# Lab 5 — Technical Report (fill after real GitHub Actions run)

## Application
Mini-VulnFinBot is a Flask API with `/health` and `/api/chat`. It validates JSON, message type and length, and returns general mock financial responses.

## Scan results (do not invent results)
| Tool | Findings and identifiers | Severity | Recommended action |
|---|---|---|---|
| Bandit | TODO from JSON | TODO | TODO |
| Semgrep | TODO from JSON | TODO | TODO |
| pip-audit | TODO from JSON | TODO | Upgrade affected dependencies |
| Trivy | TODO from JSON | TODO | Update base image and dependencies |
| OWASP ZAP | TODO from JSON | TODO | Review HTTP response headers |
| AI security tests | TODO from report | Mock-only | Test a real LLM separately |

## Controlled vulnerability demonstration
1. Create an isolated branch; add a temporary `eval(user_input)` example in a separate test-only Python file under `app/`.
2. Push the branch and record Semgrep/Bandit findings and screenshots.
3. Remove the insecure example, push again, and compare findings.
4. Do not merge the insecure branch into main.

## Evidence
Add links or screenshots of: repository tree, running `/health`, successful tests, GitHub Actions jobs, artifact list, findings before/after remediation.

## Limitations
The financial assistant is a deterministic mock. Prompt-injection tests only assess app-level behavior; no genuine LLM attack-resistance conclusion is possible.
