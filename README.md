# Serverless Image Processing System (B.Tech Minor Project)

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Terraform](https://img.shields.io/badge/Terraform-IaC-blueviolet)
![Serverless](https://img.shields.io/badge/Architecture-Serverless-green)
![Status](https://img.shields.io/badge/Project-Academic_Minor_Project-blue)

An academic serverless image processing system built on AWS that automatically resizes images when uploaded through a secure web interface.

---

## Table of Contents

- [Overview](#overview)
- [Skills Demonstrated](#skills-demonstrated)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup and Deployment](#setup-and-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Verification Steps](#verification-steps)
- [Screenshots](#screenshots)
- [Challenges and Learnings](#challenges-and-learnings)
- [Future Improvements](#future-improvements)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

This project implements an **AWS-based Serverless Image Processing System** designed as a **B.Tech minor project**.  
Users upload images via a browser-based frontend. The system automatically resizes the images using AWS Lambda and stores the processed outputs in a separate S3 bucket.

The project focuses on:
- Serverless architecture concepts
- Infrastructure as Code using Terraform
- Secure frontend uploads using Amazon Cognito
- Event-driven cloud workflows

This system is intentionally kept **simple, academic-friendly, and viva-ready**.

---

## Skills Demonstrated

- AWS Serverless Architecture
- Amazon S3 event-based workflows
- AWS Lambda (Python + Pillow)
- IAM least-privilege access design
- Amazon Cognito Identity Pools
- Terraform Infrastructure as Code
- Basic frontend-cloud integration
- Cloud debugging using CloudWatch Logs

---

## Architecture

**Architecture Diagram (Placeholder)**  
`[ Add architecture diagram here for report / viva ]`

### Flow Explanation

- User uploads an image from the browser
- Image is stored in **S3 Input Bucket**
- S3 event triggers **Lambda Function**
- Lambda resizes the image and creates a thumbnail
- Processed images are stored in **S3 Output Bucket**
- User accesses processed images via public S3 URLs

---

## Tech Stack

| Category            | Tool / Service |
|---------------------|---------------|
| Cloud Provider      | AWS |
| Storage             | Amazon S3 |
| Compute             | AWS Lambda |
| Authentication      | Amazon Cognito Identity Pool |
| IaC                 | Terraform |
| Language            | Python |
| Image Library       | Pillow |
| Frontend            | HTML, JavaScript |
| Logging             | Amazon CloudWatch |

---

## Prerequisites

- AWS Account  
  https://aws.amazon.com/

- AWS CLI  
  https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

- Terraform  
  https://developer.hashicorp.com/terraform/downloads

- Docker Desktop  
  https://www.docker.com/products/docker-desktop/

- Git  
  https://git-scm.com/

---

## Setup and Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/vaibhav208/btech-minor-project-serverless-image-processing.git
cd btech-minor-project-serverless-image-processing
```
### 2. Configure AWS Credentials

Run the following command to set up your AWS CLI with the necessary access keys and region:

```bash
aws configure
```
### 3. Build and Push Lambda Docker Image

Navigate to the lambda directory, build the Docker image for the `linux/amd64` platform, and push it to Amazon ECR.

> **Note:** Replace `<AWS_ACCOUNT_ID>` with your actual AWS Account ID.

```bash
cd lambda
docker build --platform=linux/amd64 -t <AWS_ACCOUNT_ID>[.dkr.ecr.us-east-1.amazonaws.com/serverless-image-processing-lambda:lambda](https://.dkr.ecr.us-east-1.amazonaws.com/serverless-image-processing-lambda:lambda) .
docker push <AWS_ACCOUNT_ID>[.dkr.ecr.us-east-1.amazonaws.com/serverless-image-processing-lambda:lambda](https://.dkr.ecr.us-east-1.amazonaws.com/serverless-image-processing-lambda:lambda)
```
### 4. Deploy Infrastructure Using Terraform

Initialize and apply the Terraform configuration to provision the infrastructure.

```bash
cd terraform
terraform init
terraform apply
```
### 5. Update Frontend Configuration

Edit the `frontend/app.js` file and update the following values with the outputs from the Terraform deploy:

* **Cognito Identity Pool ID**
* **AWS Region**
* **Input Bucket Name**

## CI/CD Pipeline

**Not implemented.**

This project intentionally avoids CI/CD pipelines to keep the scope suitable for academic evaluation. All deployments are performed manually using Terraform and Docker.

## Verification Steps

1. Open `frontend/index.html` in a browser.
2. Select an image file.
3. Upload the image.
4. **Verify the following:**
    * Upload success message is displayed.
    * Lambda logs appear in CloudWatch.
    * Resized image appears in the output S3 bucket.
    * Thumbnail image appears in the output S3 bucket.

## Screenshots

* **Frontend upload screen** *(placeholder)*
* **CloudWatch Lambda logs** *(placeholder)*
* **S3 input and output buckets** *(placeholder)*

## Challenges and Learnings

The table below summarizes the **major challenges faced during the project**, the **approach used to resolve them**, and the **key learnings**, written in an academic and viva-friendly manner.

| Phase | Challenge | Root Cause | Approach Used | Key Learning |
|------|---------|-----------|---------------|-------------|
| Lambda Packaging | Pillow library import error (`_imaging` missing) | Lambda runtime mismatch with locally built dependencies | Switched from ZIP-based Lambda to **Docker image–based Lambda** using AWS-provided base image | Container images ensure runtime consistency and reduce dependency issues |
| Docker + Lambda | `InvalidParameterValueException: image manifest not supported` | Docker Buildx produced OCI manifest not supported by Lambda | Disabled provenance and used correct platform (`linux/amd64`) | AWS Lambda supports only specific image formats and architectures |
| Terraform State | Lambda deployment failing due to missing image | Image tag mismatch between Terraform and ECR | Introduced `image_tag` variable and enforced tag consistency | Infrastructure and application artifacts must stay tightly aligned |
| S3 Event Handling | `NoSuchKey` error during image fetch | URL-encoded S3 object keys (`%28`, `%29`) | Decoded object key inside Lambda using URL decoding | S3 events provide encoded object keys by default |
| IAM Permissions | AccessDenied errors for S3 operations | Missing `s3:ListBucket` and scoped permissions | Refined IAM policy with least-privilege actions | IAM permissions must match API behavior, not assumptions |
| Frontend Upload | Browser upload failed with CORS error | S3 bucket lacked CORS configuration | Added CORS rules via Terraform | Browser-based cloud access requires explicit CORS rules |
| Public Access | Processed image URLs returned `AccessDenied` | Account-level Block Public Access prevented bucket policy | Temporarily disabled account-level block and applied bucket policy | AWS account-level settings override resource-level permissions |
| Observability | Difficult to debug silent failures | Insufficient logging in Lambda | Added structured CloudWatch logs | Logging is essential for debugging serverless systems |
| Event Reliability | Failed Lambda executions lost silently | No retry or failure handling | Conceptual DLQ design using SQS (academic-safe) | DLQs improve reliability and fault isolation |
| Terraform Debugging | Repeated apply failures with no changes | Terraform state drift confusion | Used `terraform plan` + logs before reapply | Terraform state awareness is critical for stable IaC |
| Frontend Integration | Upload succeeded but output not visible | Output bucket access misconfigured | Enabled public read for output bucket only | Separation of read/write access improves security |
| Architecture Design | Risk of overengineering | Academic project constraints | Chose minimal AWS services only | Simpler architectures are easier to explain in viva |
| Security Scope | Risk of unrestricted uploads | No file validation initially | Added file type and size checks in Lambda | Validation should be enforced server-side |
| Performance | Large images slowed processing | Single-size resize initially | Added thumbnail generation | Multiple output sizes improve usability |
| Academic Constraints | Balancing depth vs complexity | Overuse of DevOps tools not suitable | Limited tooling to Terraform + Docker | Tool choice should match project goals |

---

### Overall Takeaway

This project demonstrated that **serverless systems shift complexity from infrastructure management to integration, permissions, and observability**.  
The systematic debugging approach—logs → permissions → configuration → architecture—proved essential and is directly applicable to real-world cloud engineering.

This experience significantly strengthened understanding of **event-driven architectures**, **cloud-native debugging**, and **Infrastructure as Code discipline**, while remaining well within **academic evaluation standards**.


## Future Improvements

* [ ] Add CloudFront for faster image delivery.
* [ ] Add user-specific folders using Cognito identity IDs.
* [ ] Add optional API Gateway layer.
* [ ] Improve frontend UI.
* [ ] Add image format conversion.

## Repository Structure

```text
btech-minor-project-serverless-image-processing/
├── frontend/
│   ├── index.html
│   └── app.js
├── lambda/
│   ├── Dockerfile
│   └── image_processor.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── README.md
```
## Contributing

This repository is intended for academic use.

Contributions are not expected, but suggestions are welcome via issues.

## License

This project is provided for **educational purposes only**.

> **Disclaimer:** No production guarantees are provided.

## Author

**Vaibhav Sarkar**
*B.Tech Student*
*Minor Project – Cloud Computing & DevOps*

* **GitHub:** [https://github.com/vaibhav208](https://github.com/vaibhav208)
