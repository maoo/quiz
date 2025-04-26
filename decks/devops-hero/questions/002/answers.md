# Answers to: What Docker instruction is used in this Dockerfile?

1. Cache busting - Line 9-10
2. Base image - Line 6
3. Directory setting - Line 7
4. Volume mounting - Not used
5. Entry command - Line 14
6. File copying - Line 8
7. Environment var - Line 11
8. Port publishing - Line 12
9. User switching - Line 13
10. Package install - Line 9-10

Notes:
- Line 6: FROM alpine:3.14 sets the base image
- Line 7: WORKDIR /app sets the working directory
- Line 8: COPY . . copies files from build context to image
- Line 9-10: RUN installs packages and has --no-cache flags (cache busting)
- Line 11: ENV PORT=8080 sets an environment variable
- Line 12: EXPOSE $PORT exposes a port for publishing
- Line 13: USER nobody switches to non-root user
- Line 14: CMD ["python3", "app.py"] sets the entry command
- No VOLUME instruction is present for volume mounting