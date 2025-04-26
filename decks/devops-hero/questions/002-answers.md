# Answers to: Which statements are true for this Dockerfile?

1. Uses latest Alpine - FALSE
2. Runs as non-root - TRUE
3. Copies all files - TRUE
4. Has security issue - FALSE
5. Sets working dir - TRUE
6. Uses multistage build - FALSE
7. Installs Python 2 - FALSE
8. Exposes port 8080 - TRUE
9. Uses ENTRYPOINT - FALSE
10. Caches pip packages - FALSE

Notes:
- It uses Alpine 3.14 specifically, not latest
- It runs as 'nobody' user (non-root) which is good security practice
- It uses COPY . . which copies all files from the context
- Sets working directory to /app with WORKDIR
- It uses `--no-cache-dir` for pip which prevents caching packages
- It uses CMD not ENTRYPOINT
- It installs Python 3, not Python 2