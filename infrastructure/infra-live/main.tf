data "aws_vpc" "default" {
  default = true
}


module "ecr" {
  source               = "../modules/ecr"
  ecr_repository_name  = var.ecr_repository_name
  image_tag_mutability = var.image_tag_mutability
  lifecycle_policy     = var.lifecycle_policy
  output_file          = var.output_file
  ecr_tags             = var.ecr_tags
}

module "s3" {
  source            = "../modules/s3"
  bucket_name       = var.bucket_name
  sse_algorithm     = var.sse_algorithm
  force_destroy     = var.force_destroy
  enable_versioning = var.enable_versioning
  enable_sse        = var.enable_sse
  s3_tags           = var.s3_tags
}

module "security_group" {
  source         = "../modules/security_group"
  sg_name        = var.sg_name
  vpc_id         = data.aws_vpc.default.id
  ingress_rules  = var.ingress_rules
  egress_rules   = var.egress_rules
  sg_description = var.sg_description
  sg_output_file = var.sg_output_file
  sg_tags        = var.sg_tags
}

resource "aws_iam_openid_connect_provider" "github_oidc" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = [
    // the certificate thumbprint for token.actions.githubusercontent.com
    "6938fd4d98bab03faadb97b34396831e3780aea1",
  ]
}




data "aws_iam_policy_document" "ci_assume" {
  statement {
    effect    = "Allow"
    actions   = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github_oidc.arn]
    }

    # Exact match on the audience
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Exact match on the GitHub repo:branch
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_owner}/${var.github_repo}:ref:refs/heads/main"]
    }
  }
}


data "aws_iam_policy_document" "ec2_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# 2. CI Role
module "ci_role" {
  source             = "../modules/iam_role"
  role_name          = "${var.github_repo}-ci-role"
  assume_role_policy = data.aws_iam_policy_document.ci_assume.json

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess",
  ]

  iam_role_tags = {
    Name        = "${var.github_repo}-ci-role"
    Environment = "Dev"
  }
  iam_role_output_file = var.iam_role_output_file
}

# 3. EC2 Role
module "ec2_role" {
  source             = "../modules/iam_role"
  role_name          = "${var.github_repo}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
  ]

  iam_role_tags = {
    Name        = "${var.github_repo}-ec2-role"
    Environment = "Dev"
  }
  iam_role_output_file = var.iam_role_output_file
}

# 4. Instance Profile for EC2
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.github_repo}-ec2-profile"
  role = module.ec2_role.role_name
}

module "ec2" {
  source               = "../modules/ec2"
  instance_name        = var.instance_name
  instance_type        = var.instance_type
  ami_id               = var.ami_id
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
  key_name             = var.key_name
  subnet_id            = var.subnet_id
  security_group_ids   = var.security_group_ids
  ec2_output_file      = var.ec2_output_file
  ec2_tags             = var.ec2_tags
}



