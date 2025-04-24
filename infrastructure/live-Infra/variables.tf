variable "aws_region" {
  description = "AWS region where resources will be created"
  default     = "ap-south-1"
}

variable "sse_algorithm" {
  description = " Enrytion Technique to be used on data Objet"
  default     = "AES256" # Uses AES-256 encryption for all objects in the bucket
}

  