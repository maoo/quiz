# Answers to: What issues exist in this Kubernetes manifest?

1. Using latest tag - TRUE
2. Hard-coded secrets - TRUE
3. Single replica - TRUE
4. Missing readiness - TRUE
5. No resource limits - TRUE
6. Privileged container - TRUE
7. Wrong port exposed - FALSE
8. No node selector - TRUE
9. Missing labels - FALSE
10. Probe too frequent - TRUE

Notes:
- Using `:latest` tag makes deployments unpredictable and harder to rollback
- Secrets like passwords and API keys should be in Kubernetes Secrets, not env variables
- Only 1 replica means no high availability
- No readinessProbe defined, only livenessProbe
- No resource requests or limits defined, which could lead to resource contention
- Container runs in privileged mode, which is a major security risk
- Container port 8080 is correctly exposed
- No node selector or affinity rules for controlling pod placement
- Basic labels are present (`app: api`), though more detailed labels would be better
- Health probe running every 3 seconds is too frequent and can cause unnecessary load