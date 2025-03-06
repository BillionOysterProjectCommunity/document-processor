provider "google" {
  project     = "ors-document-analysis"
  region      = "us-east1"
}

resource "google_storage_bucket" "ors-storage-v2" {
  provider = google
  name          = "ors-storage-v2-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      days_since_noncurrent_time = 3
      send_age_if_zero = false
    }
  }
}
