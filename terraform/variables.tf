variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for data lake storage"
  default     = "deljimae-kestra-bucket"
}

variable "s3_bucket_tag_name" {
  description = "Tag name for the S3 bucket"
  default     = "deljimae-kestra-bucket"
}

variable "s3_bucket_tag_environment" {
  description = "Environment tag for the S3 bucket"
  default     = "Dev"
}

variable "athena_staging_database_name" {
  description = "Athena database name for staging/raw data"
  default     = "kestradb"
}

variable "athena_dw_database_name" {
  description = "Athena database name for transformed/warehouse data"
  default     = "kestradb"
}
