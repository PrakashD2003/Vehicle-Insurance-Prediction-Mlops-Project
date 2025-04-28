output "repository_url" {
  description = "URL to push/pull images"
  value       = aws_ecr_repository.this.repository_url
}

output "repository_arn" {
  description = "The ARN of the ECR repo"
  value       = aws_ecr_repository.this.arn
}

output "registry_id" {
  value = aws_ecr_repository.this.registry_id
}

resource "local_file" "ecr_metadata" {
  content = jsonencode({
    repository_name = aws_ecr_repository.this.name
    repository_url = aws_ecr_repository.this.repository_url
    repository_arn = aws_ecr_repository.this.arn
    registry_id    = aws_ecr_repository.this.registry_id
    tags           = aws_ecr_repository.this.tags
  })

  filename = var.output_file
}