## DevOps Quiz Question

**Question:** Which of the following Terraform resource configurations are correct for AWS EC2 instance creation?

```
1  resource "aws_instance" "web_server" {
2    ami           = "ami-0c55b159cbfafe1f0"
3    instance_type = "t2.micro"
4    subnet_id     = aws_subnet.main.id
5    vpc_security_group_ids = [aws_security_group.allow_web.id]
6    tags = {
7      Name = "WebServer"
8    }
9    user_data = <<-EOF
10     #!/bin/bash
11     sudo apt-get update
12     sudo apt-get install -y apache2
13     sudo systemctl start apache2
14     sudo systemctl enable apache2
15   EOF
16 }
```

**Options:**
1. The AMI ID is specified correctly
2. The instance type should be in uppercase (T2.MICRO)
3. The subnet_id references a Terraform resource correctly
4. vpc_security_group_ids should be a string instead of a list
5. The Name tag follows AWS best practices
6. The user_data script requires base64 encoding
7. The EOF delimiter for user_data is properly indented
8. Apache2 service is correctly installed and enabled
9. The resource requires a mandatory key_name parameter
10. The configuration includes proper dependency handling

**Answers:**
1. TRUE
2. FALSE
3. TRUE
4. FALSE
5. TRUE
6. FALSE
7. TRUE
8. TRUE
9. FALSE
10. TRUE

```svg
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <!-- Central question -->
  <text x="250" y="250" font-size="10px" text-anchor="middle">Which of the following Terraform resource configurations are correct for AWS EC2 instance creation?</text>
  
  <!-- Options circle -->
  <circle cx="250" cy="250" r="100" fill="none" stroke="grey" stroke-dasharray="5,5"/>
  
  <!-- Answer circle -->
  <circle cx="250" cy="250" r="150" fill="none" stroke="grey" stroke-dasharray="5,5"/>
  
  <!-- Options and Answers -->
  <!-- Position 1 -->
  <text x="250" y="150" font-size="10px" text-anchor="middle">1. The AMI ID is specified correctly</text>
  <text x="250" y="100" font-size="10px" text-anchor="middle">TRUE</text>
  
  <!-- Position 2 -->
  <text x="314" y="173" font-size="10px" text-anchor="middle">2. The instance type should be in uppercase</text>
  <text x="340" y="138" font-size="10px" text-anchor="middle">FALSE</text>
  
  <!-- Position 3 -->
  <text x="346" y="233" font-size="10px" text-anchor="middle">3. The subnet_id references a Terraform resource correctly</text>
  <text x="395" y="225" font-size="10px" text-anchor="middle">TRUE</text>
  
  <!-- Position 4 -->
  <text x="327" y="310" font-size="10px" text-anchor="middle">4. vpc_security_group_ids should be a string</text>
  <text x="362" y="325" font-size="10px" text-anchor="middle">FALSE</text>
  
  <!-- Position 5 -->
  <text x="271" y="350" font-size="10px" text-anchor="middle">5. The Name tag follows AWS best practices</text>
  <text x="291" y="395" font-size="10px" text-anchor="middle">TRUE</text>
  
  <!-- Position 6 -->
  <text x="200" y="350" font-size="10px" text-anchor="middle">6. The user_data script requires base64 encoding</text>
  <text x="175" y="395" font-size="10px" text-anchor="middle">FALSE</text>
  
  <!-- Position 7 -->
  <text x="155" y="295" font-size="10px" text-anchor="middle">7. The EOF delimiter for user_data is properly indented</text>
  <text x="105" y="310" font-size="10px" text-anchor="middle">TRUE</text>
  
  <!-- Position 8 -->
  <text x="155" y="205" font-size="10px" text-anchor="middle">8. Apache2 service is correctly installed and enabled</text>
  <text x="105" y="175" font-size="10px" text-anchor="middle">TRUE</text>
  
  <!-- Position 9 -->
  <text x="200" y="150" font-size="10px" text-anchor="middle">9. The resource requires a mandatory key_name parameter</text>
  <text x="175" y="105" font-size="10px" text-anchor="middle">FALSE</text>
  
  <!-- Position 10 -->
  <text x="250" y="175" font-size="10px" text-anchor="middle">10. The configuration includes proper dependency handling</text>
  <text x="250" y="125" font-size="10px" text-anchor="middle">TRUE</text>
</svg>
```