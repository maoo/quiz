# DevOps Hero Question 004

## Kubernetes Deployment Analysis

Examine the following YAML manifest for a Kubernetes Deployment and determine if each statement about it is TRUE or FALSE.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: web-apps
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-frontend
  template:
    metadata:
      name: frontend-pod
      labels:
        app: frontend-web
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
```

1. Wrong API version
2. Missing strategy
3. Label mismatch
4. Port is invalid
5. Replicas too low
6. Wrong image tag
7. Missing readiness
8. Low memory limit
9. Missing namespace
10. Spec is complete

## Sources
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes Labels and Selectors: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

## URL
https://blog.session.it/quiz/decks/devops-hero/questions/004-question