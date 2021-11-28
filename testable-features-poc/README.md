# Purpose

Demonstrate how to make SQL-based features testable and verifiable within Python client, as well as show how the same client can run in pre-production and production environments.

See [testable-features-poc.ipynb](testable-features-poc.ipynb).

# Setup

To reproduce this, you'll need to:

1. Install dependencies: `pip install google-cloud-bigquery google-cloud-storage jinja2 pyyaml`
1. Setup [GCP authenication](https://cloud.google.com/docs/authentication/getting-started)
1. Create a BigQuery table and populate using the national summary data from the [Atlantic COVID Tracking Project data](https://covidtracking.com/data/download).
1. You'll need to tweak the code in `client.py`
