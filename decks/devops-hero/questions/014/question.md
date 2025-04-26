# What pattern does each Bash script line match?

Identify the bash scripting pattern or concept used in each part of this deployment script.

```bash
#!/bin/bash
set -e

ENVIRONMENT=${1:-dev}
VERSION=$(git describe --tags --always)
APP_NAME="myservice"
KUBE_CONTEXT="cluster-${ENVIRONMENT}"

echo "Deploying $APP_NAME version $VERSION to $ENVIRONMENT"

# Check prerequisites
if ! command -v kubectl >/dev/null 2>&1; then
    echo "Error: kubectl not found"
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker not found"
    exit 1
fi

# Build and push Docker image
docker build -t "$APP_NAME:$VERSION" .
docker tag "$APP_NAME:$VERSION" "registry.example.com/$APP_NAME:$VERSION"
docker push "registry.example.com/$APP_NAME:$VERSION"

# Update Kubernetes deployment
kubectl config use-context "$KUBE_CONTEXT"
kubectl set image deployment/$APP_NAME $APP_NAME="registry.example.com/$APP_NAME:$VERSION" --record
kubectl rollout status deployment/$APP_NAME

# Notify
echo "Deployment completed successfully!"
```

## Options
1. Error handling
2. String interpolation
3. Default parameters
4. Command substitution
5. Error redirection
6. Conditional checks
7. Exit codes
8. Variable assignment
9. Command execution
10. String literals

## Sources
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Bash Scripting Best Practices](https://linuxconfig.org/bash-scripting-best-practices)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/014-question