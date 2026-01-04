variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "serverless-image-processing"
}
variable "image_tag" {
  description = "Docker image tag for Lambda"
  type        = string
}
