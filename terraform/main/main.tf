terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Create an S3 bucket for data lake storage
resource "aws_s3_bucket" "deljimae-kestra-bucket" {
  bucket        = var.s3_bucket_name
  force_destroy = true

  tags = {
    Name        = var.s3_bucket_tag_name
    Environment = var.s3_bucket_tag_environment
  }
}

# Create Athena database for raw/staging data
resource "aws_athena_database" "staging" {
  name   = var.athena_staging_database_name
  bucket = "deljimae-kestra-bucket"
}

# Create Athena database for transformed/warehouse data
resource "aws_athena_database" "dw" {
  name   = var.athena_dw_database_name
  bucket = aws_s3_bucket.global_power_bucket.bucket
}
