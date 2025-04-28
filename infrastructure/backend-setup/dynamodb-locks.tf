resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = var.billing_mode


  attribute {
    name = var.aws_dynamodb_table_hash_key
    type = "S"
  }


  hash_key = var.aws_dynamodb_table_hash_key


  point_in_time_recovery {
    enabled = true
  }
}