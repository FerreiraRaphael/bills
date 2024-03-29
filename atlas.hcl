
# The "local" environment represents our local testings.
variable "dev_token" {
  type    = string
  default = getenv("TURSO_TOKEN")
}

variable "dev_url" {
  type    = string
  default = getenv("TURSO_DB_URL")
}

env "local" {
  url = "sqlite://db/dev.sqlite"
}

env "test" {
  url = "sqlite://db/test.sqlite"
}

env "dev" {
  url     = "libsql+wss://${var.dev_url}?authToken=${var.dev_token}"
  to      = "file://db/schema.sql"
  dev-url = "sqlite://dev?mode=memory"
  exclude = ["_litestream*"]
}
