output "instance_id" {
  description = "ID of the created EC2 instance"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.this.public_ip
}

resource "local_file" "ec2_metadata" {
  content = jsonencode({
    instance_name = aws_instance.this.tags["Name"]
    instance_type = aws_instance.this.instance_type
    ami_id        = aws_instance.this.ami
    key_name      = aws_instance.this.key_name
    instance_id = aws_instance.this.id
    public_ip   = aws_instance.this.public_ip
  })

  filename = var.ec2_output_file
  
}