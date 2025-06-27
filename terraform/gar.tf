resource "google_artifact_registry_repository" "docker_repo" {
  provider     = google
  location     = "us"
  repository_id = "cicd-repo"
  format       = "DOCKER"
  description  = "Docker repo for Copilot CI/CD"
}