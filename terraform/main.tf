resource "scaleway_object_bucket" "nr-prod" {
  name = "nr-prod"
  tags = {
    env = "prod"
  }
}