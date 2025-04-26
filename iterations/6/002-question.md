# DevOps Hero Question 002 🐳

## Dockerfile Best Practices

```dockerfile
FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y nginx
COPY . /app
USER root
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Which of these statements are TRUE about this Dockerfile?

### Options
1. Uses pinned version
2. Has multi-stage build
3. Runs as non-root
4. Has cache efficiency
5. Creates large image
6. Uses HEALTHCHECK
7. Has layer reduction
8. Includes .dockerignore
9. Uses best practices
10. Has proper cleanup

## References 📚
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Container Security Best Practices](https://sysdig.com/blog/dockerfile-best-practices/)

## Question URL 🔗
[View Question Online](https://blog.session.it/quiz/decks/devops-hero/questions/002-question)