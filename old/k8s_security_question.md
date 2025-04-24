## DevOps Quiz Question

**Question:** In Kubernetes security, which practices effectively mitigate risks when deploying sensitive workloads? A robust security posture requires multiple layers of protection including network policies, RBAC controls, runtime security, and using security contexts. When implementing these controls across a cluster with pods that require varying levels of privilege, which of the following statements are accurate regarding Kubernetes security best practices as defined by CIS Benchmarks and the Kubernetes documentation?

**Options:**
1. PodSecurityPolicies are current
2. Set allowPrivilegeEscalation:false
3. Run containers as root user
4. Use latest image tags in prod
5. limitSeccompProfiles is required
6. NetworkPolicies use CIDRs
7. Implement pod service accounts
8. Default seccomp profile works
9. RBAC should allow admin:all
10. Use readOnlyRootFilesystem

**Answers:**
1. FALSE
2. TRUE
3. FALSE
4. FALSE
5. FALSE
6. TRUE
7. TRUE
8. TRUE
9. FALSE
10. TRUE