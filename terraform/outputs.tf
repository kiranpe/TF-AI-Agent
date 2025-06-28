
# output "iap_client_id" {
#   value = google_iap_client.default.client_id
# }
# output "iap_client_secret" {
#   value = google_iap_client.default.secret
# }
output "static_ip" {
  value = google_compute_global_address.copilot_static_ip.address
}
