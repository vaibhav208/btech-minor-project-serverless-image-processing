# Outputs will be added as resources are created
output "input_bucket_name" {
  description = "S3 bucket for original uploaded images"
  value       = aws_s3_bucket.input_bucket.bucket
}

output "output_bucket_name" {
  description = "S3 bucket for resized images"
  value       = aws_s3_bucket.output_bucket.bucket
}
output "lambda_role_arn" {
  description = "IAM role ARN for Lambda function"
  value       = aws_iam_role.lambda_role.arn
}
output "lambda_function_name" {
  description = "Image processing Lambda function name"
  value       = aws_lambda_function.image_processor.function_name
}
output "cognito_identity_pool_id" {
  value = aws_cognito_identity_pool.identity_pool.id
}
