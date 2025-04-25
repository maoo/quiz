# DevOps Hero Question 002

## Kubernetes Deployment Troubleshooting

Analyze the following Kubernetes deployment manifest and determine which statements are TRUE about potential issues:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 3
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: app-container
        image: myregistry.com/myapp
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
```

1. Label mismatch exists
2. No image tag specified
3. CPU limit is missing
4. Wrong probe port
5. More replicas needed
6. No readiness probe
7. Port mismatch exists
8. Missing memory limit
9. Wrong API version
10. Needs imagePullPolicy

## Sources
- Kubernetes Deployments Documentation: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes Probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

## URL
https://blog.session.it/quiz/decks/devops-hero/questions/002-question