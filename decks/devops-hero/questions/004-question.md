# Which statements are true about this Kubernetes manifest?

Examine this Kubernetes manifest and determine which statements about it are true.

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
1. Uses latest tag
2. Has resource limits
3. Runs Daemonset
4. Has network policy
5. Has health checks
6. Runs as non-root
7. Uses Canary deploy
8. Runs 3 replicas
9. Exposes NodePort
10. Has ConfigMap

## Sources
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/004-question