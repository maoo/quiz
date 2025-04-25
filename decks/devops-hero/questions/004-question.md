# DevOps Hero Question 004 ⚙️

## Kubernetes YAML Analysis

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

Which statements are TRUE about this YAML manifest?

### Options
1. Uses latest tag
2. Has network policy
3. Has liveness probe
4. Sets resource limits
5. Uses StatefulSet
6. Has PodDisruptionBudget
7. Enables auto-scaling
8. Runs in production
9. Uses 3 replicas
10. Has pod security

## References 📚
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## Question URL 🔗
[View Question Online](https://blog.session.it/quiz/decks/devops-hero/questions/004-question)