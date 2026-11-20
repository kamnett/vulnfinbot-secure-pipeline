# Mini-VulnFinBot — Lab 5

A small Flask financial-advice **mock** API with a GitHub Actions security pipeline. The mock is deterministic and **not an LLM**; its tests do not establish resistance to prompt injection in a real model.

## Architecture
`Client -> Flask /api/chat -> request validation -> deterministic mock -> JSON response`.
`GitHub Actions -> pytest, Bandit, Semgrep, pip-audit, Docker, Trivy, OWASP ZAP -> artifacts`.

## Local setup (Python 3.12)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
python run.py
```
Visit `http://127.0.0.1:5000/health` or send:
```bash
curl -X POST http://127.0.0.1:5000/api/chat -H 'Content-Type: application/json' -d '{"message":"How can I manage my monthly budget?"}'
```

## Docker
```bash
docker build -t vulnfinbot:latest .
docker run --rm -p 5000:5000 vulnfinbot:latest
```

## Security tools
- **Bandit:** Python source-code security analysis.
- **Semgrep:** custom rules for `eval`, `exec`, and `shell=True`.
- **pip-audit:** Python dependency vulnerabilities.
- **Trivy:** Docker image vulnerabilities.
- **OWASP ZAP:** passive baseline web scan of the running health endpoint.
- **AI tests:** application-level mock tests for instruction override, prompt disclosure, sensitive data, unauthorized tool actions, and output validation. Real prompt-injection evaluation requires an actual model.

The pipeline runs on push and pull requests. Go to **GitHub > Actions > Security CI Pipeline > latest run > Artifacts** to download `vulnfinbot-security-reports`. Scanner steps are non-blocking for report collection; inspect reports rather than assuming a green workflow means no vulnerabilities.

## Vulnerabilities and remediation
Do not invent findings. Fill in `TECHNICAL_REPORT_TEMPLATE.md` from actual scan outputs. For the controlled example, add an `eval(user_input)` call in a **separate throwaway branch only**, run Semgrep/Bandit, remove it, rerun, and compare results. Never merge insecure test code.

## Known limits
- ZAP baseline scans only the health endpoint; it does not actively fuzz the POST chat API.
- Dependency ranges are not lockfile-pinned; update and re-audit dependencies.
- The mock does not have model prompts, credentials, or executable tools; AI-specific results are limited to API behavior.
- Check CI logs and artifact contents for scanner errors and fix any issues before submission.
