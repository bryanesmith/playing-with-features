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

To create a new repository with automatically generated name and feature stores hosted locally:

```
feast init
```

To create a new repository with features stores hosted in GCP:

```
feast init -type gcp <repo-name>
```

To publish feature changes to feature repository and enable you to use features for offline applications:

```
feast apply
```

To publish features to online feature store:

```
feast materialize 2019-01-01 2021-09-07
```

To publish additional features to online feature store after previously running `materialize` (and feast will smartly start with previous end date):

```
feast materialize-incremental 2021-09-15 # end date
```
