terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.32.0"
    }
  }
}

provider "google" {
    region = "europe-west4"
    project = var.project_id
}