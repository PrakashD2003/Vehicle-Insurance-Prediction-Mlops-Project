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
  sg_description = var.sg_description
  sg_output_file = var.sg_output_file
  sg_tags        = var.sg_tags
}

module "ec2" {
  source             = "../modules/ec2"
  instance_name      = var.instance_name
  instance_type      = var.instance_type
  ami_id             = var.ami_id
  key_name           = var.key_name
  subnet_id          = var.subnet_id
  security_group_ids = var.security_group_ids
  ec2_output_file    = var.ec2_output_file
  ec2_tags           = var.ec2_tags
}

