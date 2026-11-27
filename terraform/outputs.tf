output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}
output "aws_region" {
  value = var.aws_region
}
output "cluster_name" {
  value = aws_eks_cluster.main.name
}
output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}
output "backend_ecr_repository_url" {
  value = aws_ecr_repository.backend.repository_url
}
output "frontend_ecr_repository_url" {
  value = aws_ecr_repository.frontend.repository_url
}
output "update_kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.main.name}"
}
