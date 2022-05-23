provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

variable "aws_region" {
  default = "us-west-2"
}

variable "aws_profile" {
  default = ""
}

# This key must already exist - it will not be created by Terraform
variable "key_name" {
  default = "django_key"
}

# Ubuntu AMIs from https://cloud-images.ubuntu.com/locator/ec2/
variable "instance_ami" {
  default = "ami-01380ef7bcd9184ca" # Ubuntu 22.04 arm64 HVM/EBS in us-west-2
}

variable "instance_size" {
  default = "t4g.micro"
}

data "aws_availability_zones" "available" {}

# AWS will assign the VPC an IPv6 CIDR with a prefix length of /56
resource "aws_vpc" "django_vpc" {
  cidr_block                       = "10.128.0.0/16"
  enable_dns_support               = true
  enable_dns_hostnames             = true
  assign_generated_ipv6_cidr_block = true

  tags = {
    Name = "django_vpc"
  }
}

# The subnet IPv6 CIDR must be in the VPC CIDR and have a prefix length of /64
resource "aws_subnet" "django_public_subnet" {
  vpc_id          = aws_vpc.django_vpc.id
  cidr_block      = cidrsubnet(aws_vpc.django_vpc.cidr_block, 4, 0)
  ipv6_cidr_block = cidrsubnet(aws_vpc.django_vpc.ipv6_cidr_block, 8, 0)

  map_public_ip_on_launch         = true
  assign_ipv6_address_on_creation = true

  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "django_public_subnet"
  }
}

# The security group must allow ingress and egress from IPv6
resource "aws_security_group" "django_security" {
  name        = "django_security"
  description = "Django Security"
  vpc_id      = aws_vpc.django_vpc.id

  revoke_rules_on_delete = true

  tags = {
    Name = "django_security"
  }
}

resource "aws_security_group_rule" "egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  description       = "All egress traffic"
  security_group_id = aws_security_group.django_security.id
}

resource "aws_security_group_rule" "http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  description       = "All HTTP traffic"
  security_group_id = aws_security_group.django_security.id
}

resource "aws_security_group_rule" "https" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  description       = "All HTTPS traffic"
  security_group_id = aws_security_group.django_security.id
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.django_vpc.id

  tags = {
    Name = "django_gateway"
  }
}

resource "aws_route_table" "django_route_table" {
  vpc_id = aws_vpc.django_vpc.id

  # Route all IPv6 traffic to the Internet gateway
  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.default.id
  }

  # Route all IPv4 traffic to the Internet gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

  tags = {
    Name = "django_subnet"
  }
}

# The route table must be associated with the subnet
resource "aws_route_table_association" "django_public_assoc" {
  subnet_id      = aws_subnet.django_public_subnet.id
  route_table_id = aws_route_table.django_route_table.id
}

# Create the web EC2 instance
resource "aws_instance" "django_web" {
  ami           = var.instance_ami
  instance_type = var.instance_size
  key_name      = var.key_name
  subnet_id     = aws_subnet.django_public_subnet.id

  vpc_security_group_ids      = [aws_security_group.django_security.id]
  associate_public_ip_address = true
  disable_api_termination     = false

  # To keep your current IPv6 address when replacing the AWS instance, add it below:
  # ipv6_addresses = []

  root_block_device {
    volume_size = 8  # The size of the provisioned EBS
  }

  tags = {
    Name = "django_web"
  }
}
