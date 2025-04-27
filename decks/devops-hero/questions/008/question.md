# Rank these Kubernetes manifest issues by severity

Watch this video about Kubernetes security issues and then rank the issues in the manifest below from most critical (1) to least critical (10).

## Kubernetes Security Best Practices

<iframe width="560" height="315" src="https://www.youtube.com/embed/wqsUfvRyYpw" title="Kubernetes Security Best Practices" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Now analyze this Kubernetes manifest for security and operational issues:

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
9. Missing namespace
10. Probe too frequent

## Sources
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [CNCF Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/blob/main/security-whitepaper/CNCF_cloud-native-security-whitepaper-Nov2020.pdf)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-checklist/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/008-question

Question Type: QR - YouTube Video
Answer Type: Ordering/number