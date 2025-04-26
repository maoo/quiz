# Which security issues exist in this Terraform configuration?

Analyze this infrastructure-as-code snippet and identify potential security issues.

```terraform
resource "aws_s3_bucket" "data_bucket" {
  bucket = "company-data-bucket-${var.environment}"
  acl    = "public-read"

  versioning {
    enabled = true
  }
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_execution_policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "*"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  description = "Security group for web servers"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Options
1. Public S3 bucket
2. Missing S3 logging
3. Wildcard IAM policy
4. Open SSH access
5. No resource tagging
6. Missing bucket policy
7. No encryption in use
8. MFA delete disabled
9. Open egress traffic
10. Versioning enabled

## Sources
- [Terraform AWS Security Best Practices](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/security-best-practices)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/006-question