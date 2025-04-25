# Terraform Configuration Analysis

## Question
Which of the following statements about this Terraform configuration are correct?

## Code Snippet
```terraform
1  provider "aws" {
2    region = "us-west-2"
3  }
4  
5  resource "aws_security_group" "web" {
6    name        = "web-sg"
7    description = "Security group for web servers"
8  
9    vpc_id = aws_vpc.main.id
10 
11   ingress {
12     from_port   = 443
13     to_port     = 443
14     protocol    = "tcp"
15     cidr_blocks = ["0.0.0.0/0"]
16   }
17 
18   ingress {
19     from_port   = 80
20     to_port     = 80
21     protocol    = "tcp"
22     cidr_blocks = ["0.0.0.0/0"]
23   }
24 
25   egress {
26     from_port   = 0
27     to_port     = 0
28     protocol    = "-1"
29     cidr_blocks = ["0.0.0.0/0"]
30   }
31 
32   tags = {
33     Name        = "web-sg"
34     Environment = var.environment
35   }
36 }
37 
38 resource "aws_instance" "web" {
39   ami           = "ami-0c55b159cbfafe1f0"
40   instance_type = "t2.micro"
41   
42   vpc_security_group_ids = [aws_security_group.web.id]
43   subnet_id              = aws_subnet.public.id
44 
45   user_data = <<-EOF
46     #!/bin/bash
47     echo "Hello, World" > index.html
48     nohup busybox httpd -f -p 80 &
49   EOF
50 
51   tags = {
52     Name = "web-server"
53   }
54 }
```

## Options
1. Uses AWS provider
2. Restricts SSH access
3. Opens HTTP globally
4. Uses latest AMI
5. t2.micro instance
6. Creates load balancer
7. Uses user_data
8. Unrestricted egress
9. Uses variables
10. Auto-healing setup

## Sources
- Terraform AWS Provider Documentation: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- AWS Security Best Practices: https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/welcome.html
- HashiCorp Terraform Associate Certification: https://www.hashicorp.com/certification/terraform-associate
- AWS Solutions Architect Certification Guide: https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf

## URL
[devops-hero/001](https://blog.session.it/quiz/questions/devops-hero/001-question)