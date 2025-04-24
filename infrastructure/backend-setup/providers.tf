terraform {
  required_version = "v1.11.4"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.33.0"
    }
  }
}

provider "aws" {
  region = var.aws_region # AWS region is set using a variable
}

