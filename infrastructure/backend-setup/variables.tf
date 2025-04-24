variable "aws_region" {
  description = "AWS region where resources will be created"
  default     = "ap-south-1"
}

variable "sse_algorithm" {
  description = " Enrytion Technique to be used on data Objet"
  default = "AES256"  # Uses AES-256 encryption for all objects in the bucket
}

variable "billing_mode" {
  description = "Payment Mode to be used for DynamoDB"
  default = "PAY_PER_REQUEST"  # Charges based on the number of read/write requests instead of fixed capacity
}