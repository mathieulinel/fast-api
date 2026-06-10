resource "google_project_service" "artifactregistry" {
  service = "artifactregistry.googleapis.com"
}

resource "google_artifact_registry_repository" "orders" {
  repository_id = "${terraform.workspace}-api-app-math-tf"
  format = "DOCKER"
  depends_on = [
    google_project_service.artifactregistry
  ]
}

# resource "google_sql_database_instance" "db_instance" {
#   name             = "postgres-db-instance"
#   database_version = "POSTGRES_17"
#   region           = "europe-west4"
#   deletion_protection = false
#   settings {
#     # Second-generation instance tiers are based on the machine
#     # type. See argument reference below.
#     tier = "db-f1-micro"
#   }
# }

# resource "google_sql_database" "default_db" {
#   name     = var.db
#   instance = google_sql_database_instance.db_instance.name
# }

# resource "google_sql_user" "default_user" {
#   name     = var.db_username
#   instance = google_sql_database_instance.db_instance.name
#   password = var.db_password
# }

resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "${terraform.workspace}-api-app-tf"
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

      image = "europe-west4-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.orders.repository_id}/api_app-api:2.0.0"
      # volume_mounts {
      #   name = "cloudsql"
      #   mount_path = "/cloudsql"
      # }

    }
    containers {
      env {
        name = "DB"
        value = var.db
      }
      env {
        name = "POSTGRES_DB"
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
        name = "POSTGRES_USER"
        value = var.db_username
      }
      env {
        name = "POSTGRES_PASSWORD"
        value = var.db_password
      }
      env {
        name = "PGDATA"
        value = "var/lib/postgresql/data/pgdata"
      }
      image = "postgres:17"

    }
    # volumes {
    #   name = "cloudsql"
    #   cloud_sql_instance {
    #     instances = [google_sql_database_instance.default.connection_name]
    #   }
    # }
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
  filename        = "${path.module}/${terraform.workspace}-backend.tf"

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