resource "scaleway_object_bucket" "nr-prod" {
  name = "nr-prod"
  tags = {
    env = "prod"
  }
}

resource "scaleway_object_bucket" "nr-dev" {
  name = "nr-dev"
  tags = {
    env = "dev"
  }
}