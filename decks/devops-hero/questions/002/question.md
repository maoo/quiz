# What Docker instruction is used in this Dockerfile?

Match each line from this Dockerfile with the correct Docker instruction or concept.

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
1. Cache busting
2. Base image
3. Directory setting
4. Volume mounting
5. Entry command
6. File copying
7. Environment var
8. Port publishing
9. User switching
10. Package install

## Sources
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/security/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/002-question

Question Type: QR - Embedded content
Answer Type: Names/labels/words