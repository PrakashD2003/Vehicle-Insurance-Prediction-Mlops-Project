output "bucket_id" {
  description = "ID of the created S3 bucket"
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.this.arn
}

output "encryption_enabled" {
  description = "Whether SSE configuration is applied"
  value       = length(aws_s3_bucket_server_side_encryption_configuration.this)
}

output "versioning_enabled" {
  description = "Whether versioning is enabled"
  value       = length(aws_s3_bucket_versioning.this)
}

