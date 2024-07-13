variable "datasets" {
  description = "A map of datasets and their tables"
  type = map(
    list(
      object({
        table_id    = string
        schema_file = string
      })
    )
  )
}
