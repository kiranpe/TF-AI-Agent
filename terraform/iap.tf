
# resource "google_iap_client" "default" {
#   display_name = "Copilot IAP Client"
#   brand         = var.brand
# }

# resource "kubernetes_secret" "iap_oauth_secret" {
#   metadata {
#     name = "iap-oauth-secret"
#   }
#   data = {
#     client_id     = base64encode(google_iap_client.default.client_id)
#     client_secret = base64encode(google_iap_client.default.secret)
#   }
# }
