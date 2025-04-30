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
  default = ""
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

variable "iam_instance_profile" {
  description = "Name of the IAM Instance Profile to attach to this EC2 (optional)"
  type        = string
  default     = null
}

# where to write the output file
variable "ec2_output_file" {
  description = "Path to write out resource metadata for CI/CD"
  type        = string
  default     = "./outputs/ecr_info.json"
}

