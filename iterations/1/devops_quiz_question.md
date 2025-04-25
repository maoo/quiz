## DevOps Quiz Question

**Question:** Which statements about this Terraform configuration are correct?

```hcl
1  resource "aws_security_group" "web_sg" {
2    name        = "web-sg"
3    description = "Security group for web servers"
4    vpc_id      = aws_vpc.main.id
5  
6    ingress {
7      from_port   = 80
8      to_port     = 80
9      protocol    = "tcp"
10     cidr_blocks = ["0.0.0.0/0"]
11   }
12 
13   ingress {
14     from_port   = 443
15     to_port     = 443
16     protocol    = "tcp"
17     cidr_blocks = ["0.0.0.0/0"]
18   }
19 
20   egress {
21     from_port   = 0
22     to_port     = 0
23     protocol    = "-1"
24     cidr_blocks = ["0.0.0.0/0"]
25   }
26 
27   tags = {
28     Name = "web-sg"
29     Environment = var.environment
30   }
31 }
```

**Options:**
1. Line 4 references a VPC resource that must be defined elsewhere
2. Lines 10 and 17 allow access from any IP address
3. Line 23 specifies UDP protocol for egress traffic
4. This security group allows HTTPS traffic
5. The security group blocks all outbound traffic
6. Line 20-25 creates a rule that permits all outbound traffic
7. The configuration will fail because no ICMP rules are defined
8. Line 29 uses a variable that must be defined elsewhere
9. The security group allows SSH access on port 22
10. This security group needs an explicit dependency on aws_vpc.main

**Answers:**
1. TRUE
2. TRUE
3. FALSE
4. TRUE
5. FALSE
6. TRUE
7. FALSE
8. TRUE
9. FALSE
10. FALSE