# What Kubernetes feature is applied in this manifest?

Identify the Kubernetes functionality represented in each part of this deployment manifest.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: backend
    spec:
      securityContext:
        runAsNonRoot: true
      containers:
      - name: api
        image: company/api:v1.2.3
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

## Options
1. Namespace isolation
2. Security policy
3. Resource quotas
4. Auto-scaling
5. Image versioning
6. Health checking
7. Update strategy
8. Service discovery
9. Pod replication
10. Port mapping

## Sources
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/004-question