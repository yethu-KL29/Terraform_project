
/////////////dbt cloud Terraform Project//////////////////////

//1. Provider Configuration

provider "google" {
  credentials = file("C:/Users/yethu/Downloads/projecttransformed-d34992713caa.json")
  project     = "projecttransformed"
  region      = "us-central1"
}


//2. Dataset Resource Creation

resource "google_bigquery_dataset" "datasets" {
  for_each = var.datasets

  dataset_id = each.key
  location   = "US"
}
//3. Table Resource Creation

resource "google_bigquery_table" "tables" {
  for_each = { for dataset, tables in var.datasets : dataset => tables }

  dataset_id = google_bigquery_dataset.datasets[each.key].dataset_id
  table_id   = each.value[0].table_id
  schema     = file(each.value[0].schema_file)

}


// it is for  inserting the resource_utilisation_table IaC

/////////////////////////////////////////////////////////////////////////////////////////////////


resource "google_bigquery_table" "update_table" {
  dataset_id = google_bigquery_dataset.datasets["resource_utilisation_schema"].dataset_id
  table_id   = "resource_utilisation_table"
  schema     = file("resource_utilisation_schema.json")

  deletion_protection = false
}

// used the command : terraform apply -target=google_bigquery_table.update_table

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////