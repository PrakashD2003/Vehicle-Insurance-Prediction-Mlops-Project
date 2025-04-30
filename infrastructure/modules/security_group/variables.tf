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
  default = ""
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