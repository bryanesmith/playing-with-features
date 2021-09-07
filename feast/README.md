# Feast projects

## 1. driven_hyena

Consuming offline, online features from the sample Feast offline store, `driver_stats.parquet`.

## 2. living_pegasus

Converting CSV from the [COVID Tracking Project](https://covidtracking.com/data/download) to Panda DataFrame, and using that as offline store.

Note features are cumulative. (Most likely, we'd want these to be non-cumulative, but I don't want to do work.)

## 3. covid_gcp

GCP-based equivalent to `living_pegasus` project.

# Filesystem

* `apps/`: hold toy applications consuming features from feature repositories, but in offline and online modes.
    - `apps/lib/`: store custom libraries for use by the applications.
* `data/`: stores shared data. (Any feature repository-specific data will be stored in respective repository directory.)
* `feature-repos/`: stores each Feast project.
* `utils/`: stores any command-line utilities.

# Cheatsheet

## Feast

To create a new repository with automatically generated name and feature stores hosted locally:

```
feast init
```

To create a new repository with features stores hosted in GCP:

```
feast init -t gcp <repo-name>
```

To publish feature changes to feature repository from current directory and enable you to use features for offline applications:

```
feast apply
```

To apply a repository from a different directory:

```
feast -c feature_repos/covid_gcp apply
```

To publish features to online feature store:

```
feast materialize 2019-01-01 2021-09-07
```

To publish additional features to online feature store after previously running `materialize` (and feast will smartly start with previous end date):

```
feast materialize-incremental 2021-09-15 # end date
```

## GCP

Before you can run `feast apply` on a GCP-hosted store, you need to:

1. Create a BigQuery database using `data/us-covid.parquet`
    - Don't use `us-covid.csv`; it'll fail because the `date` column isn't using timestamp format
1. Authenticate with GCP, using [these instructions](https://cloud.google.com/docs/authentication/getting-started) to:
    1. Create a service account and attach a role
    2. Download a JSON key
    3. Store path to JSON key in `GOOGLE_APPLICATION_CREDENTIALS` environment variable

Tips:
* Your first call to fetch data may fail if you don't have a Firestore (or Datastore) database setup. Error should contain instructions to fix.
* When setting `table_ref` in `BigQuerySource`, you'll get an error if you use the table ID as-is from BigQuery, in format `<project-id>:<dataset>.<table>`. Instead, switch the semi-colon to a period: `<project-id>.<dataset>.<table>`
