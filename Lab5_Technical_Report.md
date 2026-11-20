# Lab 5 — Technical Security Report

**Project:** Mini-VulnFinBot  
**Repository:** https://github.com/kamnett/vulnfinbot-secure-pipeline  
**Date:** 20 November 2026

## 1. Project overview
Mini-VulnFinBot is a Python Flask REST API with a health-check endpoint (`GET /health`) and a chat endpoint (`POST /api/chat`). The current chat implementation uses deterministic mock responses, not a real large language model. The project uses GitHub Actions to automate testing and security scans.

## 2. Security testing methodology
The pipeline runs Python unit and mock AI security tests, Bandit and Semgrep static analysis, pip-audit dependency scanning, a Docker build and Trivy image scan, and an OWASP ZAP baseline scan against the running application. Reports are uploaded as GitHub Actions artifacts.

## 3. Final security scan findings
The following findings were extracted from the final uploaded GitHub Actions artifact (`vulnfinbot-security-reports-4.zip`).

| Tool | Observed result | Assessment / recommended action |
|---|---|---|
| Bandit | 0 findings | Continue scanning on each code change. |
| Semgrep | 0 findings | Keep and expand custom rules as application complexity increases. |
| pip-audit | 0 reported dependency vulnerabilities | Continue monitoring and updating Python dependencies. |
| Trivy | 237 findings: 49 High, 111 Medium, 68 Low, 9 Unknown | Prioritize High findings, identify affected image packages and fixed versions, update/rebuild the base image, and rescan. |
| OWASP ZAP | 1 informational alert: Non-Storable Content | Review caching behavior; no Medium or Low alert was reported in the final ZAP JSON. |
| AI security tests | 6 tests passed in mock-only test run | These tests check deterministic application behavior; test a real LLM separately before claiming prompt-injection resistance. |

## 4. Security remediation demonstration
The application initially set `Content-Security-Policy` to `default-src 'none'; frame-ancestors 'none'`. The response-header configuration was strengthened with `base-uri 'none'`, `form-action 'none'`, `Cross-Origin-Resource-Policy: same-origin`, and `Permissions-Policy: camera=(), microphone=(), geolocation=()`.

The earlier scan was reported during the laboratory workflow as containing four alert categories, including CSP, Cross-Origin-Resource-Policy, and Permissions-Policy warnings. In the final uploaded ZAP JSON, only the informational `Non-Storable Content` alert remains. This is consistent with the intended header remediation. The original artifact should be retained as evidence for a strict before/after comparison.

A separate Dockerfile change upgraded `pip` during image build. The earlier reported Trivy count was 240, and the final verified report contains 237 findings. This change in counts alone does not establish that three particular vulnerabilities were remediated; the image package inventories and CVE identifiers should be compared to make that determination.

## 5. AI-specific security limitations
The automated mock tests include instruction override, system prompt disclosure, sensitive-data disclosure, unauthorized tool use, and unsafe output scenarios. The mock returns a fixed financial response and does not expose tools or confidential data. This is useful for validating application-level behavior but **does not constitute a genuine LLM prompt-injection evaluation**. A controlled real-model test environment would be needed for that claim.

## 6. Remaining risks and recommended next steps
1. Review Trivy's 49 High-severity findings, including affected packages, CVEs, and whether patched versions are available.
2. Rebuild against an updated, explicitly selected base image and compare Trivy findings at the CVE level.
3. Keep security headers and automated API tests in place.
4. Expand Semgrep rules and test coverage when new features are added.
5. If an actual LLM is integrated, implement authorization boundaries and evaluate prompt-injection attacks using synthetic data only.
6. Review the ZAP scan scope: the current workflow targets `/health`, which does not provide comprehensive coverage of the `POST /api/chat` endpoint.

## 7. Evidence for submission
- GitHub repository and successful GitHub Actions workflow run.
- The final security-reports artifact, including Bandit, Semgrep, pip-audit, Trivy, ZAP and AI security reports.
- Screenshot of `pytest -v` showing 19 passed tests.
- Screenshot of `GET /health` returning `{"status":"healthy"}`.
- Before/after ZAP reports or screenshots showing header-related alerts disappearing.
- Screenshot of the Trivy findings and the workflow artifact upload.

## 8. Conclusion
The laboratory produced a working Flask application with an automated GitHub Actions security-testing workflow and collected scanner artifacts. The security-header remediation was reflected in the later ZAP report. The container still has significant reported vulnerabilities, and mock AI tests must not be presented as evidence of real LLM security. These limitations are documented rather than concealed.
