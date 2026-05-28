resource "google_project_service" "artifactregistry" {
  service = "artifactregistry.googleapis.com"
}

resource "google_artifact_registry_repository" "orders" {
  repository_id = "api-app-math-tf"
  format = "DOCKER"
  depends_on = [
    google_project_service.artifactregistry
  ]
}

resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "api-app-tf"
  location = "europe-west4"
  client   = "terraform"
  deletion_protection=false

  depends_on = [
    google_project_service.cloudrun
  ]

  template {
    containers {
      ports {
        container_port = 8000
      }
      env {
        name = "DB"
        value = var.db
      }
      env {
        name = "DB_NAME"
        value = var.db_name
      }
      env {
        name = "DB_HOST"
        value = var.db_host
      }
      env {
        name = "DB_PORT"
        value = var.db_port
      }
      env {
        name = "DB_USERNAME"
        value = var.db_username
      }
      env {
        name = "DATA_DIR"
        value = var.data_dir
      }

      image = "europe-west4-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.orders.repository_id}/api_app-api:latest"

    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

data "google_storage_bucket" "api-app-state" {
  name = var.bucket_id
}

resource "local_file" "default" {
  file_permission = "0644"
  filename        = "${path.module}/backend.tf"

  # You can store the template in a file and use the templatefile function for
  # more modularity, if you prefer, instead of storing the template inline as
  # we do here.
  content = <<-EOT
  terraform {
    backend "gcs" {
      bucket = "${data.google_storage_bucket.api-app-state.name}"
    }
  }
  EOT
}