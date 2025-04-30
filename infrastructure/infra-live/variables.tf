variable "aws_region" {
  description = "The AWS region to deploy the infrastructure"
  type        = string
  default     = "ap-south-1" # Default region can be changed as per requirement

}

### ECR Repository Configuration ###
variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "vehicle-insurance-project-repo"
}

variable "ecr_tags" {
  description = "Tags to apply to the ECR repository"
  type        = map(string)
  default     = {}
}

variable "image_tag_mutability" {
  description = "Whether the image tag is mutable or immutable"
  type        = string
  default     = false
}

variable "lifecycle_policy" {
  description = "Lifecycle policy for the ECR repository"
  type        = string
  default     = null
}

variable "output_file" {
  description = "Path to write out resource metadata for CI/CD"
  type        = string
  default     = "./infrastructure/outputs/ecr_info.json"
}





#### S3 Bucket Configuration ###
variable "bucket_name" {
  description = "Name of the S3 Bucket"
  type        = string
  default     = "vehicle-insurance-prediction-mlops-s3"
}

variable "sse_algorithm" {
  description = "SSE algorithm to use (e.g. aws:kms)"
  type        = string
  default     = "AES256"
}


variable "force_destroy" {
  description = "Whether to delete all objects when destroying the bucket"
  type        = bool
  default     = false
}

variable "enable_versioning" {
  description = "Enable bucket versioning"
  type        = bool
  default     = false
}

variable "enable_sse" {
  description = "Enable server-side encryption"
  type        = bool
  default     = false
}


variable "s3_tags" {
  description = "A map of tags to assign to the bucket"
  type        = map(string)
  default     = {}
}





### Security Group Configuration ###
variable "sg_name" {
  description = "Name for the SG"
  type        = string
}
variable "sg_description" {
  description = "SG description"
  type        = string
  default     = "managed by Terraform"
}
variable "vpc_id" {
  description = "ID of the VPC to attach SG to"
  type        = string
  default     = ""
}

# simple 1-rule example; you can expand this to lists of maps
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
}

variable "egress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
    { from_port = 0, to_port = 0, protocol = "-1", cidr_blocks = ["0.0.0.0/0"] }
  ]
}

variable "sg_tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}

variable "sg_output_file" {
  description = "Path to write out resource metadata for CI/CD"
  type        = string
  default     = "./outputs/sg_info.json"
}





### EC2 Instance Configuration ###
variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID where EC2 will be launched"
  type        = string
  default     = ""
}

variable "security_group_ids" {
  description = "List of security group IDs"
  type        = list(string)
}

variable "key_name" {
  description = "Key pair name for SSH access"
  type        = string
}

variable "instance_name" {
  description = "Name tag for the EC2 instance"
  type        = string
}

variable "ec2_tags" {
  description = "Additional tags for EC2"
  type        = map(string)
  default     = {}
}

variable "ec2_output_file" {
  description = "Path to write out resource metadata for CI/CD"
  type        = string
  default     = "./outputs/ecr_info.json"
}

variable "iam_instance_profile" {
  description = "Name of the IAM Instance Profile to attach to this EC2 (optional)"
  type        = string
  default     = null
}





### IAM ROLE CONFIGURATION ###
# variable "role_name" {
#   description = "Name of the IAM role to create"
#   type        = string
# }

# variable "assume_role_policy" {
#   description = "The JSON policy that grants an entity permission to assume the role"
#   type        = string
# }

variable "managed_policy_arns" {
  description = "List of IAM managed policy ARNs to attach to the role"
  type        = list(string)
  default     = []
}

variable "inline_policies" {
  description = <<EOF
Map of inline policies to attach.  
Key   = policy name  
Value = JSON policy document  
EOF
  type        = map(string)
  default     = {}
}

variable "iam_role_tags" {
  description = "Tags to apply to the IAM role"
  type        = map(string)
  default     = {}
}

variable "iam_role_output_file" {
  description = "If non-null, write this role’s metadata (name, id, arn, tags) to this JSON file"
  type        = string
  default     = null
}

variable "github_owner" {
  description = "GitHub owner or organization name for the CI OIDC trust policy"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name for the CI OIDC trust policy"
  type        = string
}
