variable "aws_region" {
  type    = string
  default = "eu-west-2"
}
variable "project_name" {
  type    = string
  default = "turbo-test-automation"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}
variable "cluster_name" {
  type    = string
  default = "turbo-test-eks"
}
variable "cluster_admin_cidrs" {
  description = "Restrict public Kubernetes API access to your own public IPv4 address /32."
  type        = list(string)
  validation {
    condition     = length(var.cluster_admin_cidrs) > 0 && alltrue([for cidr in var.cluster_admin_cidrs : can(cidrhost(cidr, 0))])
    error_message = "Set at least one valid CIDR, preferably your public IPv4 address followed by /32."
  }
}
variable "node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}
variable "node_desired_size" {
  type    = number
  default = 2
}
variable "node_min_size" {
  type    = number
  default = 1
}
variable "node_max_size" {
  type    = number
  default = 3
}
