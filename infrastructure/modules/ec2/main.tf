locals {
  default_tags = merge({
    Name        = var.instance_name
    Environment = "Dev"
    },
    var.ec2_tags,
  )
}

resource "aws_instance" "this" {
    ami = var.ami_id
    instance_type = var.instance_type
    key_name = var.key_name
    vpc_security_group_ids = var.security_group_ids
    subnet_id = var.subnet_id
    iam_instance_profile = var.iam_instance_profile
    tags = local.default_tags
}

