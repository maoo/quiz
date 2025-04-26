# Answers to: What's correct in this Helm chart?

1. Uses fixed tag - TRUE
2. Has resource limits - TRUE
3. Uses NodePort - FALSE
4. Has replica count = 3 - FALSE
5. Has probes - TRUE
6. Uses rolling update - FALSE
7. Runs as root - FALSE
8. Uses HTTPS - TRUE
9. Has PVC config - FALSE
10. Uses ClusterIP - TRUE

Notes:
- The image tag is fixed at "1.2.3" (not using "latest")
- Resource limits and requests are specified
- Service type is ClusterIP, not NodePort
- Replica count is set to 2, not 3
- Liveness probe is configured
- No specific deployment strategy is defined
- SecurityContext specifies runAsNonRoot: true
- HTTPS is implied by the cert-manager annotation
- No PersistentVolumeClaim configuration is present
- Service type is explicitly set to ClusterIP