resource "aws_s3_bucket" "mlops_s3_bucket" {
  bucket = "vehicle-insurance-prediction-mlops-s3"
  tags = {
    Name        = "Vehicle-Insurance-Prediction-Project-Data-Bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "mlops_s3_bucket_versioning" {
  bucket = aws_s3_bucket.mlops_s3_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mlops_s3_bucket_encryption" {
  bucket = aws_s3_bucket.mlops_s3_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = var.sse_algorithm
    }
  }
}

resource "aws_s3_bucket_public_access_block" "mlops_s3_bucket_block_public_access" {
  bucket = aws_s3_bucket.mlops_s3_bucket.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}