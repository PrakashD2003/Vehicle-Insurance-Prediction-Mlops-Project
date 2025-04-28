variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default = "vehicle-insurance-project-repo"
}

variable "image_tag_mutability" {
  description = "Whether the image tag is mutable or immutable"
  type        = string
  default     = false # mutable or true for immutable
}

variable "lifecycle_policy" {
  description = "Lifecycle policy for the ECR repository"
  type        = string
  default     = null 
}

variable "ecr_tags" {
  description = "A map of tags to assign to the ECR repository"
  type        = map(string)
  default     = {}
  
}

# where to write the output file
variable "output_file" {
  description = "Path to write out resource metadata for CI/CD"
  type        = string
  default     = "./infrastructure/outputs/ecr_info.json"
}