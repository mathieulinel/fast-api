# variable "suffix" {
#   type = string
# }

variable "project_id" {
  default = "api-app-math-v4"
  type = string
}

# variable "cloudrun_id" {
#   type = string
# }

variable "db" {
  type = string
}

variable "db_name" {
  type = string
}

variable "db_host" {
  type = string
}

variable "db_port" {
  type = string
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type = string
}

variable "data_dir" {
  type = string
}

variable "bucket_id" {
  type = string
}