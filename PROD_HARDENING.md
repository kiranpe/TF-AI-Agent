
# Production Hardening Checklist for GKE + HTTPS + IAP

## ✅ Network & Access
- [ ] Enable VPC Service Controls to isolate access to sensitive resources.
- [ ] Use private GKE clusters with no public endpoint.
- [ ] Limit `kubectl` access using IAM & Workload Identity.

## ✅ Load Balancer & IAP
- [ ] Use Google-managed SSL certificates (✓)
- [ ] Restrict IAP to trusted email domain:
  - Set up OAuth brand to limit to `@company.com` accounts
  - In IAP access controls, allow only specific GCP groups or domains
- [ ] Enable HTTPS redirect in `FrontendConfig` (✓)
- [ ] Enable Cloud Armor WAF rules (e.g., block IPs, XSS, rate limiting)

## ✅ Kubernetes Settings
- [ ] Set resource `limits` and `requests` in all containers
- [ ] Enable liveness and readiness probes
- [ ] Use Node Affinity and Pod Anti-Affinity if needed
- [ ] Use GKE Autopilot or pre-defined node pools for isolation

## ✅ Logging & Monitoring
- [ ] Enable GKE-native monitoring with Cloud Monitoring and Logging
- [ ] Enable Error Reporting for FastAPI exceptions
- [ ] Configure Alerting policies (high latency, 5xx, etc.)

## ✅ Secrets & Configs
- [ ] Use Secret Manager or Vault instead of Kubernetes Secrets for sensitive data
- [ ] Rotate OAuth client secrets regularly
- [ ] Restrict access to secrets via Workload Identity

## ✅ CI/CD & GitOps
- [ ] Use GitHub Actions or ADO pipelines with lint + validation
- [ ] Use `terraform validate`, `tfsec`, and `kube-score` in CI
- [ ] Store Terraform state in remote backend (e.g., GCS + Locking)

## ✅ DNS
- [ ] Automate DNS zone creation via Terraform (✓)
- [ ] Use short TTLs for faster propagation

## ✅ Miscellaneous
- [ ] Use custom domain (✓)
- [ ] Add `robots.txt` to block web crawlers
- [ ] Set HTTP headers: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`

