# Identify best practices in this Terraform code

Analyze the following Terraform configuration and determine which statements are true regarding best practices.

```hcl
provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"
  
  name = "production-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-west-2a", "us-west-2b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Environment = "production"
    Terraform   = "true"
    Owner       = "DevOps-Team"
  }
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Allow web traffic"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
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
1. Uses modules
2. Has version pinning
3. Uses variables
4. Has proper tagging
5. Has state locking
6. Uses workspaces
7. Has remote backend
8. Uses data sources
9. Enables encryption
10. Uses conditionals

## Sources
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)

URL: https://blog.session.it/quiz/decks/devops-hero/questions/010-question

Question Type: QR - Embedded content
Answer Type: Binary