# Answers to: Which statements are true about this Kubernetes manifest?

1. Uses latest tag - FALSE
2. Has resource limits - TRUE
3. Runs Daemonset - FALSE
4. Has network policy - FALSE
5. Has health checks - TRUE
6. Runs as non-root - TRUE
7. Uses Canary deploy - FALSE
8. Runs 3 replicas - TRUE
9. Exposes NodePort - FALSE
10. Has ConfigMap - FALSE

Notes:
- It uses a specific tag (v1.2.3), not latest
- It has both resource limits and requests defined
- It's a Deployment, not a DaemonSet
- No NetworkPolicy is defined in this manifest
- It has both liveness and readiness probes (health checks)
- It uses securityContext.runAsNonRoot: true
- It uses RollingUpdate strategy, not Canary
- It specifies 3 replicas
- It only defines containerPort, not a NodePort service
- No ConfigMap is referenced or defined