output "security_group_id" {
  description = "The ID of the security group"
  value       = aws_security_group.this.id
}

resource "local_file" "sg_metadata" {
  filename = var.sg_output_file
  content  = jsonencode({   
    security_group_name = aws_security_group.this.name,
    security_group_id = aws_security_group.this.id,
    vpc_id            = aws_security_group.this.vpc_id,
    tags              = aws_security_group.this.tags,
    description       = aws_security_group.this.description,
  })
}
