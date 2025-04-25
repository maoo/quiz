# DevOps Hero Question 004 - Answers ✅

## Kubernetes YAML Analysis

### Correct Answers
1. ✅ Uses latest tag
2. ❌ Has network policy
3. ❌ Has liveness probe
4. ✅ Sets resource limits
5. ❌ Uses StatefulSet
6. ❌ Has PodDisruptionBudget
7. ❌ Enables auto-scaling
8. ✅ Runs in production
9. ✅ Uses 3 replicas
10. ❌ Has pod security

## Explanation
This question tests knowledge of Kubernetes manifests and configurations. The YAML shows a Deployment (not a StatefulSet) with 3 replicas running in the production namespace. It uses the latest tag for the nginx image (which is not recommended for production) and correctly sets resource requests and limits. It does not include health probes (liveness/readiness), network policies, PodDisruptionBudgets, auto-scaling configuration, or pod security context definitions.