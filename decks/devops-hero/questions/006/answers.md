# Answers to: Which security issues exist in this Terraform configuration?

1. Public S3 bucket - TRUE
2. Missing S3 logging - TRUE
3. Wildcard IAM policy - TRUE
4. Open SSH access - TRUE
5. No resource tagging - TRUE
6. Missing bucket policy - TRUE
7. No encryption in use - FALSE
8. MFA delete disabled - TRUE
9. Open egress traffic - TRUE
10. Versioning enabled - FALSE

Notes:
- The S3 bucket has `acl = "public-read"` which makes it publicly accessible
- The IAM policy uses wildcard permissions (`"*"` for both Action and Resource)
- SSH port 22 is open to the world (`0.0.0.0/0`)
- No resource tagging is implemented for cost allocation or security identification
- Bucket policy is missing, which could be used to further restrict access
- Server-side encryption is actually enabled with AES256
- MFA delete is not enabled on the S3 bucket
- Egress traffic allows all outbound connections (`0.0.0.0/0`)
- Versioning is correctly enabled, which is a security best practice