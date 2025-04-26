# Which statements are true for this Dockerfile?

Analyze this Docker container definition and identify which statements are true.

```dockerfile
FROM alpine:3.14
WORKDIR /app
COPY . .
RUN apk add --no-cache python3 py3-pip && \
    pip install --no-cache-dir -r requirements.txt
ENV PORT=8080
EXPOSE $PORT
USER nobody
CMD ["python3", "app.py"]
```

## Options
1. Uses latest Alpine
2. Runs as non-root
3. Copies all files
4. Has security issue
5. Sets working dir
6. Uses multistage build
7. Installs Python 2
8. Exposes port 8080
9. Uses ENTRYPOINT
10. Caches pip packages

## Sources
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/security/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/002-question