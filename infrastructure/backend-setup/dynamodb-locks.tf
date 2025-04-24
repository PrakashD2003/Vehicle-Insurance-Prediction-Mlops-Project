resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = var.billing_mode


  attribute {
    name = "LockID"
    type = "S"
  }


  hash_key = "LockID"


  point_in_time_recovery {
    enabled = true
  }
}