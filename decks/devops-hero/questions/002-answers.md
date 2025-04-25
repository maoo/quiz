# DevOps Hero Question 002 - Answers ✅

## Dockerfile Best Practices

### Correct Answers
1. ❌ Uses pinned version
2. ❌ Has multi-stage build
3. ❌ Runs as non-root
4. ❌ Has cache efficiency
5. ✅ Creates large image
6. ❌ Uses HEALTHCHECK
7. ✅ Has layer reduction
8. ❌ Includes .dockerignore
9. ❌ Uses best practices
10. ❌ Has proper cleanup

## Explanation
This question tests understanding of Dockerfile best practices. The example violates several best practices: it uses the latest tag instead of a pinned version, lacks multi-stage builds, explicitly sets USER to root (security issue), doesn't use proper cache optimization with frequent changes last, uses Ubuntu instead of smaller base images, lacks a HEALTHCHECK command, doesn't mention .dockerignore file usage, and doesn't clean up apt caches. It does have some layer reduction by chaining commands with &&, but overall doesn't follow most container best practices.