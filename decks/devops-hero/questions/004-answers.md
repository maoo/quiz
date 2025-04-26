# Answers to: What Kubernetes feature is applied in this manifest?

1. Namespace isolation - Line 10
2. Security policy - Line 26-27
3. Resource quotas - Line 31-37
4. Auto-scaling - Not present
5. Image versioning - Line 30
6. Health checking - Line 40-48
7. Update strategy - Line 16-20
8. Service discovery - Line 13-15, 23-24
9. Pod replication - Line 12
10. Port mapping - Line 38-39

Notes:
- Namespace isolation: The 'namespace: production' defines the namespace
- Security policy: The securityContext with runAsNonRoot enforces security
- Resource quotas: CPU/memory limits and requests define resource boundaries
- Image versioning: The specific tag v1.2.3 on the image
- Health checking: Both liveness and readiness probes are configured
- Update strategy: RollingUpdate with maxUnavailable and maxSurge parameters
- Service discovery: The labels and selectors enable service discovery
- Pod replication: The replicas: 3 setting defines how many pods to run
- Port mapping: The containerPort defines which port the container exposes
- Auto-scaling is not present (would require HorizontalPodAutoscaler)