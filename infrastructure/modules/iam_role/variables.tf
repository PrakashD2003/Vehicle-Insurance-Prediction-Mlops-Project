variable "role_name" {
  description = "Name of the IAM role to create"
  type        = string
}

variable "assume_role_policy" {
  description = "The JSON policy that grants an entity permission to assume the role"
  type        = string
}

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
  type    = map(string)
  default = {}
}

variable "iam_role_tags" {
  description = "Tags to apply to the IAM role"
  type        = map(string)
  default     = {}
}

# where to write the output file
variable "iam_role_output_file" {
  description = "If non-null, write this role’s metadata (name, id, arn, tags) to this JSON file"
  type        = string
  default     = null
}
