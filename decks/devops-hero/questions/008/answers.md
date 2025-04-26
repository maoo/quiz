# Answers to: Rank these Kubernetes manifest issues by severity

1. Using latest tag - 6
2. Hard-coded secrets - 1
3. Single replica - 8
4. Missing readiness - 7
5. No resource limits - 5
6. Privileged container - 2
7. Wrong port exposed - 9
8. No node selector - 10
9. Missing namespace - 4
10. Probe too frequent - 3

Notes on severity ranking (most to least critical):
1. Hard-coded secrets - Directly exposes sensitive credentials
2. Privileged container - Provides root access to host system
3. Probe too frequent - Can cause service disruption
4. Missing namespace - Risk of resource conflicts and security isolation issues
5. No resource limits - Can lead to resource exhaustion
6. Using latest tag - Unpredictable deployments, no version control
7. Missing readiness - Potential for premature traffic routing
8. Single replica - Lack of high availability
9. Wrong port exposed - The port 8080 is actually correct, not a real issue
10. No node selector - Optional feature, least critical