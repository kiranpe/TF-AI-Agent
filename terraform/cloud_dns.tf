
resource "google_compute_global_address" "copilot_static_ip" {
  name = "copilot-static-ip"
  project = var.project_id
  ip_version = "IPV4"
  address_type = "EXTERNAL"
  description = "Reserved IP for HTTPS Load Balancer (Copilot)"
}

resource "google_compute_managed_ssl_certificate" "copilot_cert" {
  name    = "copilot-cert"
  project = var.project_id
  managed {
    domains = [var.domain]
  }
}

resource "google_dns_managed_zone" "copilot_zone" {
  name        = "copilot-zone"
  dns_name    = var.domain_with_dot
  description = "Managed zone for Copilot App"
}

resource "google_dns_record_set" "copilot_dns" {
  name         = "copilot.${google_dns_managed_zone.copilot_zone.dns_name}"
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.copilot_zone.name
  rrdatas      = [google_compute_global_address.default.address]
}
