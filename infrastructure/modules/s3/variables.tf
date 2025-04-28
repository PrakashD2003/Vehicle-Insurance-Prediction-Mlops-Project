
variable "bucket_name" {
  description = "Name of the S3 Bucket"
  type        = string
  default = "vehicle-insurance-prediction-mlops-s3"
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