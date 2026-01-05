variable "resource_prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "log"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}