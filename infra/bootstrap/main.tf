resource "google_project" "api_app" {
  name       = "API app"
  project_id = var.project_id
  billing_account = var.billing_account
  folder_id = var.folder_id
  deletion_policy = "DELETE"
}

resource "google_storage_bucket" "api-app-state" {
  name     = var.bucket_id
  location = "US"
  project = google_project.api_app.project_id
  force_destroy               = true
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}