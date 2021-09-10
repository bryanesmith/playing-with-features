# Setup

1. Setup Hopsworks cluster
    - Can use [hosted demo platform](https://managed.hopsworks.ai/signup) for trial period

2. `pip install hsfs[hive] pyarrow`

3. While logged into Hopsworks, under your account > Settings > Api keys, create a key with all scopes (except you may not need inference). **Save the secret; you cannot retrieve it again later.**

4. Before running scripts, set environment variables:

    ```
    export HSFS_API_KEY=abc123yourapikeysecret
    export HSFS_HOST=yourhost.cloud.hopsworks.ai
    export HSFS_PORT=443
    export HSFS_PROJECT=your_project_name
    ```

5. Create the database. **Warning: this will delete us_covid feature group in your project if it exists.**:
    ```
    python us-covid/setup_features_unsafe.py
    ```

6. Fetch data from offline and online stores:
    ```
    python us-covid/fetch_features.py
    ```

## Challenges
* Field validation error message when creating feature store not displayed in new UI
* Had to disable time travel when creating feature group due to error
* Error messages with jobs obfuscated by RestAPIError
* Jobs sometimes take very long time to run
* Error with query running in job that doesn't result in error when running locally
* Dumps random files in your filesystem, not sure when or why
