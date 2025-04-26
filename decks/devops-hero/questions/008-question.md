# What issues exist in this Kubernetes manifest?

Analyze this Kubernetes deployment configuration and identify issues or best practices that are not being followed.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api-container
        image: company/api:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_PASSWORD
          value: "password123"
        - name: API_KEY
          value: "sk_live_abcdef123456"
        resources: {}
        securityContext:
          privileged: true
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 3
          periodSeconds: 3
```

## Options
1. Using latest tag
2. Hard-coded secrets
3. Single replica
4. Missing readiness
5. No resource limits
6. Privileged container
7. Wrong port exposed
8. No node selector
9. Missing labels
10. Probe too frequent

## Sources
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [CNCF Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/blob/main/security-whitepaper/CNCF_cloud-native-security-whitepaper-Nov2020.pdf)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/008-question