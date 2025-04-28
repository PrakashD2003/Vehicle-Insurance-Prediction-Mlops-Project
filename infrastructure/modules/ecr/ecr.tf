locals{
  default_tags = merge(
    {
      Name        = var.ecr_repository_name
      Environment = "Dev"
    },
    var.ecr_tags,      # user-supplied tags override these if present
  )
}

resource "aws_ecr_repository" "this" {
  name = var.ecr_repository_name
  tags = local.default_tags
  image_tag_mutability = var.image_tag_mutability
}

resource "aws_ecr_lifecycle_policy" "this" {
  count = var.lifecycle_policy != null ? 1 : 0
  repository = aws_ecr_repository.this.name
  policy     = var.lifecycle_policy
}