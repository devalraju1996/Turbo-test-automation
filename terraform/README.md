# Turbo Test Automation — Terraform

Creates a learning/lab AWS environment in eu-west-2:
- VPC, two public subnets in separate AZs, Internet Gateway and routes
- EKS control plane and managed EC2 worker node group
- ECR repositories for frontend and backend
- IAM roles and policies required by EKS

## Network and cost choices
This is a lab design, not a production network design. Worker nodes are placed in public subnets to avoid a NAT Gateway and its recurring hourly/data charges. The EKS public API endpoint is restricted to the CIDR you provide. The default worker size is two t3.medium instances. One node is cheaper but has no worker-node redundancy.

EKS control plane, EC2 nodes, EBS volumes, ECR storage, and later load balancers can incur charges. Review AWS pricing before applying and destroy the lab when finished.

## Configure
Copy `terraform.tfvars.example` to `terraform.tfvars`. Get your public IPv4 in PowerShell:

    (Invoke-RestMethod -Uri "https://checkip.amazonaws.com").Trim()

Set `cluster_admin_cidrs` to your real address plus `/32`, e.g. `["198.51.100.24/32"]`. The sample IP in the example file is documentation-only and must be replaced.

## Validate and plan
Run from this folder:

    terraform init
    terraform fmt -recursive
    terraform validate
    terraform plan -out=tfplan
    terraform show tfplan

Check the account, region, resource list and instance sizes. Do not apply if anything is unexpected. Only after reviewing and approving the plan:

    terraform apply tfplan

Then connect kubectl:

    aws eks update-kubeconfig --region eu-west-2 --name turbo-test-eks
    kubectl get nodes

## Cleanup
Remove Kubernetes LoadBalancer services and other separately-created resources first, then run:

    terraform destroy

Review the destroy plan. ECR repositories use `force_delete = false`, so delete images/repositories separately if Terraform reports they are not empty.

## Jenkins note
This starter uses local Terraform state. Do not run concurrent applies from different machines or Jenkins. Before Jenkins manages Terraform, migrate state to a dedicated encrypted S3 backend with state locking and restrict access using an IAM role. Never commit credentials, `terraform.tfvars`, or Terraform state.
