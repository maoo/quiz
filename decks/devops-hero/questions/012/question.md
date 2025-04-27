# What's correct in this Helm chart?

Analyze this Helm chart diagram and values.yaml file to determine which statements are true.

## Helm Chart Architecture

![Helm Architecture](https://helm.sh/img/helm-architecture.svg)
*Helm Architecture*

![Kubernetes Application Deployment with Helm](https://d33wubrfki0l68.cloudfront.net/9dce8ca2b56a3aa742b24a7c7a8c929d4676e55c/43822/docs/v21.1/images/kubernetes-deploy-sequence.png)
*Kubernetes Application Deployment with Helm*

![Helm Template Structure](https://d33wubrfki0l68.cloudfront.net/c1d2fb8d7e5cd9f1c5d1d9e92e90599ec6761eac/9c456/docs/topics/chart_template_guide/graduated-bases.png)
*Helm Template Structure*

Now analyze this values.yaml file:

```yaml
# values.yaml for a web application
replicaCount: 2

image:
  repository: myapp
  tag: "1.2.3"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 60
  periodSeconds: 10

securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

## Options
1. Uses fixed tag
2. Has resource limits
3. Uses NodePort
4. Has replica count = 3
5. Has probes
6. Uses rolling update
7. Runs as root
8. Uses HTTPS
9. Has PVC config
10. Uses ClusterIP

## Sources
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Helm Chart Development Tips](https://helm.sh/docs/howto/charts_tips_and_tricks/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/012-question

Question Type: QR - Embedded Images
Answer Type: Binary