output "role_name" {
  description = "The name of the IAM Role"
  value       = aws_iam_role.this.name
}

output "role_id" {
  description = "The stable ID of the IAM role"
  value       = aws_iam_role.this.id
}

output "role_arn" {
  description = "The ARN of the IAM role"
  value       = aws_iam_role.this.arn
}

output "role_tags" {
  description = "Tags attached to the IAM Role"
  value       = aws_iam_role.this.tags
}

resource "local_file" "iam_role_metadata" {
  # only create if the caller supplied a filename
  count    = var.iam_role_output_file != null ? 1 : 0
  filename = var.iam_role_output_file
  content  = jsonencode({
    role_name = aws_iam_role.this.name
    role_id   = aws_iam_role.this.unique_id
    role_arn  = aws_iam_role.this.arn
    tags      = aws_iam_role.this.tags
  })
}
